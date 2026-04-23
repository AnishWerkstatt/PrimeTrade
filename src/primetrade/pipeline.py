from pathlib import Path
from time import perf_counter

import logging
import pandas as pd

from src.primetrade.config import AppConfig
from src.primetrade.validation import validate_input_csv


def _load_csv_with_fallback(input_csv: Path, logger: logging.Logger) -> pd.DataFrame:
    try:
        df = pd.read_csv(input_csv)
    except Exception as exc:
        raise ValueError(f"Invalid CSV format: {input_csv}") from exc

    # Some exports wrap each full line in quotes, causing pandas to read one column.
    if len(df.columns) == 1 and "," in str(df.columns[0]):
        logger.warning(
            "Detected quoted-line CSV format. Applying fallback parser.",
            extra={"event": "csv_fallback_parser"},
        )
        column_names = [name.strip() for name in str(df.columns[0]).split(",")]
        expanded = df.iloc[:, 0].astype(str).str.strip('"').str.split(",", expand=True)

        if expanded.shape[1] != len(column_names):
            raise ValueError(
                "CSV fallback parsing failed: unexpected number of columns after split"
            )

        expanded.columns = column_names
        return expanded

    return df


def run_pipeline(input_csv: Path, config: AppConfig, logger: logging.Logger) -> dict:
    start = perf_counter()
    logger.info("Pipeline started", extra={"event": "pipeline_start"})

    validate_input_csv(input_csv)
    full_df = _load_csv_with_fallback(input_csv, logger)

    if full_df.empty:
        raise ValueError("CSV is empty")

    if "close" not in full_df.columns:
        raise ValueError("Missing required column: close")

    try:
        close = pd.to_numeric(full_df["close"], errors="coerce")
    except Exception as exc:
        raise ValueError("Unable to parse 'close' column as numeric") from exc

    if close.isna().all():
        raise ValueError("Column 'close' has no valid numeric values")

    logger.info(
        "Rows loaded",
        extra={"event": "rows_loaded", "rows": int(len(full_df))},
    )

    full_df = full_df.copy()
    full_df["close"] = close
    full_df["rolling_mean"] = close.rolling(window=config.window, min_periods=config.window).mean()
    logger.info("Rolling mean computed", extra={"event": "rolling_mean_done"})

    full_df = full_df.dropna(subset=["close", "rolling_mean"]).copy()
    logger.info(
        "Rows after dropping NaN",
        extra={
            "event": "rows_after_dropna",
            "rows_after_dropping_na": int(len(full_df)),
        },
    )

    if full_df.empty:
        raise ValueError("No valid rows after applying rolling window")

    signal = (full_df["close"] > full_df["rolling_mean"]).astype(int)
    logger.info("Signal generated", extra={"event": "signal_generated"})

    latency_ms = int((perf_counter() - start) * 1000)
    metrics = {
        "version": config.version,
        "rows_processed": int(len(signal)),
        "metric": "signal_rate",
        "value": round(float(signal.mean()), 4),
        "latency_ms": latency_ms,
        "seed": config.seed,
        "status": "success",
    }

    logger.info(
        "Metrics computed",
        extra={
            "event": "metrics_summary",
            "rows": metrics["rows_processed"],
        },
    )
    return metrics
