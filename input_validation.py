"""
input_validation.py - Input Validation & Collection Module
Handles all user input with validation
"""

import datetime

SLEEP_MAP = {"bad": 1, "medium": 2, "good": 3}
MOOD_MAP = {
    "angry": 1, "anxious": 1, "irritable": 1,
    "hyper": 2,
    "calm": 3, "relaxed": 3, "happy": 3
}
YES_NO_MAP = {"no": 1, "yes": 2}


def ask_choice(prompt, mapping):
    """Validate choice-based input."""
    while True:
        value = input(prompt).lower().strip()
        if value in mapping:
            return mapping[value]
        print("❌ Invalid input. Please try again.")


def ask_number(prompt, min_val=None, max_val=None, is_float=False):
    """Validate numeric input with range checking."""
    while True:
        try:
            value = float(input(prompt)) if is_float else int(input(prompt))
            if (min_val is None or value >= min_val) and \
               (max_val is None or value <= max_val):
                return value
        except ValueError:
            pass
        print(
            f"❌ Invalid input. Please enter a number"
            + (f" between {min_val}-{max_val}" if min_val and max_val else "")
            + "."
        )


def to_number(val):
    try:
        return int(val)
    except (ValueError, TypeError):
        try:
            return float(val)
        except (ValueError, TypeError):
            return 0


def classify_water():
    """Classify water intake into levels with realistic limits."""
    w = ask_number("Water (liters): ", 0, 10, True)
    return 1 if w < 1 else 2 if w <= 1.5 else 3


def classify_steps():
    """Classify daily steps into levels with realistic limits."""
    s = ask_number("Steps: ", 0, 50000)
    return 1 if s < 4000 else 2 if s < 10000 else 3


def collect_daily_inputs():
    today = datetime.datetime.now().strftime("%Y/%m/%d")
    while True:
        change = input(
            f"Today is {today}. Do you want to change the date? (yes/no): "
        ).strip().lower()
        if change == "yes":
            while True:
                custom_date = input("Enter the date (YYYY/MM/DD): ").strip()
                try:
                    datetime.datetime.strptime(custom_date, "%Y/%m/%d")
                    date = custom_date
                    break
                except ValueError:
                    print("❌ Invalid date format. Please try again.")
            break
        elif change == "no":
            date = today
            break
        else:
            print("Please answer 'yes' or 'no'.")

    print("\n🌟 Quick Daily Check-in 🌟")
    print(f"Date: {date}\n")

    day = {
        "date": date,
        "sleep": ask_choice("Sleep (good/medium/bad): ", SLEEP_MAP),
        "stress": ask_number("Stress (1-5): ", 1, 5),
        "friends": ask_choice("Hung out with friends? (yes/no): ", YES_NO_MAP),
        "water": classify_water(),
        "exercise": ask_choice("Exercise? (yes/no): ", YES_NO_MAP),
        "mood": ask_choice(f"Mood {list(MOOD_MAP.keys())}: ", MOOD_MAP),
        "work_hours": ask_number("Work hours: ", 0, 16, True),
        "hobbies": ask_choice("Hobbies today? (yes/no): ", YES_NO_MAP),
        "steps": classify_steps(),
        "meds": ask_choice("Meds taken? (yes/no): ", YES_NO_MAP)
    }
    return day


if __name__ == "__main__":
    # Test module
    print("✅ input_validation.py loaded successfully")
    print("   Testing ask_choice...")
    # Uncomment to test:
    # result = ask_choice("Test (yes/no): ", YES_NO_MAP)
    # print(f"   Result: {result}")
