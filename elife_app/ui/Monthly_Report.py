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
                    f'Last 28 days ({start_date.isoformat()} to {end_date.isoformat()})'
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
                    with ui.card().classes('w-full'):
                        ui.label(f'Score: {score}').classes('text-sm')
                        ui.markdown(f"**{header}**\n\n{body}")

            ui.button('Refresh', on_click=refresh)
            refresh()


__all__ = ['create_monthly_report_page']
