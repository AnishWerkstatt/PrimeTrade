# PrimeTrade MLOps Assignment

## Quick Start (Evaluator)

```powershell
docker build -t primetrade-pipeline .
docker run --rm primetrade-pipeline
```

This repository implements a minimal MLOps-style batch pipeline demonstrating:
- Reproducibility (config + seed)
- Observability (structured logs + metrics)
- Deployment readiness (Dockerized, one-command execution)

## Deliverables in this repo

- run.py
- config.yaml
- data.csv
- requirements.txt
- Dockerfile
- README.md
- metrics.json (sample successful output)
- run.log (sample successful log)

## 1) Environment setup (Windows PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If activation is blocked:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

## 2) Local run (required CLI)

```powershell
python run.py --input data.csv --config config.yaml --output metrics.json --log-file run.log
```

## Row count note

For a rolling window of 5 and ~10,000 input rows:
- `rows_loaded` ≈ 10000
- `rows_processed` ≈ 9996

This is correct because the first `window - 1` rows do not have a rolling mean yet and are dropped with explicit NaN handling.

## Reproducibility

The pipeline is deterministic. Results are reproducible across runs due to the fixed random seed specified in `config.yaml`.

## 3) Build Docker image

```powershell
docker build -t primetrade-pipeline .
```

## 4) Run Docker container

Default run (used for evaluation):

```powershell
docker run --rm primetrade-pipeline
```

Optional: run with volume mount for local file access or debugging:

```powershell
docker run --rm -v "${PWD}:/app" primetrade-pipeline
```

## Example metrics.json (success)

```json
{
	"version": "v1",
	"rows_processed": 9996,
	"metric": "signal_rate",
	"value": 0.4953,
	"latency_ms": 75,
	"seed": 42,
	"status": "success"
}
```
