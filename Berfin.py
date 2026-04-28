import json
import os
import datetime


# =========================
# Daily Entry Class
# =========================
class DailyEntry:
    def __init__(self, date, sleep, stress, water, exercise, mood, steps):
        self.date = date
        self.sleep = sleep
        self.stress = stress
        self.water = water
        self.exercise = exercise
        self.mood = mood
        self.steps = steps
        self.score = 0

    def calculate_score(self):
        self.score = (
            self.sleep +
            self.water +
            self.exercise +
            self.mood +
            self.steps
        )

        if self.stress <= 2:
            self.score += 3
        elif self.stress == 3:
            self.score += 1

        return self.score

    def get_advice(self):
        advice = []

        if self.sleep == 1:
            advice.append("😴 Get better sleep.")
        if self.water == 1:
            advice.append("💧 Drink more water.")
        if self.exercise == 1:
            advice.append("🏃 Move your body.")
        if self.mood == 1:
            advice.append("💖 Take care of your mood.")
        if self.steps == 1:
            advice.append("👟 Walk more.")
        if self.stress >= 4:
            advice.append("🧘 Reduce stress.")

        return advice

    def to_dict(self):
        return {
            "date": self.date,
            "sleep": self.sleep,
            "stress": self.stress,
            "water": self.water,
            "exercise": self.exercise,
            "mood": self.mood,
            "steps": self.steps,
            "score": self.score
        }


# =========================
# Wellness Tracker Class
# =========================
class WellnessTracker:
    def __init__(self):
        self.file_name = "wellness_data.json"
        self.entries = []
        self.load_data()

    def add_entry(self, entry):
        self.entries.append(entry)

    def save_data(self):
        data = [entry.to_dict() for entry in self.entries]

        with open(self.file_name, "w") as file:
            json.dump(data, file, indent=4)

    def load_data(self):
        if os.path.exists(self.file_name):
            with open(self.file_name, "r") as file:
                data = json.load(file)

                for item in data:
                    entry = DailyEntry(
                        item["date"],
                        item["sleep"],
                        item["stress"],
                        item["water"],
                        item["exercise"],
                        item["mood"],
                        item["steps"]
                    )
                    entry.score = item["score"]
                    self.entries.append(entry)


# =========================
# Report Generator Class
# =========================
class ReportGenerator:
    @staticmethod
    def weekly_report(entries):
        if len(entries) == 0:
            print("No data available.")
            return

        last_7 = entries[-7:]

        average = sum(entry.score for entry in last_7) / len(last_7)

        print("\n📊 Weekly Report")
        print("-" * 30)
        print(f"Days tracked: {len(last_7)}")
        print(f"Average Score: {average:.1f}")

    @staticmethod
    def monthly_report(entries):
        if len(entries) == 0:
            print("No data available.")
            return

        average = sum(entry.score for entry in entries) / len(entries)

        print("\n📈 Monthly Report")
        print("-" * 30)
        print(f"Days tracked: {len(entries)}")
        print(f"Average Score: {average:.1f}")


# =========================
# Helper Functions
# =========================
def ask_number(prompt, min_val, max_val):
    while True:
        try:
            value = int(input(prompt))
            if min_val <= value <= max_val:
                return value
        except:
            pass

        print("Invalid input.")


def get_today():
    return datetime.datetime.now().strftime("%Y/%m/%d")


def create_daily_entry():
    print("\n🌟 Daily Check-In 🌟")

    date = get_today()

    sleep = ask_number("Sleep (1=bad, 2=medium, 3=good): ", 1, 3)
    stress = ask_number("Stress (1-5): ", 1, 5)
    water = ask_number("Water (1=low, 2=ok, 3=good): ", 1, 3)
    exercise = ask_number("Exercise (1=no, 2=yes): ", 1, 2)
    mood = ask_number("Mood (1=bad, 2=ok, 3=good): ", 1, 3)
    steps = ask_number("Steps (1=low, 2=ok, 3=high): ", 1, 3)

    entry = DailyEntry(
        date,
        sleep,
        stress,
        water,
        exercise,
        mood,
        steps
    )

    entry.calculate_score()

    return entry


def menu():
    print("\n💗 Wellness Tracker 💗")
    print("1. Add Daily Entry")
    print("2. Weekly Report")
    print("3. Monthly Report")
    print("4. Exit")

    return ask_number("Choose: ", 1, 4)


# =========================
# Main Program
# =========================
def main():
    tracker = WellnessTracker()

    while True:
        choice = menu()

        if choice == 1:
            entry = create_daily_entry()

            tracker.add_entry(entry)
            tracker.save_data()

            print(f"\n✅ Score: {entry.score}")

            advice = entry.get_advice()

            if advice:
                print("💡 Advice:")
                for item in advice:
                    print(item)

        elif choice == 2:
            ReportGenerator.weekly_report(tracker.entries)

        elif choice == 3:
            ReportGenerator.monthly_report(tracker.entries)

        elif choice == 4:
            print("Goodbye ✨")
            break


main()
