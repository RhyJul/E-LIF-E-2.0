from elife_app.domain.models import DailyEntry


class WellnessService:

    def calculate_score(self, entry: DailyEntry) -> tuple[int, list[str]]:
        score = sum([
            entry.sleep, entry.friends, entry.water, entry.exercise,
            entry.mood, entry.steps, entry.hobbies, entry.meds
        ])

        advice = []

        if entry.stress <= 2:
            score += 3
        elif entry.stress == 3:
            score += 1
        else:
            advice.append("💪 Lower your stress bestie!")

        if entry.friends == 1:
            advice.append("🌿 Touch grass with friends!")
        if entry.water == 1:
            advice.append("💧 Hydrate queen!")
        if entry.exercise == 1:
            advice.append("🏃 Move your body!")
        if entry.mood == 1:
            advice.append("💖 Your mood needs attention!")
        if entry.steps == 1:
            advice.append("👟 Walk more!")
        if entry.hobbies == 1:
            advice.append("🎨 Do something fun!")
        if entry.meds == 1:
            advice.append("💊 Don't forget your meds!")

        entry.score = score
        return score, advice
