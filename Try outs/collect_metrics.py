"""Single-user metrics collector.

Provides `collect_metrics` which validates inputs, optionally saves them
to `data/metrics.csv`, and returns a list of saved records. It supports
both interactive use (prompts) and programmatic use by passing a
`user_inputs` dict mapping metric keys to string values.
"""
from datetime import datetime
from pathlib import Path
import csv
from typing import Optional, Dict, Any, List, Tuple

DATA_DIR = Path("data")
CSV_PATH = DATA_DIR / "metrics.csv"
FIELDNAMES = ["timestamp", "metric", "value", "units", "context", "comment"]


FIELDS: List[Tuple[str, str, type, Optional[Tuple[float, float]], str]] = [
    ("sleep_duration", "Sleep last night (hours, e.g. 7.5): ", float, (0, 24), "hours"),
    ("water_ml", "Water consumed today (ml, e.g. 1500): ", float, (0, 20000), "ml"),
    ("steps", "Steps today (count): ", int, (0, 100000), "count"),
    ("mood", "Mood (1-5): ", int, (1, 5), "rating"),
]


def ensure_data_dir() -> None:
    DATA_DIR.mkdir(exist_ok=True)


def append_metric(metric: str, value: Any, units: str, context: str = "", comment: str = "") -> None:
    first = not CSV_PATH.exists()
    with CSV_PATH.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        if first:
            writer.writeheader()
        writer.writerow({
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "metric": metric,
            "value": value,
            "units": units,
            "context": context,
            "comment": comment,
        })


def parse_number(s: str, cast: type = float):
    try:
        return cast(s.replace(",", "").strip())
    except Exception:
        return None


def _validate_and_build(key: str, raw: str, caster: type, valid_range: Optional[Tuple[float, float]], units: str,
                        context: str = "daily_checkin") -> Optional[Dict[str, Any]]:
    if raw is None:
        return None
    raw = raw.strip()
    if raw == "":
        return None
    value = parse_number(raw, cast=caster)
    if value is None:
        return None
    if valid_range is not None:
        low, high = valid_range
        try:
            if not (low <= value <= high):
                return None
        except Exception:
            return None
    if caster is int:
        value = int(value)

    return {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "metric": key,
        "value": value,
        "units": units,
        "context": context,
        "comment": "",
    }


def collect_metrics(user_inputs: Optional[Dict[str, str]] = None, save: bool = True,
                    context: str = "daily_checkin") -> List[Dict[str, Any]]:
    """Collect metrics for single user.

    - If `user_inputs` is None, prompts the user interactively for each field.
    - If `user_inputs` is provided, it should be a dict mapping metric keys
      (e.g. "sleep_duration") to string values (as if typed by the user).
    - Returns a list of validated records (and saves each to CSV when
      `save` is True).
    """
    ensure_data_dir()
    records: List[Dict[str, Any]] = []

    for key, prompt, caster, valid_range, units in FIELDS:
        if user_inputs is not None:
            raw = user_inputs.get(key, "").strip()
        else:
            raw = input(prompt).strip()

        rec = _validate_and_build(key, raw, caster, valid_range, units, context=context)
        if rec is None:
            # skip invalid or empty
            continue
        if save:
            append_metric(rec["metric"], rec["value"], rec["units"], context=rec.get("context", ""))
        records.append(rec)

    return records


if __name__ == "__main__":
    # Interactive run: collect and print returned records
    recs = collect_metrics()
    if not recs:
        print("No valid entries were provided.")
    else:
        print(f"Saved {len(recs)} record{'s' if len(recs) != 1 else ''}:")
        for r in recs:
            print(f" - {r['metric']}: {r['value']} {r['units']} ({r['timestamp']})")
