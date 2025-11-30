import csv
import random
import os


def e_life_tracker():
    """
    A simple E-lif(e) tracker that takes daily input and provides basic advice,
    enforcing valid input before moving to the next question.
    """
    print("--- E-lif(e) Daily Tracker Input ---")
    # Initialize a score
    score = 0
    advice = []
    # --- 1. Quality of Sleep (good, medium, bad) ---
    while True:
        sleep = input("Quality of sleep (good/medium/bad): ").lower().strip()
        if sleep == 'good':
            score += 3
            break
        elif sleep == 'medium':
            score += 1
            break
        elif sleep == 'bad':
            advice.append("Prioritize improving your sleep quality.")
            break
        else:
            print("❌ Invalid input. Please enter 'good', 'medium', or 'bad'.")
    # --- 2. Stress Level (1-5, lower is better) ---
    while True:
        try:
            stress_input = input("Stress level (1-5, where 1 is lowest): ")
            stress = int(stress_input)
            if 1 <= stress <= 2:
                score += 3
                break
            elif stress == 3:
                score += 1
                break
            elif 4 <= stress <= 5:
                advice.append(
                    "Look for ways to reduce your stress level today.")
                break
            else:
                print("❌ Input must be between 1 and 5.")
        except ValueError:
            print("❌ Invalid input. Please enter a whole number (1, 2, 3, 4, or 5).")

    # --- 3. Hung out with friends (yes/no) ---
    while True:
        friends = input("Hung out with friends (yes/no): ").lower().strip()
        if friends == 'yes':
            score += 2
            break
        elif friends == 'no':
            advice.append(
                "Social interaction can boost your mood. Reach out to someone soon.")
            break
        else:
            print("❌ Invalid input. Please enter 'yes' or 'no'.")
    # --- 4. Water Intake (in Liters) ---
    while True:
        try:
            water_input = input("Water intake (in Liters): ")
            water = float(water_input)
            if water > 1.5:
                score += 3
                break
            elif water >= 1.0:
                score += 1
                break
            elif water >= 0:  # Anything less than 1.0
                advice.append(
                    "Increase your water intake to at least 1-1.5 liters.")
                break
            else:
                print("❌ Input cannot be negative.")
        except ValueError:
            print("❌ Invalid input. Please enter a number (e.g., 1.5).")

    # --- 5. Exercise (yes/no) ---
    while True:
        exercise = input("Exercise (yes/no): ").lower().strip()
        if exercise == 'yes':
            score += 3
            break
        elif exercise == 'no':
            advice.append("Try to fit in some physical activity tomorrow.")
            break
        else:
            print("❌ Invalid input. Please enter 'yes' or 'no'.")

    # --- 6. Mood (relaxed, happy, etc.) ---
    valid_moods = ['relaxed', 'happy', 'angry',
                   'hyper', 'anxious', 'calm', 'irritable']
    while True:
        mood = input(
            "Mood (relaxed, happy, angry, hyper, anxious, calm, irritable): ").lower().strip()
        if mood in valid_moods:
            if mood in ['relaxed', 'happy', 'calm']:
                score += 2
            elif mood in ['angry', 'anxious', 'irritable']:
                advice.append(
                    f"Notice your '{mood}' mood. What might have contributed to it?")
            # 'hyper' adds no score/advice in this logic, but is valid
            break
        else:
            print(
                f"❌ Invalid input. Please enter one of the options: {', '.join(valid_moods)}.")

    # --- 7. Work/School (hours) ---
    while True:
        try:
            work_hours_input = input("Work/School (hours): ")
            work_hours = float(work_hours_input)
            if work_hours > 10:
                advice.append(
                    "You worked a long day. Ensure you're taking proper breaks.")
            # Allow any non-negative float/int input to proceed
            if work_hours >= 0:
                break
            else:
                print("❌ Work hours cannot be negative.")
        except ValueError:
            print("❌ Invalid input. Please enter a number (e.g., 8 or 4.5).")

    # --- 8. Hobbies (yes/no) ---
    while True:
        hobbies = input("Engaged in hobbies (yes/no): ").lower().strip()
        if hobbies == 'yes':
            score += 2
            break
        elif hobbies == 'no':
            advice.append(
                "Make time for a hobby; it's great for mental well-being.")
            break
        else:
            print("❌ Invalid input. Please enter 'yes' or 'no'.")
    # --- 9. Steps (number) ---
    while True:
        try:
            steps_input = input("Steps taken: ")
            steps = int(steps_input)
            if steps > 10000:
                score += 3
                break
            elif steps >= 4000:
                score += 2
                break
            elif steps >= 0:  # Less than 4000
                advice.append(
                    "Increase your steps, aim for at least 4,000 to 10,000.")
                break
            else:
                print("❌ Steps cannot be negative.")
        except ValueError:
            print("❌ Invalid input. Please enter a whole number.")
    # --- 10. Medication/Supplements (yes/no) ---
    while True:
        meds = input("Medication/Supplements taken (yes/no): ").lower().strip()
        if meds in ['yes', 'no']:
            break
        else:
            print("❌ Invalid input. Please enter 'yes' or 'no'.")

    # --- Weekly Status Report and Advice ---
    print("\n--- E-lif(e) Status Report ---")
    print(f"**Total Basic Wellness Score: {score}**")
    # Overall advice based on total score (very rough scale)
    if score >= 18:
        print("🎉 **Excellent Day!** Keep up this positive momentum; you're doing great across the board.")
    elif score >= 10:
        print("👍 **Good Day!** You've hit most of your key wellness goals, but there's room for small improvements.")
    else:
        print("⚠️ **Okay Day.** Review the specific advice below to see where you can focus your energy tomorrow.")
    # Specific advice
    if advice:
        print("\n**Specific Daily Tips:**")
        for tip in advice:
            print(f"- {tip}")
    else:
        print("\n**No specific issues detected.** You had a well-balanced day! 😊")


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


