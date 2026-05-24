from __future__ import annotations

from datetime import date

from nicegui import app, ui

from elife_app.data_access.dao import EntryDAO
from elife_app.services.wellness_service import WellnessService


def create_daily_report_page(entry_dao: EntryDAO,
                             wellness_service: WellnessService) -> None:
    """Register the /daily-report page showing today's score and advice."""
    @ui.page('/daily-report')
    def daily_report_page() -> None:
        user_id = app.storage.user.get('user_id')
        username = app.storage.user.get('username')

        if not user_id or not username:
            ui.navigate.to('/')
            return

        ui.add_head_html('''
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Source+Sans+3:wght@400;500;600&display=swap" rel="stylesheet">
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body {
            @apply bg-orange-200;
        }
    </style>
''')

        with ui.column().classes('w-full items-center gap-4 p-8 text-slate-900 min-h-screen'):
            ui.label(f'Daily report for {username}').classes(
                'font-display text-2xl font-bold text-emerald-700')
            ui.button('Back to dashboard', on_click=lambda: ui.navigate.to('/dashboard')).classes(
                'px-4 py-2 rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white font-semibold')

            date_label = ui.label('')
            timestamp_label = ui.label('')
            score_label = ui.label('')
            advice_container = ui.column().classes('w-full gap-2')

            def format_advice_paragraphs(
                    items: list[str],
                    chunk_size: int = 3) -> str:
                if not items:
                    return "No recommendations for today. Keep it up!"
                paragraphs = []
                for i in range(0, len(items), chunk_size):
                    chunk = items[i:i + chunk_size]
                    paragraphs.append(' '.join(chunk))
                return '\n\n'.join(paragraphs)

            def get_latest_entry():
                entries = entry_dao.list_for_user(int(user_id))
                if not entries:
                    return None, None

                today = date.today()
                for entry in entries:
                    if entry.date == today:
                        return entry, 'today'

                return entries[0], 'latest'

            def refresh() -> None:
                advice_container.clear()

                entry, label = get_latest_entry()
                if entry is None:
                    date_label.set_text(
                        'No entries yet. Add a daily entry first.')
                    timestamp_label.set_text('')
                    score_label.set_text('')
                    return

                score, advice = wellness_service.calculate_score(entry)
                score_label.set_text(f'Wellness score: {score}')

                if label == 'today':
                    date_label.set_text(
                        f'Report for today ({entry.date.strftime("%d.%m.%Y")})')
                else:
                    date_label.set_text(
                        f'Most recent entry ({entry.date.strftime("%d.%m.%Y")})')

                if entry.created_at:
                    stamp = entry.created_at.strftime('%d.%m.%Y %H:%M')
                else:
                    stamp = 'unknown'
                timestamp_label.set_text(f'Logged at: {stamp}')

                header = (
                    f"Feedback for entry dated {entry.date.strftime('%d.%m.%Y')} (logged {stamp})."
                )

                report_body = format_advice_paragraphs(advice)
                ui.markdown(f"**{header}**\n\n{report_body}")

            ui.button('Refresh', on_click=refresh).classes(
                'bg-emerald-600 hover:bg-emerald-700 text-white font-semibold')
            refresh()


__all__ = ['create_daily_report_page']
