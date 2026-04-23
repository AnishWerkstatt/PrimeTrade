import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        for key in (
            "event",
            "input_csv",
            "output_dir",
            "seed",
            "rows",
            "rows_after_dropping_na",
            "window",
            "version",
        ):
            if hasattr(record, key):
                payload[key] = getattr(record, key)

        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)

        return json.dumps(payload, ensure_ascii=True)


def setup_logging(log_file: Path, level: str = "INFO") -> logging.Logger:
    logger = logging.getLogger("primetrade")
    logger.setLevel(level.upper())
    logger.handlers.clear()
    logger.propagate = False

    formatter = JsonFormatter()

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    log_file.parent.mkdir(parents=True, exist_ok=True)
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger
