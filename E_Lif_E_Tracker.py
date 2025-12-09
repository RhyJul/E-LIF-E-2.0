
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
# Generate Monthly Advice (Simple & Helpful)
# ==========================================


def generate_monthly_advice(averages):
    """Generate simple, non-medical advice based on monthly metrics."""
    advice_list = []

    # Sleep advice
    if averages.get("sleep", 0) < 2:
        advice_list.append(
            "💤 Your sleep quality seems low. Try to get to bed earlier and create a calm bedtime routine.")
    elif averages.get("sleep", 0) >= 2.5:
        advice_list.append(
            "✨ Great sleep! Keep your consistent sleep schedule.")

    # Stress advice
    if averages.get("stress", 0) > 3.5:
        advice_list.append(
            "😌 High stress this month. Try taking short breaks, go for walks, or practice breathing exercises.")
    elif averages.get("stress", 0) <= 2:
        advice_list.append(
            "🌟 Your stress levels are great! Keep doing what you're doing.")

    # Exercise advice
    if averages.get("exercise", 0) < 1.5:
        advice_list.append(
            "🏃 You could move more! Try a 20-minute walk or dance to your favorite songs.")
    elif averages.get("exercise", 0) >= 1.8:
        advice_list.append(
            "💪 Awesome exercise habits! You're taking great care of yourself.")

    # Water intake advice
    if averages.get("water", 0) < 1.5:
        advice_list.append(
            "💧 Drink more water! Aim for 2-3 liters daily. Add some lemon or mint for flavor.")
    elif averages.get("water", 0) >= 2.5:
        advice_list.append(
            "💙 Perfect hydration! You're doing amazing with your water intake.")

    # Social life advice
    if averages.get("friends", 0) < 1.5:
        advice_list.append(
            "👯 Try connecting with friends more. Even a quick call or text can boost your mood!")
    elif averages.get("friends", 0) >= 1.8:
        advice_list.append(
            "🌈 Great social life! Keep nurturing those connections.")

    # Hobbies advice
    if averages.get("hobbies", 0) < 1.5:
        advice_list.append(
            "🎨 Make time for hobbies! Even 30 minutes of something you love can make a big difference.")
    elif averages.get("hobbies", 0) >= 1.8:
        advice_list.append(
            "🎭 Love seeing you take time for hobbies! That's so important for your wellbeing.")

    # Medication/health advice
    if averages.get("meds", 0) < 1.5:
        advice_list.append(
            "💊 Don't forget your daily routine! Setting phone reminders can help.")
    elif averages.get("meds", 0) >= 1.8:
        advice_list.append("✅ Excellent consistency with your health routine!")

    # Steps advice
    if averages.get("steps", 0) < 1.5:
        advice_list.append(
            "👟 More movement needed! Try parking farther away or taking stairs instead of elevators.")
    elif averages.get("steps", 0) >= 2.5:
        advice_list.append("🚶 Fantastic activity levels! Keep it up!")

    # Mood advice
    if averages.get("mood", 0) < 2:
        advice_list.append(
            "💖 Your mood could use a boost. Try something that makes you smile—a favorite show, song, or snack!")
    elif averages.get("mood", 0) >= 2.5:
        advice_list.append(
            "😊 Your mood is great! You've got positive energy this month.")

    return advice_list


# ==========================================
# Monthly Report (Enhanced with Advice)
# ==========================================


def save_monthly_report(data):
    """
    Generate comprehensive monthly report in JSON and TXT format with personalized advice.
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

    # Generate advice
    advice = generate_monthly_advice(averages)

    # Save JSON
    json_name = f"monthly_report_{today.year}_{today.month:02d}.json"
    json.dump(report, open(json_name, "w"), indent=4)

    # Save TXT with advice
    txt_name = f"monthly_report_{today.year}_{today.month:02d}.txt"
    with open(txt_name, "w", encoding="utf-8") as f:
        f.write("💗 MONTHLY GIRLYPOP WELLNESS REPORT 💗\n")
        f.write("="*70 + "\n\n")
        f.write(f"📅 Month: {today.strftime('%B %Y')}\n")
        f.write(f"📊 Days tracked: {report['days_logged']}\n")
        f.write(f"📈 Total wellness score: {report['total_score']}\n")
        f.write(f"⭐ Average daily score: {report['average_score']:.1f}/25\n\n")

        f.write("─" * 70 + "\n")
        f.write("MONTHLY METRICS BREAKDOWN:\n")
        f.write("─" * 70 + "\n\n")
        for k, v in averages.items():
            f.write(f"  • {k.capitalize()}: {v:.1f}\n")

        f.write("\n" + "─" * 70 + "\n")
        f.write("💡 PERSONALIZED ADVICE FOR THIS MONTH:\n")
        f.write("─" * 70 + "\n\n")
        for idx, adv in enumerate(advice, 1):
            f.write(f"{idx}. {adv}\n")

        f.write("\n" + "="*70 + "\n")
        f.write("🎯 SUMMARY:\n")
        if report['average_score'] >= 20:
            f.write("You had an EXCELLENT month! Your wellness habits are strong.\n")
            f.write("Keep maintaining these positive routines! 🌟\n")
        elif report['average_score'] >= 16:
            f.write("You had a GOOD month! You're taking care of yourself well.\n")
            f.write("Focus on areas that could use a little more attention. ✨\n")
        elif report['average_score'] >= 12:
            f.write("You had an OK month. There's room for improvement!\n")
            f.write("Start with one small change and build from there. 💪\n")
        else:
            f.write(
                "This month was challenging. Remember, progress over perfection!\n")
            f.write("Pick ONE area to focus on next month. You've got this! 💖\n")
        f.write("="*70 + "\n")

    print(f"\n✅ Reports saved!\n  📄 JSON: {json_name}\n  📋 TXT: {txt_name}")
    print(f"\n📋 Preview of {txt_name}:")
    with open(txt_name, "r", encoding="utf-8") as f:
        print(f.read())

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
