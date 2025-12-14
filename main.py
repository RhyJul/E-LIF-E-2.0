import datetime
import json
import os
from menu import main_menu

DATA_FILE = "data/girlypop_data.json"
WEEKLY_DATA_FILE = "data/weekly_data.txt"
WEEKLY_REPORT_FILE = "weekly_report.txt"

# Input mappings for validation
SLEEP_MAP = {"bad": 1, "medium": 2, "good": 3}
MOOD_MAP = {
    "angry": 1, "anxious": 1, "irritable": 1,
    "hyper": 2,
    "calm": 3, "relaxed": 3, "happy": 3
}
YES_NO_MAP = {"no": 1, "yes": 2}

FIELDS_NUMERIC = ["sleep", "stress", "friends", "water",
                  "exercise", "mood", "work_hours", "hobbies", "steps", "meds"]

# ==========================================
# Data Storage & Loading (28 Day History)
# ==========================================


def load_data():
    """Load all historical data from JSON file."""
    if os.path.exists(DATA_FILE):
        return json.load(open(DATA_FILE))
    return []


def save_data(data):
    """Save all data to JSON file (maintains 28+ day history)."""
    json.dump(data, open(DATA_FILE, "w"), indent=4)


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

# ==========================================
# Input Validation & Collection
# ==========================================


def ask_choice(prompt, mapping):
    """Validate choice-based input."""
    while True:
        value = input(prompt).lower().strip()
        if value in mapping:
            return mapping[value]
        print("❌ Invalid input. Please try again.")


# DEFINITION FROM LOWEST TO HIGHEST NUMBER
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


def collect_daily_inputs():
    """
    USE CASE: Enter daily wellness data
    - Prompts user with quick questions
    - Validates each entry to prevent invalid input
    - Returns complete daily entry
    """
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
        # How should I understand that???
        "work_hours": ask_number("Work hours: ", 0, 16, True),
        "hobbies": ask_choice("Hobbies today? (yes/no): ", YES_NO_MAP),
        "steps": classify_steps(),
        "meds": ask_choice("Meds taken? (yes/no): ", YES_NO_MAP)
    }
    return day


def classify_water():
    """Classify water intake into levels with realistic limits."""
    w = ask_number("Water (liters): ", 0, 10,
                   True)  # Max 10 liters (realistic limit)
    return 1 if w < 1 else 2 if w <= 1.5 else 3


def classify_steps():
    """Classify daily steps into levels with realistic limits."""
    s = ask_number(
        "Steps: ", 0, 50000)  # Max 50,000 steps (realistic limit for a day)

# ==========================================
# Wellness Score Calculation & Advice
# ==========================================


advice = []


def to_number(val):
    try:
        return int(val)
    except (ValueError, TypeError):
        try:
            return float(val)
        except (ValueError, TypeError):
            return 0


def process_day(day):
    """
    USE CASE: Generate daily status report with personalized advice
    - Calculates wellness score based on all metrics
    - Provides actionable, personalized advice
    - Returns score and advice list
    """
    score = sum(
        to_number(day.get(key))
        for key in [
            "sleep", "friends", "water", "exercise", "mood",
            "steps", "hobbies", "meds"
        ]
    )

    advice = []

    # Stress handling
    if to_number(day.get("stress")) <= 2:
        score += 3
    elif to_number(day.get("stress")) == 3:
        score += 1
    else:
        advice.append("💪 Lower your stress bestie!")

    # Personalized advice based on metrics
    if to_number(day.get("friends")) == 1:
        advice.append("🌿 Touch grass with friends!")
    if to_number(day.get("water")) == 1:
        advice.append("💧 Hydrate queen!")
    if to_number(day.get("exercise")) == 1:
        advice.append("🏃 Move your body!")
    if to_number(day.get("mood")) == 1:
        advice.append("💖 Your mood needs attention!")
    if to_number(day.get("steps")) == 1:
        advice.append("👟 Walk more!")
    if to_number(day.get("hobbies")) == 1:
        advice.append("🎨 Do something fun!")
    if to_number(day.get("meds")) == 1:
        advice.append("💊 Don't forget your meds!")

    day["score"] = score
    return day, advice

# ==========================================
# Weekly Report Generation
# ==========================================


def generate_weekly_report(data):
    """
    USE CASE: Generate weekly status report
    - Calculates averages for the past 7 days
    - Provides summary and recommendations
    - Saves to weekly_report.txt
    """
    if not data or len(data) < 1:
        return "❌ Not enough data for weekly report"

    # Get last 7 days
    week_data = data[-7:] if len(data) >= 7 else data

    report = f"\n{'='*60}\n"
    report += f"📊 WEEKLY WELLNESS REPORT\n"
    report += f"{'='*60}\n"
    report += f"Period: {week_data[0]['date']} to {week_data[-1]['date']}\n"
    report += f"Days tracked: {len(week_data)}\n\n"

    avg_score = sum(d["score"] for d in week_data) / len(week_data)
    report += f"📈 Average Daily Score: {avg_score:.1f}\n\n"

    report += "METRIC AVERAGES:\n"
    for field in FIELDS_NUMERIC:
        if field in week_data[0]:
            avg = sum((d.get(field) or 0) for d in week_data) / len(week_data)
            report += f"  • {field}: {avg:.1f}\n"

    # Summary
    report += f"\n{'─'*60}\n"
    if avg_score >= 18:
        report += "🌟 Excellent week! Keep up the great habits!\n"
    elif avg_score >= 15:
        report += "✨ Good week! Small improvements possible.\n"
    else:
        report += "💪 Time to focus on your wellness goals!\n"

    return report


