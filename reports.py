"""
reports.py - Report Generation Module
Generates weekly and monthly reports with analysis and advice
"""

import datetime
import json

FIELDS_NUMERIC = ["sleep", "stress", "friends", "water",
                  "exercise", "mood", "work_hours", "hobbies", "steps", "meds"]

WEEKLY_REPORT_FILE = "weekly_report.txt"


def generate_weekly_report(data):
    """
    Generate weekly status report from last 7 days of data.
    Returns formatted report string.
    """
    if not data or len(data) < 1:
        return "❌ Not enough data for weekly report"

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


def generate_monthly_advice(averages):
    """Generate personalized advice based on monthly metrics."""
    advice_list = []

    if averages.get("sleep", 0) < 2:
        advice_list.append(
            "💤 Your sleep quality seems low. Try to get to bed earlier.")
    elif averages.get("sleep", 0) >= 2.5:
        advice_list.append(
            "✨ Great sleep! Keep your consistent sleep schedule.")

    if averages.get("stress", 0) > 3.5:
        advice_list.append(
            "😌 High stress this month. Try taking short breaks or walks.")
    elif averages.get("stress", 0) <= 2:
        advice_list.append(
            "🌟 Your stress levels are great! Keep doing what you're doing.")

    if averages.get("exercise", 0) < 1.5:
        advice_list.append("🏃 You could move more! Try a 20-minute walk.")
    elif averages.get("exercise", 0) >= 1.8:
        advice_list.append(
            "💪 Awesome exercise habits! You're taking great care of yourself.")

    if averages.get("water", 0) < 1.5:
        advice_list.append("💧 Drink more water! Aim for 2-3 liters daily.")
    elif averages.get("water", 0) >= 2.5:
        advice_list.append("💙 Perfect hydration! You're doing amazing.")

    if averages.get("friends", 0) < 1.5:
        advice_list.append(
            "👯 Try connecting with friends more. Even a quick call helps!")
    elif averages.get("friends", 0) >= 1.8:
        advice_list.append(
            "🌈 Great social life! Keep nurturing those connections.")

    if averages.get("hobbies", 0) < 1.5:
        advice_list.append(
            "🎨 Make time for hobbies! Even 30 minutes makes a difference.")
    elif averages.get("hobbies", 0) >= 1.8:
        advice_list.append("🎭 Love seeing you take time for hobbies!")

    if averages.get("meds", 0) < 1.5:
        advice_list.append(
            "💊 Don't forget your daily routine! Set phone reminders.")
    elif averages.get("meds", 0) >= 1.8:
        advice_list.append("✅ Excellent consistency with your health routine!")

    if averages.get("steps", 0) < 1.5:
        advice_list.append(
            "👟 More movement needed! Park farther away or use stairs.")
    elif averages.get("steps", 0) >= 2.5:
        advice_list.append("🚶 Fantastic activity levels! Keep it up!")

    if averages.get("mood", 0) < 2:
        advice_list.append(
            "💖 Your mood could use a boost. Try something that \n"
            "makes you smile!")
    elif averages.get("mood", 0) >= 2.5:
        advice_list.append("😊 Your mood is great! You've got positive energy.")

    return advice_list


def save_monthly_report(data):
    """Generate and save comprehensive monthly report."""
    if not data:
        print("❌ No days logged this month 😭")
        return

    today = datetime.datetime.now()

    averages = {
        field: sum(d[field] for d in data) / len(data)
        for field in FIELDS_NUMERIC
    }

    report_data = {
        "month": today.month,
        "year": today.year,
        "days_logged": len(data),
        "total_score": sum(d["score"] for d in data),
        "average_score": sum(d["score"] for d in data) / len(data),
        "averages": averages
    }

    advice = generate_monthly_advice(averages)

    json_name = f"monthly_report_{today.year}_{today.month:02d}.json"
    with open(json_name, "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=4)

    txt_name = f"monthly_report_{today.year}_{today.month:02d}.txt"
    with open(txt_name, "w", encoding="utf-8") as f:
        f.write("💗 MONTHLY GIRLYPOP WELLNESS REPORT 💗\n")
        f.write("="*70 + "\n\n")
        f.write(f"📅 Month: {today.strftime('%B %Y')}\n")
        f.write(f"📊 Days tracked: {report_data['days_logged']}\n")
        f.write(f"📈 Total wellness score: {report_data['total_score']}\n")
        f.write(
            f"⭐ Average daily score: {report_data['average_score']:.1f}"
            f"/25\n\n"
        )

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
        if report_data['average_score'] >= 20:
            f.write("You had an EXCELLENT month! 🌟\n")
        elif report_data['average_score'] >= 16:
            f.write("You had a GOOD month! ✨\n")
        elif report_data['average_score'] >= 12:
            f.write("You had an OK month. Room for improvement! 💪\n")
        else:
            f.write("This month was challenging.\n"
                    "Progress over perfection! 💖\n")
        f.write("="*70 + "\n")

    print(f"\n✅ Reports saved!\n  📄 JSON: {json_name}\n  📋 TXT: {txt_name}")


if __name__ == "__main__":
    # Test module
    print("✅ reports.py loaded successfully")
    print("   Weekly and Monthly report functions available")