# -------------------------------------------------------------
# ✨ GIRLYPOP DAILY MESSAGE GENERATOR ✨
# -------------------------------------------------------------


def fun_girly_message(score):
    high = [
        "Hey girly, you're literally glowing. Keep doing whatever you're doing.",
        "Bestie, you ate this day UP. No crumbs were left.",
        "Queen behavior only. I’m so proud of you it’s annoying.",
        "Girl, your wellness routine? Pinterest would cry.",
        "Babes… you’re giving main character with her life together.",
        "Girly, today you were unstoppable. Soft life unlocked.",
        "Miss Ma’am, you're thriving harder than my houseplants."
    ]

    mid = [
        "Hey bestie, proud of you, but also… drink some water please.",
        "Girlypop, you did okay, but I know your potential is serving more.",
        "Cutie, you’re doing fine, but let's not get too comfy, mkay?",
        "You gave ‘responsible-ish’. We’ll take it.",
        "Bestie… mid but still cute.",
        "Girl, this was a soft attempt. Tomorrow we slay harder."
    ]

    low = [
        "Giiirl… get it together. This is not your best era.",
        "Bestie, blink twice if life is beating you up.",
        "Girly… what exactly were you doing today??",
        "Sweetie, the bar is on the floor and somehow you still tripped.",
        "Girl, be serious. I love you, but be serious.",
        "Bestie… your wellness score said ‘yikes.’",
        "Girlypop, we need a reboot. Control-alt-DELETE your habits immediately."
    ]

    if score >= 18:
        return random.choice(high)
    elif score >= 10:
        return random.choice(mid)
    else:
        return random.choice(low)

# -------------------------------------------------------------
# ✨ GIRLYPOP SUMMARY GENERATOR ✨
# -------------------------------------------------------------


def generate_daily_summaries_girly(inputs):
    summaries = {}

    summaries["sleep"] = {
        "input": inputs["sleep"],
        "summary": (
            "Sleep check, bestie: your rest sets the vibe for your whole day. "
            "Good sleep = glowing queen energy. Bad sleep = pls go to bed earlier."
        )
    }

    summaries["stress"] = {
        "input": inputs["stress"],
        "summary": (
            "Stress radar: calm girl era or full chaos gremlin mode? "
            "Low stress means soft life activated."
        )
    }

    summaries["friends"] = {
        "input": inputs["friends"],
        "summary": (
            "Did you see the girlies or hermit in your cave? Socializing = serotonin boost."
        )
    }

    summaries["water"] = {
        "input": inputs["water"],
        "summary": (
            "Hydration check: were you a wellness influencer or a dehydrated desert goblin?"
        )
    }

    summaries["exercise"] = {
        "input": inputs["exercise"],
        "summary": (
            "Movement moment: did you move like a hot girl, or were you in full cozy gremlin mode?"
        )
    }

    summaries["mood"] = {
        "input": inputs["mood"],
        "summary": (
            "Emotional vibes: happy/calm = thriving. Anxious/angry = bestie, breathe."
        )
    }

    summaries["work_hours"] = {
        "input": inputs["work_hours"],
        "summary": (
            "Capitalism report: did you grind too hard or achieve the soft-life work balance?"
        )
    }

    summaries["hobbies"] = {
        "input": inputs["hobbies"],
        "summary": (
            "Hobby era: did you romanticize your life today or forget you're fun?"
        )
    }

    summaries["steps"] = {
        "input": inputs["steps"],
        "summary": (
            "Step check: walking goddess or sleepy lil sloth?"
        )
    }

    summaries["meds"] = {
        "input": inputs["meds"],
        "summary": (
            "Did you take your potions, spells, tinctures, meds? Responsible queen hours."
        )
    }

    summaries["overall"] = (
        "Today's vibe is a mix of all your cute habits — some slayed, some fell down the stairs, "
        "but you're still THAT girl."
    )

    return summaries

