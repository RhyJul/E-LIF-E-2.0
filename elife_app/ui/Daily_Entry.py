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
    """Register the /daily-entry page for managing past wellness entries."""
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
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body {
            @apply bg-orange-200;
        }
        .q-field__native, .q-field__label {
            color: #1f2937 !important;
        }
        .q-checkbox__label {
            color: #1f2937 !important;
        }
        .q-checkbox__inner {
            color: #10b981 !important;
        }
        .q-date__calendar-item button {
            color: #0f4c23 !important;
        }
        .q-date__header {
            color: #1f2937 !important;
        }
        .q-date__header * {
            color: #1f2937 !important;
        }
        .q-date__calendar-weekdays > div {
            color: #0f4c23 !important;
        }
        .q-date__navigation button {
            color: #0f4c23 !important;
        }
        .q-date__header-title, .q-date__header-subtitle {
            color: #1f2937 !important;
        }
    </style>
''')

        db = database or Database()
        db.init_schema()
        wellness = WellnessService()

        with ui.column().classes('w-full items-center gap-4 p-8 text-slate-900'):

            ui.button('Back to dashboard',
                      on_click=lambda: ui.navigate.to('/dashboard')).classes('bg-emerald-600 hover:bg-emerald-700 text-white font-semibold text-sm px-3 py-1')

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
                    with ui.card().classes('bg-emerald-500/10 border border-emerald-500/30 backdrop-blur-sm rounded-lg w-96') as card:
                        with ui.column():
                            ui.label('Edit entry').classes(
                                'text-lg font-medium')
                            d_input = ui.input(
                                label='Date', value=entry.date.strftime('%Y-%m-%d'))
                            sleep_input = ui.number(
                                label='Sleep quality', value=entry.sleep_quality)
                            stress_input = ui.number(
                                label='Stress', value=entry.stress)
                            mood_input = ui.number(
                                label='Mood', value=entry.mood)
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

                                card.remove()
                                refresh()

                            with ui.row():
                                ui.button('Save', on_click=save_edit).classes(
                                    'bg-emerald-600 hover:bg-emerald-700 text-white font-semibold text-sm px-3 py-1')
                                ui.button('Cancel', on_click=card.remove).classes(
                                    'bg-emerald-600 hover:bg-emerald-700 text-white font-semibold text-sm px-3 py-1')

                def delete_entry() -> None:
                    with db.session_scope() as session:
                        obj = session.get(DailyEntry, entry.id)
                        if obj and obj.user_id == int(user_id):
                            session.delete(obj)
                            session.commit()

                    refresh()

                with entries_container:
                    with ui.row().classes('items-center justify-between w-full py-2 px-4 border rounded'):
                        ui.label(
                            f'{entry.date.strftime("%d.%m.%Y")} — score: {entry.score} — logged: {format_stamp()}')
                        with ui.row():
                            ui.button('Edit', on_click=open_edit).classes(
                                'bg-emerald-600 hover:bg-emerald-700 text-white font-semibold text-sm px-3 py-1')
                            ui.button('Delete', on_click=delete_entry).classes(
                                'bg-emerald-600 hover:bg-emerald-700 text-white font-semibold text-sm px-3 py-1')

            # Add new entry form
            with ui.card().classes('bg-emerald-500/10 border border-emerald-500/30 backdrop-blur-sm rounded-lg text-slate-900 w-full'):
                ui.label('Add new daily entry').classes('text-lg font-medium')
                with ui.column().classes('gap-2'):
                    ui.label('Date (DD.MM.YYYY)').classes(
                        'text-sm font-medium')
                    with ui.row().classes("gap-4 items-center"):
                        with ui.input(placeholder='31.01.2026') as date_input:
                            with ui.menu() as menu:
                                ui.date(on_change=lambda e: (date_input.set_value(datetime.strptime(
                                    e.value, '%Y-%m-%d').strftime('%d.%m.%Y')), menu.close()))
                        ui.icon('calendar_month').classes(
                            'cursor-pointer').on('click', menu.open)
                    ui.label('Sleep quality').classes('text-sm font-medium')
                    sleep_input = ui.number(value=5)
                    ui.label('Stress').classes('text-sm font-medium')
                    stress_input = ui.number(value=5)
                    ui.label('Mood').classes('text-sm font-medium')
                    mood_input = ui.number(value=5)
                    ui.label('Steps').classes('text-sm font-medium')
                    steps_input = ui.number(value=0)
                    ui.label('Work hours').classes('text-sm font-medium')
                    work_input = ui.number(value=0.0)

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
                        # Check if entry for this date already exists
                        stmt = (
                            select(DailyEntry)
                            .where(DailyEntry.user_id == int(user_id))
                            .where(DailyEntry.date == d.date())
                        )
                        existing_entry = session.exec(stmt).first()

                        if existing_entry:
                            ui.notify(
                                'Entry for this date has already been submitted', type='warning')
                            return

                        session.add(entry)

                    ui.notify('Check-in submitted successfully!',
                              type='positive')
                    date_input.set_value('')
                    refresh()

                ui.button('Add entry', on_click=add_entry).classes(
                    'bg-emerald-600 hover:bg-emerald-700 text-white font-semibold text-sm px-3 py-1')

            ui.separator()
            ui.label('Entries').classes('text-lg font-medium')
            avg_label
            ui.button('Refresh', on_click=refresh).classes(
                'bg-emerald-600 hover:bg-emerald-700 text-white font-semibold text-sm px-3 py-1')

            refresh()


__all__ = ['create_daily_entry_page']
