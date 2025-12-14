"""
wellness_score.py - Wellness Score Calculation Module
Calculates daily wellness score and generates personalized advice
"""


def process_day(day):
    """
    Calculate wellness score and generate personalized advice.
    Returns tuple of (processed_day, advice_list)
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


if __name__ == "__main__":
    # Test module
    print("✅ wellness_score.py loaded successfully")
    test_day = {
        "sleep": 2, "stress": 3, "friends": 1, "water": 3,
        "exercise": 1, "mood": 3, "work_hours": 8,
        "hobbies": 1, "steps": 2, "meds": 1
    }
    result, advice = process_day(test_day)
    print(f"   Test score: {result['score']}")
    print(f"   Advice count: {len(advice)}")