# -------------------------------------------------------------
# ✨ MONTHLY REPORT GENERATOR ✨
# -------------------------------------------------------------


def generate_monthly_report_girly(month_data):
    total_days = len(month_data)

    if total_days == 0:
        return "Bestie… you logged NOTHING this month. And that’s very anti-Lana-Del-Rey-core of you."

    total_score = sum(day["score"] for day in month_data)
    avg_score = total_score / total_days

    # Count moods
    mood_counts = {}
    for day in month_data:
        mood = day["summaries"]["mood"]["input"]
        mood_counts[mood] = mood_counts.get(mood, 0) + 1

    most_common_mood = max(mood_counts, key=mood_counts.get)

    # Advice stats
    total_advice = sum(len(day["advice"]) for day in month_data)

    # Score vibe
    if avg_score >= 18:
        vibe = "✨Peak Soft-Life Princess Era✨"
    elif avg_score >= 10:
        vibe = "💖Mostly That Girl, but she forgets to hydrate 💖"
    else:
        vibe = "😩Survival Mode but with lip gloss 😩"

    # Build Report
    report = "\n💗💗💗 MONTHLY GIRLYPOP WELLNESS REPORT 💗💗💗\n"
    report += "----------------------------------------------------\n"

    report += f"\n📅 Days Logged: **{total_days}**"
    report += f"\n💅 Avg Wellness Score: **{avg_score:.1f}/24**"
    report += f"\n💖 Overall Vibe: **{vibe}**"
    report += f"\n🌈 Most Common Mood: **{most_common_mood.title()}**"
    report += f"\n📌 Total ‘Bestie Pls’ Advice Moments: **{total_advice}**"

    report += "\n\n✨ MONTHLY TEA ✨\n"

    if most_common_mood in ["happy", "relaxed", "calm"]:
        report += f"- Dominant mood was **{most_common_mood}**, meaning you were glowing, moisturized, and unbothered.\n"
    else:
        report += f"- Dominant mood was **{most_common_mood}**, which means drama followed you like a side quest.\n"

    if avg_score > 18:
        report += "- You lived like a wellness CEO. The girlies are taking notes.\n"
    elif avg_score > 10:
        report += "- A few ✨wobble✨ moments but overall? Still iconic.\n"
    else:
        report += "- Babe… you were in the trenches, but your spirit stayed sparkly.\n"

    if total_advice == 0:
        report += "- ZERO advice moments?? Bestie you're basically an NPC main character.\n"
    elif total_advice < total_days:
        report += "- A healthy sprinkle of advice moments. Balanced queen.\n"
    else:
        report += "- Collecting advice like Pokémon cards, I see. Character development era.\n"

    report += "\n💅✨ PROUD OF YOU ✨💅\nNext month is your reinvention arc.\n"

    return report

# -------------------------------------------------------------
# ✨ DAILY TRACKER ✨
# -------------------------------------------------------------


