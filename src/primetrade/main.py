import json
import sys
from pathlib import Path

from src.primetrade.cli import parse_args
from src.primetrade.config import AppConfig, load_config
from src.primetrade.logging_utils import setup_logging
from src.primetrade.pipeline import run_pipeline
from src.primetrade.reproducibility import set_global_seed


def _write_metrics(output_path: Path, metrics: dict) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(metrics, f, ensure_ascii=True, indent=2)


def main() -> None:
    args = parse_args()
    logger = setup_logging(args.log_file)

    version = "v1"

    try:
        logger.info(
            "Job started",
            extra={
                "event": "job_start",
                "input_csv": str(args.input_csv),
            },
        )

        config: AppConfig = load_config(args.config_path)
        version = config.version
        logger.info(
            "Config loaded and validated",
            extra={
                "event": "config_validated",
                "seed": config.seed,
                "window": config.window,
                "version": config.version,
            },
        )

        set_global_seed(config.seed)
        metrics = run_pipeline(args.input_csv, config, logger)
        _write_metrics(args.output_path, metrics)
        logger.info("Job completed successfully", extra={"event": "job_end_success"})
        print(json.dumps(metrics, ensure_ascii=True))
    except Exception as exc:
        error_metrics = {
            "version": version,
            "status": "error",
            "error_message": str(exc),
        }
        _write_metrics(args.output_path, error_metrics)
        logger.exception("Job failed", extra={"event": "job_end_error"})
        print(json.dumps(error_metrics, ensure_ascii=True))
        sys.exit(1)


if __name__ == "__main__":
    main()