def save_weekly_report(data):
    """Save weekly report to text file."""
    report = generate_weekly_report(data)

    with open(WEEKLY_REPORT_FILE, "w", encoding="utf-8") as f:
        f.write(report)

    print(report)
    print(f"✅ Report saved to {WEEKLY_REPORT_FILE}")

# ==========================================
# Monthly Report (Enhanced)
# ==========================================


def save_monthly_report(data):
    """
    Generate comprehensive monthly report in JSON and TXT format.
    """
    if not data:
        print("❌ No days logged this month 😭")
        return

    today = datetime.datetime.now()

    averages = {
        field: sum((d.get(field) or 0) for d in data) / len(data)
        for field in FIELDS_NUMERIC
    }

    report = {
        "month": today.month,
        "year": today.year,
        "days_logged": len(data),
        "total_score": sum(d["score"] for d in data),
        "average_score": sum(d["score"] for d in data) / len(data),
        "averages": averages
    }

    # Save JSON in data folder with 'monthly_data' in filename
    os.makedirs("data", exist_ok=True)
    json_name = f"data/monthly_data_{today.year}_{today.month:02d}.json"
    with open(json_name, "w") as f:
        json.dump(report, f, indent=4)

    # Save TXT in root folder
    txt_name = f"monthly_report_{today.year}_{today.month:02d}.txt"
    with open(txt_name, "w", encoding="utf-8") as f:
        f.write("💗 MONTHLY GIRLYPOP WELLNESS REPORT 💗\n")
        f.write("="*60 + "\n")
        f.write(f"Month: {today.month}/{today.year}\n")
        f.write(f"Days logged: {report['days_logged']}\n")
        f.write(f"Total score: {report['total_score']}\n")
        f.write(f"Average score: {report['average_score']:.1f}\n\n")
        f.write("AVERAGES BY METRIC:\n")
        for k, v in averages.items():
            f.write(f"  • {k}: {v:.1f}\n")

    print(f"\n✅ Reports saved!\n  📄 JSON: {json_name}\n  📋 TXT: {txt_name}")

# ==========================================
# Main Program Flow
# ==========================================


def to_number(val):
    try:
        return int(val)
    except (ValueError, TypeError):
        try:
            return float(val)
        except (ValueError, TypeError):
            return 0


def process_day(day):
    """
    USE CASE: Generate daily status report with personalized advice
    - Calculates wellness score based on all metrics
    - Provides actionable, personalized advice
    - Returns score and advice list
    """
    score = sum(
        to_number(day.get(key))
        for key in [
            "sleep", "friends", "water", "exercise", "mood",
            "steps", "hobbies", "meds"
        ]
    )

    advice = []

    # Stress handling
    if to_number(day.get("stress")) <= 2:
        score += 3
    elif to_number(day.get("stress")) == 3:
        score += 1
    else:
        advice.append("💪 Lower your stress bestie!")

    # Personalized advice based on metrics
    if to_number(day.get("friends")) == 1:
        advice.append("🌿 Touch grass with friends!")
    if to_number(day.get("water")) == 1:
        advice.append("💧 Hydrate queen!")
    if to_number(day.get("exercise")) == 1:
        advice.append("🏃 Move your body!")
    if to_number(day.get("mood")) == 1:
        advice.append("💖 Your mood needs attention!")
    if to_number(day.get("steps")) == 1:
        advice.append("👟 Walk more!")
    if to_number(day.get("hobbies")) == 1:
        advice.append("🎨 Do something fun!")
    if to_number(day.get("meds")) == 1:
        advice.append("💊 Don't forget your meds!")

    day["score"] = score
    return day, advice
# Main Program Flow
# ==========================================


def run():
    data = load_data()
    print(f"✨ E-Lif(e) Tracker - Loaded {len(data)} previous days")

    while True:
        choice = main_menu()

        if choice == 1:
            day = collect_daily_inputs()
            processed, advice = process_day(day)
            data.append(processed)
            save_data(data)
            append_to_weekly_log(processed)
            print(
                f"\n✅ Saved {processed['date']} → Wellness Score:"
                f"{processed['score']}"
            )
            if advice:
                print("\n💡 Personal Advice for Today:")
                for a in advice:
                    print(f"   {a}")
        elif choice == 2:
            print("\n📊 Generating Monthly Report...")
            save_monthly_report(data)
        elif choice == 3:
            print("\n📊 Generating Weekly Report...")
            save_weekly_report(data)
        elif choice == 4:
            print("Goodbye queen ✨")
            break


run()
