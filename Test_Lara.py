"""
E-Lif(e) Tracker - Daily Wellness & Habit Tracker
===================================================

SCENARIO:
The E-lif(e) Tracker is designed for quick, end-of-day use. The user runs the
application from the console, is prompted with quick questions about their day's habits,
and, upon completion, automatically generates a clear status report with a personalized
wellness score and actionable advice.

USER STORIES:
1. As a User, I want to track my daily habits by answering simple, quick questions 
   in order to stay strong and healthy.
2. As a User, I want to quickly add information about my lifestyle (nutrition, sport, sleep) 
   in order to get decisive and valuable information for improvement.
3. As a User, I want to receive a daily status report that gives personalized advice based 
   on my input in order to keep me motivated.
4. As a User, I want the history of my daily reports to be saved so I can view my progress 
   over time in order to track my improvement and development.

USE CASES:
• Enter daily wellness data (sleep, stress, exercise, etc.) ✓
• Validate each entry to prevent invalid input ✓
• Save all inputs to a file (e.g., 'weekly_data.txt'). Saving inputs for 28 days ✓
• Generate a weekly status report ('report.txt') with advice and summaries ✓
"""

import datetime
import json
import os
from Menu import decision

DATA_FILE = "girlypop_data.json"
WEEKLY_DATA_FILE = "weekly_data.txt"
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
    with open(WEEKLY_DATA_FILE, "a", encoding="utf-8") as f:
        f.write(f"\n{'='*50}\n")
        f.write(f"Date: {day['date']}\n")
        f.write(f"Score: {day['score']}\n")
        f.write(
            f"Sleep: {day['sleep']}, Stress: {day['stress']}, Mood: {day['mood']}\n")
        f.write(
            f"Exercise: {day['exercise']}, Water: {day['water']}, Steps: {day['steps']}\n")
        f.write(
            f"Friends: {day['friends']}, Hobbies: {day['hobbies']}, Meds: {day['meds']}\n")

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
        except:
            pass
        print(f"❌ Invalid input. Please enter a number" +
              (f" between {min_val}-{max_val}" if min_val and max_val else "") + ".")


def collect_daily_inputs():
    """
    USE CASE: Enter daily wellness data
    - Prompts user with quick questions
    - Validates each entry to prevent invalid input
    - Returns complete daily entry
    """
    today = datetime.datetime.now().strftime("%Y/%m/%d")

    print("\n🌟 Quick Daily Check-in 🌟")
    print(f"Today: {today}\n")

    day = {
        "date": today,
        "sleep": ask_choice("Sleep (good/medium/bad): ", SLEEP_MAP),
        "stress": ask_number("Stress (1-5): ", 1, 5),
        "friends": ask_choice("Hung out with friends? (yes/no): ", YES_NO_MAP),
        "water": classify_water(),
        "exercise": ask_choice("Exercise? (yes/no): ", YES_NO_MAP),
        "mood": ask_choice(f"Mood {list(MOOD_MAP.keys())}: ", MOOD_MAP),
        "work_hours": ask_number("Work hours: ", 0, None, True),
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


def process_day(day):
    """
    USE CASE: Generate daily status report with personalized advice
    - Calculates wellness score based on all metrics
    - Provides actionable, personalized advice
    - Returns score and advice list
    """
    score = sum([
        day["sleep"], day["friends"], day["water"], day["exercise"],
        day["mood"], day["steps"], day["hobbies"], day["meds"]
    ])

    advice = []

    # Stress handling
    if day["stress"] <= 2:
        score += 3
    elif day["stress"] == 3:
        score += 1
    else:
        advice.append("💪 Lower your stress bestie!")

    # Personalized advice based on metrics
    if day["friends"] == 1:
        advice.append("🌿 Touch grass with friends!")
    if day["water"] == 1:
        advice.append("💧 Hydrate queen!")
    if day["exercise"] == 1:
        advice.append("🏃 Move your body!")
    if day["mood"] == 1:
        advice.append("💖 Your mood needs attention!")
    if day["steps"] == 1:
        advice.append("👟 Walk more!")
    if day["hobbies"] == 1:
        advice.append("🎨 Do something fun!")
    if day["meds"] == 1:
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
            avg = sum(d[field] for d in week_data) / len(week_data)
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
        field: sum(d[field] for d in data) / len(data)
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

    # Save JSON
    json_name = f"monthly_report_{today.year}_{today.month:02d}.json"
    json.dump(report, open(json_name, "w"), indent=4)

# TXT. FOR MORRE DEFINTION

    # Save TXT
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


def run():
    """
    Main application loop implementing all use cases:
    1. Load historical data (28+ days)
    2. Collect daily inputs with validation
    3. Generate immediate status report with advice
    4. Save to history
    5. Option to view weekly/monthly reports
    """
    data = load_data()
    print(f"✨ E-Lif(e) Tracker - Loaded {len(data)} previous days")

    while True:
        choice = decision()

        if choice == 1:
            # USE CASE 1 & 2: Enter and validate daily data
            day = collect_daily_inputs()

            if input("\nChange date? (yes/no): ").lower().strip() == "yes":
                while True:
                    new = input("Enter date (yyyy/mm/dd): ").strip()
                    try:
                        datetime.datetime.strptime(new, "%Y/%m/%d")
                        day["date"] = new
                        break
                    except ValueError:
                        print("❌ Invalid format.")

            # USE CASE 3: Generate personalized status report
            processed, advice = process_day(day)
            data.append(processed)

            # USE CASE 4: Save to history (28+ day tracking)
            save_data(data)
            append_to_weekly_log(processed)

            print(
                f"\n✅ Saved {processed['date']} → Wellness Score: {processed['score']}")
            if advice:
                print("\n💡 Personal Advice for Today:")
                for a in advice:
                    print(f"   {a}")

        elif choice == 2:
            print("\n📊 Generating Monthly Report...")
            save_monthly_report(data)

        elif choice == 3:
            print("Goodbye queen ✨")
            break


run()
