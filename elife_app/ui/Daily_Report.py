from __future__ import annotations

from datetime import date

from nicegui import app, ui

from elife_app.data_access.dao import EntryDAO
from elife_app.services.wellness_service import WellnessService


def create_daily_report_page(entry_dao: EntryDAO, wellness_service: WellnessService) -> None:
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
    <style>
        :root {
            --bg-start: #0f172a;
            --bg-end: #1f2937;
            --card: rgba(255, 255, 255, 0.08);
            --card-border: rgba(255, 255, 255, 0.18);
            --accent: #f59e0b;
            --text: #f8fafc;
            --muted: #cbd5f5;
        }
        body {
            font-family: 'Source Sans 3', sans-serif;
            background: radial-gradient(1200px 600px at 10% -10%, #1e3a8a33, transparent),
                        radial-gradient(1200px 700px at 90% 0%, #f59e0b22, transparent),
                        linear-gradient(120deg, var(--bg-start), var(--bg-end));
            color: var(--text);
        }
        .dashboard-title {
            font-family: 'Space Grotesk', sans-serif;
            letter-spacing: 0.3px;
        }
        .glass-card {
            background: var(--card);
            border: 1px solid var(--card-border);
            backdrop-filter: blur(10px);
            border-radius: 18px;
        }
        .pill-button .q-btn {
            border-radius: 999px;
        }
        .muted-text { color: var(--muted); }
    </style>
''')

        with ui.column().classes('w-full items-center gap-4 p-8 text-white'):
            ui.label(f'Daily report for {username}').classes(
                'text-2xl font-bold')
            ui.button('Back to dashboard',
                      on_click=lambda: ui.navigate.to('/dashboard'))

            date_label = ui.label('')
            timestamp_label = ui.label('')
            score_label = ui.label('')
            advice_container = ui.column().classes('w-full gap-2')

            def format_advice_paragraphs(items: list[str], chunk_size: int = 3) -> str:
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
                        f'Report for today ({entry.date.isoformat()})')
                else:
                    date_label.set_text(
                        f'Most recent entry ({entry.date.isoformat()})')

                if entry.created_at:
                    stamp = entry.created_at.strftime('%Y-%m-%d %H:%M')
                else:
                    stamp = 'unknown'
                timestamp_label.set_text(f'Logged at: {stamp}')

                report_header = (
                    f"Feedback for entry dated {entry.date.isoformat()}."
                )
                report_body = format_advice_paragraphs(advice)
                ui.markdown(f"**{report_header}**\n\n{report_body}")

            ui.button('Refresh', on_click=refresh)
            refresh()


__all__ = ['create_daily_report_page']
