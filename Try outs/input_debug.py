# Run the tracker function()


def collect_session(user_id=""):
    """
    Compact collector: iterates over defined fields, validates, then appends.
    """
    fields = [
        ("sleep_duration", "Sleep last night (hours, e.g. 7.5): ", float, None, "hours"),
        ("water_ml", "Water consumed today (ml, e.g. 1500): ", float, None, "ml"),
        ("steps", "Steps today (count): ", int, None, "count"),
        ("mood", "Mood (1-5): ", int, (1, 5), "rating"),
    ]

    print("Quick check-in: enter values or leave blank to skip.")
    saved = 0
    for key, prompt, caster, valid_range, units in fields:
        raw = input(prompt).strip()
        if raw == "":
            continue
        try:
            # allow commas in numbers like "1,500"
            cleaned = raw.replace(",", "")
            value = caster(cleaned)
        except ValueError:
            print(f"  → Invalid value for {key}, skipped.")
            continue
        if valid_range and not (valid_range[0] <= value <= valid_range[1]):
            print(
                f"  → {key} must be between {valid_range[0]} and {valid_range[1]}; skipped.")
            continue

        # optional cast for steps/mood to int
        if caster is int:
            value = int(value)
        append_metric(key, value, units, user_id=user_id,
                      context="daily_checkin")
        saved += 1

    print(f"Thanks — saved {saved} item{'s' if saved != 1 else ''}.")

python3 collect_metrics.py

from collect_metrics import collect_metrics

inputs = {
    "sleep_duration": "7.5",
    "water_ml": "1500",
    "steps": "4200",
    "mood": "4",
}
records = collect_metrics(user_inputs=inputs, save=True)
print(records)  # list of dicts for each validated metric