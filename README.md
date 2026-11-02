# Batch Quarantine

Check a JSON batch against a field contract before release. A single invalid row quarantines the entire batch and the report preserves every row-level reason.

## Run locally

Use Python 3.12. The project uses the standard library. From the repository root:

```sh
python cli.py example.json
python -m unittest -v
```

The included example is synthetic. Pass a different UTF-8 JSON file to inspect your own input. The command prints JSON to stdout. Invalid input returns status 2 and an explanation on stderr. See [CONTRACT.md](CONTRACT.md) for input fields and interpretation.

## Operational limits

The gate returns a routing decision for a caller to apply. Input is held in memory. It distinguishes JSON booleans from integers, rejects nonfinite numbers and reports field names and row numbers only.

## Resumen en español

Valida lotes completos contra un contrato y explica cada rechazo sin volcar los valores originales.
