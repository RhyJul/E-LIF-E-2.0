"""
data_storage.py - Data Storage & Loading Module
Handles loading and saving data from/to JSON files
"""

import json
import os

DATA_FILE = "data/girlypop_data.json"
WEEKLY_DATA_FILE = "data/weekly_data.txt"


def load_data():
    """Load all historical data from JSON file."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_data(data):
    """Save all data to JSON file (maintains 28+ day history)."""
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def append_to_weekly_log(day):
    """Append daily entry to weekly_data.txt for 28-day tracking."""
    os.makedirs("data", exist_ok=True)
    with open(WEEKLY_DATA_FILE, "a", encoding="utf-8") as f:
        f.write(f"\n{'='*50}\n")
        f.write(f"Date: {day['date']}\n")
        f.write(f"Score: {day['score']}\n")
        f.write(
            f"Sleep: {day['sleep']}, Stress: {day['stress']}, "
            f"Mood: {day['mood']}\n"
        )
        f.write(
            f"Exercise: {day['exercise']}, Water: {day['water']}, "
            f"Steps: {day['steps']}\n"
        )
        f.write(
            f"Friends: {day['friends']}, Hobbies: {day['hobbies']}, "
            f"Meds: {day['meds']}\n"
        )


if __name__ == "__main__":
    # Test module
    print("✅ data_storage.py loaded successfully")
    test_data = load_data()
    print(f"   Loaded {len(test_data)} records")
