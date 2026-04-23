from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass(frozen=True)
class RunArgs:
    input_csv: Path
    config_path: Path
    output_path: Path
    log_file: Path


@dataclass(frozen=True)
class AppConfig:
    seed: int
    window: int
    version: str


def load_config(config_path: Path) -> AppConfig:
    if not config_path.exists() or not config_path.is_file():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    try:
        with config_path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        raise ValueError(f"Invalid YAML format in config: {config_path}") from exc

    if not isinstance(data, dict):
        raise ValueError("Config must be a YAML object with keys: seed, window, version")

    required_keys = ("seed", "window", "version")
    missing = [key for key in required_keys if key not in data]
    if missing:
        raise ValueError(f"Config missing required keys: {missing}")

    seed = data["seed"]
    window = data["window"]
    version = data["version"]

    if not isinstance(seed, int) or seed < 0:
        raise ValueError("Config 'seed' must be a non-negative integer")
    if not isinstance(window, int) or window <= 0:
        raise ValueError("Config 'window' must be a positive integer")
    if not isinstance(version, str) or not version.strip():
        raise ValueError("Config 'version' must be a non-empty string")

    return AppConfig(seed=seed, window=window, version=version.strip())
