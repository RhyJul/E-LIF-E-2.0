from elife_app.domain.models import DailyEntry
import sys
from pathlib import Path

# Add workspace root to path so absolute imports work
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


class WellnessService:
    """Calculates the wellness score and personalized advice from a daily entry."""

    def calculate_score(self, entry: DailyEntry) -> tuple[int, list[str]]:
        """Return the wellness score and a list of advice strings for the given entry."""
        score = (
            entry.sleep_quality +
            entry.mood +
            entry.friends * 10 +
            entry.exercise * 10 +
            entry.hobbies * 10 +
            entry.meds * 10 +
            min(entry.steps // 5000, 10) +
            min(int(entry.water_intake), 10)
        )

        advice = []

        if entry.stress >= 7:
            advice.append("💪 Lower your stress bestie!")
        if entry.friends == 0:
            advice.append("🌿 Touch grass with friends!")
        if entry.water_intake < 1.5:
            advice.append("💧 Hydrate queen!")
        if entry.exercise == 0:
            advice.append("🏃 Move your body!")
        if entry.mood <= 3:
            advice.append("💖 Your mood needs attention!")
        if entry.steps < 5000:
            advice.append("👟 Walk more!")
        if entry.hobbies == 0:
            advice.append("🎨 Do something fun!")
        if entry.meds == 0:
            advice.append("💊 Don't forget your meds!")

        # Daily review phrases by range.
        if entry.sleep_quality <= 3:
            advice.append(
                "Bestie, your sleep was not giving today. Let’s aim for an earlier bedtime and less scrolling tonight."
            )
        elif entry.sleep_quality <= 6:
            advice.append(
                "Okay, you slept… but we both know you can do better. A cozy routine would help."
            )
        else:
            advice.append(
                "Sleeping beauty behavior! Your body said thank you today.")

        if entry.mood <= 3:
            advice.append(
                "Your mood is a little low today, and that’s okay. Be gentle with yourself, queen."
            )
        elif entry.mood <= 6:
            advice.append(
                "Neutral mood energy. Not bad, not iconic. Do one tiny thing that makes you smile."
            )
        else:
            advice.append("Main character mood today! Keep that energy.")

        if entry.stress <= 3:
            advice.append("Low stress? Love that for you. Protect this peace.")
        elif entry.stress <= 6:
            advice.append(
                "Stress is trying to enter the chat. Take a little break before it gets dramatic."
            )
        else:
            advice.append(
                "Girl, your stress level is screaming. Pause, breathe, hydrate, and do not overbook yourself."
            )

        if entry.water_intake <= 1.0:
            advice.append(
                "Your water intake is giving cactus, but not in a cute way. Go drink some water."
            )
        elif entry.water_intake <= 2.0:
            advice.append(
                "Not terrible, but your water bottle deserves more attention.")
        elif entry.water_intake <= 3.5:
            advice.append(
                "Hydrated queen! Your skin, brain, and body are clapping.")
        else:
            advice.append(
                "Okay hydration superstar, just keep it balanced and listen to your body."
            )

        if entry.steps <= 3000:
            advice.append(
                "Your steps were a little shy today. A cute little walk could fix that."
            )
        elif entry.steps <= 7000:
            advice.append(
                "You moved, and we respect that. Tomorrow we level up.")
        elif entry.steps <= 12000:
            advice.append(
                "Look at you getting those steps in! Fitness girl era unlocked.")
        else:
            advice.append(
                "You were basically booked and busy on foot today. Rest those legs, queen."
            )

        if entry.work_hours <= 4:
            advice.append(
                "Light workday? Cute. Use the extra time for self-care, not doom-scrolling."
            )
        elif entry.work_hours <= 8:
            advice.append(
                "Balanced workday energy. Productive but not destroyed — we love.")
        elif entry.work_hours <= 12:
            advice.append(
                "You worked a lot today. Ambitious queen, but breaks are not optional."
            )
        else:
            advice.append(
                "Absolutely not, bestie. That is too much work energy. Recovery is required."
            )

        lifestyle_on = "Healthy habit completed! She is organized, disciplined, and glowing."
        lifestyle_off = "No healthy habit today? It happens. Tomorrow we make one tiny comeback."
        advice.append(
            f"Friends: {lifestyle_on if entry.friends else lifestyle_off}")
        advice.append(
            f"Exercise: {lifestyle_on if entry.exercise else lifestyle_off}")
        advice.append(
            f"Hobbies: {lifestyle_on if entry.hobbies else lifestyle_off}")
        advice.append(f"Meds: {lifestyle_on if entry.meds else lifestyle_off}")

        if entry.period_pain is not None:
            if entry.period_pain <= 3:
                advice.append(
                    "Period pain is low today. Finally, some peace in the uterus department."
                )
            elif entry.period_pain <= 6:
                advice.append(
                    "Cramps are being annoying. Heat pad, comfy clothes, and no unnecessary drama."
                )
            else:
                advice.append(
                    "Your cramps are doing way too much. Rest, be gentle, and get medical advice if this keeps happening."
                )

        if entry.period_flow is not None:
            if entry.period_flow == 1:
                advice.append(
                    "Light flow today. Manageable, cute, and not too chaotic.")
            elif entry.period_flow == 2:
                advice.append(
                    "Medium flow today. Stay prepared, stay comfy, stay iconic.")
            elif entry.period_flow == 3:
                advice.append(
                    "Strong flow today. Emergency chocolate, comfy pants, and extra care recommended."
                )

        entry.score = score
        return score, advice

    def weekly_report(self, entries):
        if not entries:
            return "No data."

        last_7 = entries[-7:]
        avg = sum(e.score for e in last_7) / len(last_7)

        return f"📊 Weekly Average Score: {avg:.1f}"
