"""
test_wellness_score.py - Test wellness_score module
Run: python test_wellness_score.py
"""

from wellness_score import process_day

print("\n🧪 TESTING WELLNESS_SCORE MODULE\n")

# Test 1: Low score day
print("Test 1: Low score day (needs improvement)...")
low_day = {
    "sleep": 1, "stress": 5, "friends": 1, "water": 1,
    "exercise": 1, "mood": 1, "work_hours": 10,
    "hobbies": 1, "steps": 1, "meds": 1
}
result, advice = process_day(low_day)
print(f"✅ Score: {result['score']}")
print(f"   Advice items: {len(advice)}")
for a in advice[:3]:
    print(f"   - {a}")
expected_score = sum([1, 1, 1, 1, 1, 1, 1, 1]) + 0  # No stress bonus
assert result['score'] == expected_score, f"Expected"
f"{expected_score}, got {result['score']}"

# Test 2: High score day
print("\nTest 2: High score day (excellent)...")
high_day = {
    "sleep": 3, "stress": 1, "friends": 3, "water": 3,
    "exercise": 3, "mood": 3, "work_hours": 8,
    "hobbies": 3, "steps": 3, "meds": 3
}
result, advice = process_day(high_day)
print(f"✅ Score: {result['score']}")
print(f"   Advice items: {len(advice)}")
expected_score = sum([3, 3, 3, 3, 3, 3, 3, 3]) + 3  # Max stress bonus
assert result['score'] == expected_score, f"Expected"
f"{expected_score}, got {result['score']}"

# Test 3: Medium score day
print("\nTest 3: Medium score day (balanced)...")
medium_day = {
    "sleep": 2, "stress": 3, "friends": 2, "water": 2,
    "exercise": 2, "mood": 2, "work_hours": 8,
    "hobbies": 2, "steps": 2, "meds": 2
}
result, advice = process_day(medium_day)
print(f"✅ Score: {result['score']}")
print(f"   Advice items: {len(advice)}")
expected_score = sum([2, 2, 2, 2, 2, 2, 2, 2]) + 1  # Partial stress bonus
assert result['score'] == expected_score, f"Expected"
f"{expected_score}, got {result['score']}"

print("\n✅ wellness_score.py tests PASSED!\n")
