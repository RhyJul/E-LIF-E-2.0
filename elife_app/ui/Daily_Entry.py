from elife_app.services.wellness_service import WellnessService
from elife_app.domain.models import DailyEntry
from elife_app.data_access.db import Database
from sqlmodel import select
from nicegui import app, ui
from datetime import date
from datetime import date, datetime
from pathlib import Path
import sys

# make package imports work when this file is executed directly
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))


def create_daily_entry_page(database: Database | None = None) -> None:
    @ui.page('/daily-entry')
    def daily_entry_page() -> None:
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
        .q-field__native, .q-field__label {
            color: white !important;
        }
        .q-checkbox__label {
            color: white !important;
        }
        .q-checkbox__inner {
            color: #3b82f6 !important;
        }
        .q-date__calendar-item button {
            color: #0f172a !important;
        }
        .q-date__header {
            color: white !important;
        }
        .q-date__header * {
            color: white !important;
        }
        .q-date__calendar-weekdays > div {
            color: #0f172a !important;
        }
        .q-date__navigation button {
            color: #0f172a !important;
        }
        .q-date__header-title, .q-date__header-subtitle {
            color: white !important;
        }
    </style>
''')

        db = database or Database()
        db.init_schema()
        wellness = WellnessService()

        with ui.column().classes('w-full items-center gap-4 p-8 text-white'):
            
            ui.button('Back to dashboard',
                      on_click=lambda: ui.navigate.to('/dashboard'))

            entries_container = ui.column().classes('w-full gap-2')
            avg_label = ui.label('')

            def load_entries():
                with db.session_scope() as session:
                    stmt = (
                        select(DailyEntry)
                        .where(DailyEntry.user_id == int(user_id))
                        .order_by(DailyEntry.date.desc())
                    )
                    return session.exec(stmt).all()

            def refresh() -> None:
                entries = load_entries()
                entries_container.clear()

                for entry in entries:
                    create_entry_row(entry)

                if entries:
                    avg = sum(e.score for e in entries) / len(entries)
                    avg_label.set_text(f'Average score: {avg:.1f}')
                else:
                    avg_label.set_text('No data for this user yet.')

            def create_entry_row(entry: DailyEntry) -> None:
                def format_stamp() -> str:
                    if entry.created_at is None:
                        return 'unknown'
                    return entry.created_at.strftime('%d.%m.%Y %H:%M')

                def open_edit() -> None:
                    with ui.dialog().classes('w-1/2') as dlg:
                        ui.label('Edit entry').classes('text-lg font-medium')
                        d_input = ui.input(
                            label='Date', value=entry.date.isoformat())
                        sleep_input = ui.number(
                            label='Sleep quality', value=entry.sleep_quality)
                        stress_input = ui.number(
                            label='Stress', value=entry.stress)
                        mood_input = ui.number(label='Mood', value=entry.mood)
                        steps_input = ui.number(
                            label='Steps', value=entry.steps)
                        work_input = ui.number(
                            label='Work hours', value=entry.work_hours)

                        def save_edit() -> None:
                            try:
                                d = date.fromisoformat(d_input.value)
                            except ValueError:
                                ui.notify(
                                    'Invalid date format, use YYYY-MM-DD', color='red')
                                return

                            with db.session_scope() as session:
                                obj = session.get(DailyEntry, entry.id)
                                if obj is None or obj.user_id != int(user_id):
                                    ui.notify(
                                        'Entry not found for this user', color='red')
                                    return

                                obj.date = d
                                obj.sleep_quality = int(sleep_input.value)
                                obj.stress = int(stress_input.value)
                                obj.mood = int(mood_input.value)
                                obj.steps = int(steps_input.value)
                                obj.work_hours = float(work_input.value)
                                score, _ = wellness.calculate_score(obj)
                                obj.score = score
                                session.add(obj)

                            dlg.close()
                            refresh()

                        ui.button('Save', on_click=save_edit)
                        ui.button('Cancel', on_click=dlg.close)
                    dlg.open()

                def delete_entry() -> None:
                    with db.session_scope() as session:
                        obj = session.get(DailyEntry, entry.id)
                        if obj and obj.user_id == int(user_id):
                            session.delete(obj)

                    refresh()

                with ui.row().classes('items-center justify-between w-full py-2 px-4 border rounded'):
                    ui.label(
                        f'{entry.date.strftime("%d.%m.%Y")} — score: {entry.score} — logged: {format_stamp()}')
                    with ui.row():
                        ui.button('Edit', on_click=open_edit)
                        ui.button('Delete', on_click=delete_entry)

            # Add new entry form
            with ui.card().classes('glass-card text-white w-full'):
                ui.label('Add new daily entry').classes('text-lg font-medium')
                with ui.row().classes("gap-4 items-center"):
                    with ui.input(label='Date (DD.MM.YYYY)', placeholder='31.01.2026') as date_input:
                        with ui.menu() as menu:
                            ui.date(on_change=lambda e: (date_input.set_value(datetime.strptime(e.value, '%Y-%m-%d').strftime('%d.%m.%Y')), menu.close()))
                    ui.icon('calendar_month').classes('cursor-pointer').on('click', menu.open)
                sleep_input = ui.number(label='Sleep quality', value=5)
                stress_input = ui.number(label='Stress', value=5)
                mood_input = ui.number(label='Mood', value=5)
                steps_input = ui.number(label='Steps', value=0)
                work_input = ui.number(label='Work hours', value=0.0)

                def add_entry() -> None:
                    try:
                        d = datetime.strptime(date_input.value, "%d.%m.%Y")
                    except ValueError:
                        ui.notify(
                            'Invalid date format, use YYYY-MM-DD', color='red')
                        return

                    entry = DailyEntry(
                        user_id=int(user_id),
                        date=d,
                        sleep_quality=int(sleep_input.value),
                        stress=int(stress_input.value),
                        friends=0,
                        water_intake=0.0,
                        exercise=0,
                        mood=int(mood_input.value),
                        work_hours=float(work_input.value),
                        hobbies=0,
                        steps=int(steps_input.value),
                        meds=0,
                        period=0,
                    )

                    score, _ = wellness.calculate_score(entry)
                    entry.score = score

                    with db.session_scope() as session:
                        session.add(entry)

                    date_input.set_value('')
                    refresh()

                ui.button('Add entry', on_click=add_entry)

            ui.separator()
            ui.label('Entries').classes('text-lg font-medium')
            entries_container
            avg_label
            ui.button('Refresh', on_click=refresh)

            refresh()


__all__ = ['create_daily_entry_page']
