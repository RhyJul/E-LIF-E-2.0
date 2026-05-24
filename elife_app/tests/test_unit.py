from elife_app.domain.models import DailyEntry
from elife_app.services.wellness_service import WellnessService
from datetime import date


# ============================================================================
# IMPORTANT: How to Run These Tests
# =========================================================================
# DO NOT run this file directly with Python, otherwise it will fail.
# This file uses pytest fixtures that only work through the pytest runner.
#
# Run from project root terminal:
#   pytest -v elife_app/tests/test_unit.py
#
# ============================================================================

# ======================== SERVICE SCORE TESTS ========================


def test_service_score():
    """
    Test wellness score calculation with good health metrics.

    Verifies that the service correctly calculates a score when
    user has balanced, healthy habits (no period data).
    """
    wellness = WellnessService()

    entry = DailyEntry(
        date=date(2025, 1, 2),
        sleep_quality=7,
        stress=3,
        friends=1,
        water_intake=3.0,
        exercise=1,
        mood=7,
        work_hours=8.0,
        hobbies=1,
        steps=10000,
        meds=1,
        period=0,
    )

    score, advice = wellness.calculate_score(entry)

    assert isinstance(score, int), "Score should be an integer"
    assert 40 <= score <= 70, "Good health should produce mid-range score"


# ======================== EDGE CASE TESTS ========================


def test_edge_case_all_zeros(sample_items):
    """
    Test wellness score with all minimum/zero values.

    Edge case: Verifies the service correctly handles extreme conditions
    when all health metrics are at their worst (no period data).
    """
    wellness = WellnessService()

    entry = DailyEntry(
        date=date(2025, 1, 1),
        sleep_quality=0,
        stress=10,
        friends=0,
        water_intake=0,
        exercise=0,
        mood=0,
        work_hours=0,
        hobbies=0,
        steps=0,
        meds=0,
        period=0,
    )

    score, advice = wellness.calculate_score(entry)

    assert score == 0, "All zeros should produce zero score"
    assert isinstance(score, int), "Score should be an integer"
    assert len(advice) > 0, "Worst health should generate advice"


def test_edge_case_all_perfect():
    """
    Test wellness score with all optimal values.

    Edge case: Verifies the service correctly calculates the highest
    possible score when all metrics are at maximum (no period data).
    """
    wellness = WellnessService()

    entry = DailyEntry(
        date=date(2025, 1, 15),
        sleep_quality=10,
        stress=0,
        friends=1,
        water_intake=5.0,
        exercise=1,
        mood=10,
        work_hours=8.0,
        hobbies=1,
        steps=20000,
        meds=1,
        period=0,
    )

    score, advice = wellness.calculate_score(entry)

    assert score >= 65, "Perfect health should produce high score"
    assert len(advice) > 0, "Service provides feedback/advice messages"


# ======================== INPUT VALIDATION TESTS ========================


def test_constraint_violations():
    """
    Test that entry fields properly reject data outside valid constraints.

    Verifies that the DailyEntry model validates ranges and raises
    errors for out-of-bounds health metrics.
    """
    from pydantic import ValidationError

    # Test sleep_quality constraint violation (max 10)
    try:
        invalid_entry = DailyEntry(
            date=date(2025, 1, 5),
            sleep_quality=11,  # Invalid: exceeds max of 10
            stress=5,
            friends=1,
            water_intake=2.5,
            exercise=1,
            mood=5,
            work_hours=8.0,
            hobbies=1,
            steps=10000,
            meds=1,
            period=0,
        )
        assert False, "Should have raised ValidationError for sleep_quality > 10"
    except ValidationError:
        pass  # Expected behavior

    # Test water_intake constraint violation (max 5)
    try:
        invalid_entry = DailyEntry(
            date=date(2025, 1, 5),
            sleep_quality=5,
            stress=5,
            friends=1,
            water_intake=5.5,  # Invalid: exceeds max of 5.0
            exercise=1,
            mood=5,
            work_hours=8.0,
            hobbies=1,
            steps=10000,
            meds=1,
            period=0,
        )
        assert False, "Should have raised ValidationError for water_intake > 5.0"
    except ValidationError:
        pass  # Expected behavior

    # Test steps constraint violation (max 50000)
    try:
        invalid_entry = DailyEntry(
            date=date(2025, 1, 5),
            sleep_quality=5,
            stress=5,
            friends=1,
            water_intake=2.5,
            exercise=1,
            mood=5,
            work_hours=8.0,
            hobbies=1,
            steps=50001,  # Invalid: exceeds max of 50000
            meds=1,
            period=0,
        )
        assert False, "Should have raised ValidationError for steps > 50000"
    except ValidationError:
        pass  # Expected behavior


# ======================== PERIOD TESTS ========================


def test_period_tracking():
    """
    Test that period pain and flow are tracked correctly.

    Verifies the service correctly records menstrual data
    (pain level, flow intensity) when user is on their period.
    """
    wellness = WellnessService()

    entry = DailyEntry(
        date=date(2025, 1, 10),
        sleep_quality=5,
        stress=6,
        friends=0,
        water_intake=2.5,
        exercise=0,
        mood=4,
        work_hours=6.0,
        hobbies=0,
        steps=4000,
        meds=1,
        period=1,
        period_pain=7,
        period_flow=2,
    )

    score, advice = wellness.calculate_score(entry)

    assert entry.period == 1, "Period status should be recorded"
    assert entry.period_pain == 7, "Period pain level should be recorded"
    assert entry.period_flow == 2, "Period flow should be recorded"
    assert isinstance(score, int), "Score should calculate with period data"


# ======================== REPORTING TESTS ========================


def test_advice_for_low_sleep():
    """
    Test that service provides appropriate advice for poor sleep quality.

    Verifies the service generates helpful feedback when sleep quality is low,
    even if other metrics are good.
    """
    wellness = WellnessService()

    entry = DailyEntry(
        date=date(2025, 1, 20),
        sleep_quality=2,       # Poor sleep
        stress=3,
        friends=1,
        water_intake=4.0,
        exercise=1,
        mood=6,
        work_hours=8.0,
        hobbies=1,
        steps=12000,
        meds=1,
        period=0,
    )

    score, advice = wellness.calculate_score(entry)

    # Check that advice is provided and mentions sleep-related guidance
    assert isinstance(advice, list), "Advice should be a list"
    assert len(advice) > 0, "Low sleep should generate advice"
    assert any("sleep" in str(msg).lower()
               for msg in advice), "Advice should mention sleep issues"