def e_life_tracker():
    print("--- E-lif(e) Daily Tracker Input ---")

    score = 0
    advice = []

    # 1. Sleep
    while True:
        sleep = input("Sleep (good/medium/bad): ").lower().strip()
        if sleep == 'good':
            score += 3
            break
        elif sleep == 'medium':
            score += 1
            break
        elif sleep == 'bad':
            advice.append("Fix your sleep queen, it's dragging your era.")
            break
        else:
            print("Bestie that isn't an option.")

    # 2. Stress
    while True:
        try:
            stress = int(input("Stress (1-5): "))
            if 1 <= stress <= 2:
                score += 3
                break
            elif stress == 3:
                score += 1
                break
            elif 4 <= stress <= 5:
                advice.append(
                    "Lower your stress babe, you're too pretty for headaches.")
                break
            else:
                print("Enter 1–5, my love.")
        except:
            print("Number please, sugarplum.")

    # 3. Friends
    while True:
        friends = input("Hung out with friends? (yes/no): ").lower().strip()
        if friends == 'yes':
            score += 2
            break
        elif friends == 'no':
            advice.append("Touch some grass with the girlies sometime.")
            break
        else:
            print("Yes or no, angel.")

    # 4. Water
    while True:
        try:
            water = float(input("Water (liters): "))
            if water > 1.5:
                score += 3
                break
            elif water >= 1:
                score += 1
                break
            else:
                advice.append("Hydrate or died-rate, princess.")
                break
        except:
            print("Number pls.")

 # 5. Exercise
    while True:
        exercise = input("Exercise? (yes/no): ").lower().strip()
        if exercise == 'yes':
            score += 3
            break
        elif exercise == 'no':
            advice.append("Move your body babe, it loves you.")
            break
        else:
            print("Yes/no bestie.")

    # 6. Mood
    valid = ['relaxed', 'happy', 'angry',
             'hyper', 'anxious', 'calm', 'irritable']
    while True:
        mood = input(f"Mood {valid}: ").lower().strip()
        if mood in valid:
            if mood in ['relaxed', 'happy', 'calm']:
                score += 2
            else:
                advice.append(
                    f"Your mood was '{mood}'. Let's unpack that later, bestie.")
            break
        else:
            print("Pick from the list babe.")

    # 7. Work
    while True:
        try:
            work_hours = float(input("Work hours: "))
            if work_hours > 10:
                advice.append("Girly you overworked again. Rest pls.")
            if work_hours >= 0:
                break
        except:
            print("Number.")

    # 8. Hobbies
    while True:
        hobbies = input("Hobbies today? (yes/no): ").lower().strip()
        if hobbies == 'yes':
            score += 2
            break
        elif hobbies == 'no':
            advice.append("Do something fun for once babe.")
            break
        else:
            print("Yes/no angel.")

    # 9. Steps
    while True:
        try:
            steps = int(input("Steps: "))
            if steps > 10000:
                score += 3
                break
            elif steps >= 4000:
                score += 2
                break
            else:
                advice.append("Walk a little more, hot girl cardio.")
                break
        except:
            print("Whole numbers only queen.")

    # 10. Meds
    while True:
        meds = input("Meds taken? (yes/no): ").lower().strip()
        if meds in ['yes', 'no']:
            break
        else:
            print("Yes/no bestie.")

    # Build summaries
    user_inputs = {
        "sleep": sleep,
        "stress": stress,
        "friends": friends,
        "water": water,
        "exercise": exercise,
        "mood": mood,
        "work_hours": work_hours,
        "hobbies": hobbies,
        "steps": steps,
        "meds": meds
    }

    summaries = generate_daily_summaries_girly(user_inputs)

    # DAILY REPORT
    print("\n--- DAILY GIRLYPOP REPORT ---")
    print(f"Score: {score}")
    print(fun_girly_message(score))

    if advice:
        print("\nToday's Bestie Advice:")
        for a in advice:
            print(f"- {a}")

    print("\n✨ Daily Summaries ✨")
    for category, data in summaries.items():
        if category == "overall":
            print(f"\nOVERALL: {data}")
        else:
            print(f"\n[{category.upper()}] Input: {data['input']}")
            print(f"Summary: {data['summary']}")

    return {
        "score": score,
        "advice": advice,
        "summaries": summaries
    }

# -------------------------------------------------------------
# ✨ MAIN LOOP FOR TRACKING MULTIPLE DAYS ✨
# -------------------------------------------------------------


def run_month():
    month_data = []

    print("💖 Welcome to your GirlyPop Wellness Tracker 💖")
    print("Enter daily data. Type 'done' anytime to finish the month.\n")

    while True:
        go = input("Track a new day? (yes/no): ").lower().strip()
        if go == "yes":
            day_record = e_life_tracker()
            month_data.append(day_record)
            print("\nDay logged, queen! 💅✨\n")
        elif go == "no":
            break
        else:
            print("Yes or no, sparkle princess.")

    print("\n--- MONTHLY REPORT ---")
    print(generate_monthly_report_girly(month_data))


# Run program
run_month()
