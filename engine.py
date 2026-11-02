import math
from collections import defaultdict

TYPES = {"string": str, "integer": int, "number": (float, int), "boolean": bool}


def matches(value, kind):
    if kind == "number":
        return type(value) is int or (type(value) is float and math.isfinite(value))
    return type(value) is TYPES[kind]


def evaluate(data):
    schema, key, rows = data["schema"], data["key"], data["rows"]
    if not isinstance(schema, dict) or schema.get(key) not in ("integer", "string"):
        raise ValueError("key needs a string or integer schema")
    if any(kind not in TYPES for kind in schema.values()) or not isinstance(rows, list):
        raise ValueError("unsupported schema or rows")
    issues, owners = [], defaultdict(list)
    def flag(number, field, reason):
        issues.append(dict(row=number, field=field, reason=reason))
    for number, row in enumerate(rows, 1):
        if not isinstance(row, dict):
            flag(number, None, "invalid_record")
            continue
        for field in sorted(row.keys() - schema.keys()):
            flag(number, field, "unexpected")
        for field, kind in schema.items():
            if field not in row:
                flag(number, field, "missing")
            elif not matches(row[field], kind):
                flag(number, field, "wrong_type")
            elif field == key:
                owners[row[key]].append(number)
    for numbers in owners.values():
        if len(numbers) > 1:
            for number in numbers:
                flag(number, key, "duplicate")
    return {"verdict": "quarantine" if issues else "release", "rows": len(rows),
            "issues": sorted(issues, key=lambda r: (r["row"], r["field"] or "", r["reason"]))}
