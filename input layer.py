# 🔄 E-lif(e) Tracker with Input Validation Loops

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


