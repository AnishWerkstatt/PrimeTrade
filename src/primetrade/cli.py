import argparse
from pathlib import Path

from src.primetrade.config import RunArgs


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="PrimeTrade technical assessment runner")
    parser.add_argument("--input", dest="input_csv", type=Path, required=True, help="Path to input CSV")
    parser.add_argument("--config", type=Path, required=True, help="Path to config.yaml")
    parser.add_argument("--output", type=Path, required=True, help="Path to output metrics.json")
    parser.add_argument("--log-file", type=Path, required=True, help="Path to run log file")
    return parser


def parse_args() -> RunArgs:
    args = build_parser().parse_args()
    return RunArgs(
        input_csv=args.input_csv,
        config_path=args.config,
        output_path=args.output,
        log_file=args.log_file,
    )
