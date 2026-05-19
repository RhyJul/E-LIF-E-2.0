from __future__ import annotations

from datetime import date, timedelta

from nicegui import app, ui

from elife_app.data_access.dao import EntryDAO
from elife_app.services.wellness_service import WellnessService


def create_monthly_report_page(entry_dao: EntryDAO) -> None:
    @ui.page('/monthly-report')
    def monthly_report_page() -> None:
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

        with ui.column().classes('w-full items-center gap-4 p-8'):
            ui.label(f'Monthly report for {username}').classes(
                'text-2xl font-bold')
            ui.button('Back to dashboard',
                      on_click=lambda: ui.navigate.to('/dashboard'))

            range_label = ui.label('')
            avg_label = ui.label('')
            entries_container = ui.column().classes('w-full gap-2')

            def format_advice_paragraphs(items: list[str], chunk_size: int = 3) -> str:
                if not items:
                    return "No recommendations for this entry."
                paragraphs = []
                for i in range(0, len(items), chunk_size):
                    chunk = items[i:i + chunk_size]
                    paragraphs.append(' '.join(chunk))
                return '\n\n'.join(paragraphs)

            def load_entries():
                entries = entry_dao.list_for_user(int(user_id))
                cutoff = date.today() - timedelta(days=27)
                filtered = [entry for entry in entries if entry.date >= cutoff]
                filtered.sort(key=lambda entry: entry.date)
                return filtered

            def refresh() -> None:
                entries_container.clear()
                entries = load_entries()

                if not entries:
                    range_label.set_text('No entries in the last 28 days.')
                    avg_label.set_text('')
                    return

                start_date = entries[0].date
                end_date = entries[-1].date
                range_label.set_text(
                f'Last 28 days ({start_date.strftime("%d.%m.%Y")} to {end_date.strftime("%d.%m.%Y")})'
                                )

                avg = sum(entry.score for entry in entries) / len(entries)
                avg_label.set_text(
                    f'Average score: {avg:.1f} across {len(entries)} entries'
                )

                for entry in entries:
                    stamp = (
                        entry.created_at.strftime('%Y-%m-%d %H:%M')
                        if entry.created_at
                        else 'unknown'
                    )
                    score, advice = WellnessService().calculate_score(entry)
                    header = (
                        f"Feedback for entry dated {entry.date.isoformat()} (logged {stamp})."
                    )
                    body = format_advice_paragraphs(advice)
                    with ui.card().classes('glass-card w-full'):
                        ui.label(f'Score: {score}').classes('text-sm')
                        ui.markdown(f"**{header}**\n\n{body}")

            ui.button('Refresh', on_click=refresh)
            refresh()


__all__ = ['create_monthly_report_page']
