import csv
import os

CSV_FILE = "wellness_data.csv"

FIELDNAMES = [
    "date",
    "stress",
    "sleep",
    "friends",
    "exercise",
    "hobbies",
    "meds",
    "water",
    "steps",
    "advice"
]


def ensure_csv_exists():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()
        print("📁 Created CSV file with headers!")
    else:
        print("📁 CSV file already exists.")


def append_entry(entry_dict):
    # Check for missing fields
    for field in FIELDNAMES:
        if field not in entry_dict:
            raise KeyError(f"Missing field: {field}")

    with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writerow(entry_dict)

    print("💾 Entry saved successfully!")
