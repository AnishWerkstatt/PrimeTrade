from pathlib import Path

def validate_input_csv(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")
    if not path.is_file():
        raise ValueError(f"Input path is not a file: {path}")
    if path.suffix.lower() != ".csv":
        raise ValueError(f"Expected a .csv file, got: {path}")
