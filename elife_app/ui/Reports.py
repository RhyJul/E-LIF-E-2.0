from nicegui import ui, app
from elife_app.data_access.dao import EntryDAO


def create_reports_page(entry_dao: EntryDAO) -> None:
    @ui.page('/reports')
    def reports_page() -> None:
        username = app.storage.user.get('username')

        if not username:
            ui.navigate.to('/')
            return

        with ui.column().classes('w-full max-w-lg mx-auto gap-6 p-8'):
            ui.label('📊 Your Reports').classes('text-2xl font-bold text-pink-500 text-center')

            entries = entry_dao.list_all()

            if not entries:
                ui.label('No entries yet! Go do your first check-in 💗').classes('text-center')
                ui.button('Back to Dashboard', on_click=lambda: ui.navigate.to('/dashboard'))
                return

            # Weekly summary
            with ui.card().classes('w-full p-6 shadow-lg rounded-xl bg-pink-50'):
                ui.label('Weekly Summary').classes('text-xl font-bold text-pink-400')
                last_7 = entries[-7:]
                avg = sum(e.score for e in last_7) / len(last_7)
                ui.label(f'📊 Average score (last 7 days): {avg:.1f}')
                best = max(last_7, key=lambda e: e.score)
                worst = min(last_7, key=lambda e: e.score)
                ui.label(f'🏆 Best day: {best.date} (score: {best.score})')
                ui.label(f'😔 Worst day: {worst.date} (score: {worst.score})')

            # Monthly summary
            with ui.card().classes('w-full p-6 shadow-lg rounded-xl bg-pink-50'):
                ui.label('Monthly Summary').classes('text-xl font-bold text-pink-400')
                last_30 = entries[-30:]
                avg_30 = sum(e.score for e in last_30) / len(last_30)
                ui.label(f'📊 Average score (last 30 days): {avg_30:.1f}')

            # Report history
            ui.label('Report History').classes('text-xl font-bold text-pink-400')
            for entry in reversed(entries):
                with ui.card().classes('w-full p-4 shadow rounded-xl'):
                    ui.label(f'📅 {entry.date}').classes('font-bold')
                    ui.label(f'💯 Score: {entry.score}')
                    ui.label(f'😴 Sleep: {entry.sleep_quality}/10')
                    ui.label(f'😰 Stress: {entry.stress}/10')
                    ui.label(f'😊 Mood: {entry.mood}/10')

            ui.button('Back to Dashboard', on_click=lambda: ui.navigate.to('/dashboard')).classes('w-full bg-pink-400 text-white mt-4')