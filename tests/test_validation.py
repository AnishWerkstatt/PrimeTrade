from pathlib import Path

from src.primetrade.validation import validate_input_csv


def test_validate_input_csv_accepts_csv_path(tmp_path: Path) -> None:
    csv_file = tmp_path / "sample.csv"
    csv_file.write_text("close\n1\n", encoding="utf-8")
    validate_input_csv(csv_file)
