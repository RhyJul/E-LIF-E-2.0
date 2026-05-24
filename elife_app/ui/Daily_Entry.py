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
        gender = app.storage.user.get('gender')
        is_female = gender == 'female'

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

                            # Date picker for editing the entry date
                            with ui.row().classes('gap-2 items-center'):
                                with ui.input(value=entry.date.strftime('%d.%m.%Y')) as edit_date_input:
                                    with ui.menu() as edit_menu:
                                        ui.date(on_change=lambda e: (edit_date_input.set_value(datetime.strptime(
                                            e.value, '%Y-%m-%d').strftime('%d.%m.%Y')), edit_menu.close()))
                                ui.icon('calendar_month').classes(
                                    'cursor-pointer').on('click', edit_menu.open)

                            sleep_edit = ui.slider(
                                min=0, max=10, value=entry.sleep_quality).props('label-always')
                            ui.label('Sleep quality (0-10)')

                            stress_edit = ui.slider(
                                min=0, max=10, value=entry.stress).props('label-always')
                            ui.label('Stress (0-10)')

                            mood_edit = ui.slider(
                                min=0, max=10, value=entry.mood).props('label-always')
                            ui.label('Mood (0-10)')

                            with ui.row().classes('w-full gap-4'):
                                water_edit = ui.number(label='Water intake (litres)', min=0, max=5, value=getattr(
                                    entry, 'water_intake', 0.0)).classes('w-full')
                                steps_edit = ui.number(
                                    label='Step count', min=0, max=50000, value=entry.steps).classes('w-full')
                                work_edit = ui.number(
                                    label='Work hours', min=0, max=16, value=entry.work_hours).classes('w-full')

                            with ui.row().classes('w-full gap-4 flex-wrap'):
                                friends_edit = ui.checkbox(
                                    'Did you see friends today?', value=bool(entry.friends))
                                exercise_edit = ui.checkbox(
                                    'Did you exercise today?', value=bool(entry.exercise))
                                hobbies_edit = ui.checkbox(
                                    'Did you do a hobby today?', value=bool(entry.hobbies))
                                meds_edit = ui.checkbox(
                                    'Did you take your meds today?', value=bool(entry.meds))
                                period_edit = None
                                period_pain_edit = None
                                period_flow_edit = None

                                if is_female:
                                    period_edit = ui.checkbox(
                                        'Are you on your period?', value=bool(entry.period))

                                    with ui.dialog() as period_edit_dialog:
                                        with ui.card().classes('w-96 text-slate-900 period-dialog'):
                                            ui.label('Period details').classes(
                                                'text-lg font-semibold text-slate-900')
                                            period_pain_edit = ui.slider(
                                                min=0, max=10, value=entry.period_pain or 5).props('label-always')
                                            ui.label('Pain level (0-10)')
                                            ui.label('Flow level (1=low, 2=medium, 3=strong)').classes(
                                                'text-slate-900')
                                            period_flow_edit = ui.select(
                                                [1, 2, 3], value=entry.period_flow or 2).classes('w-full text-slate-900')

                                            with ui.row().classes('w-full justify-end gap-2'):
                                                ui.button('Save', on_click=period_edit_dialog.close).classes(
                                                    'bg-emerald-600 hover:bg-emerald-700 text-white font-semibold')
                                                ui.button('Close', on_click=period_edit_dialog.close).classes(
                                                    'bg-emerald-600 hover:bg-emerald-700 text-white font-semibold')

                                    def on_period_edit_change() -> None:
                                        if period_edit.value:
                                            period_edit_dialog.open()

                                    period_edit.on(
                                        'update:model-value', lambda _: on_period_edit_change())

                            def save_edit() -> None:
                                # parse edited date
                                try:
                                    chosen = datetime.strptime(
                                        edit_date_input.value, "%d.%m.%Y").date()
                                except Exception:
                                    ui.notify(
                                        'Invalid date format, use DD.MM.YYYY', color='red')
                                    return

                                # check for existing entry on chosen date
                                with db.session_scope() as session:
                                    obj_check = session.get(DailyEntry, entry.id)
                                    if obj_check is None or obj_check.user_id != int(user_id):
                                        ui.notify('Entry not found for this user', color='red')
                                        return

                                    stmt = (
                                        select(DailyEntry)
                                        .where(DailyEntry.user_id == int(user_id))
                                        .where(DailyEntry.date == chosen)
                                    )
                                    existing = session.exec(stmt).first()

                                if existing and existing.id != entry.id:
                                    # ask user to confirm overwrite
                                    with ui.dialog() as confirm_dialog:
                                        ui.label('Another entry exists for that date. Overwrite it?')

                                        def do_overwrite() -> None:
                                            with db.session_scope() as s2:
                                                obj2 = s2.get(DailyEntry, entry.id)
                                                if obj2 is None or obj2.user_id != int(user_id):
                                                    ui.notify('Entry not found for this user', color='red')
                                                    return

                                                stmt2 = (
                                                    select(DailyEntry)
                                                    .where(DailyEntry.user_id == int(user_id))
                                                    .where(DailyEntry.date == chosen)
                                                )
                                                existing2 = s2.exec(stmt2).first()
                                                if existing2 and existing2.id != entry.id:
                                                    s2.delete(existing2)

                                                obj2.date = chosen
                                                obj2.sleep_quality = int(sleep_edit.value)
                                                obj2.stress = int(stress_edit.value)
                                                obj2.mood = int(mood_edit.value)
                                                obj2.steps = int(steps_edit.value)
                                                obj2.work_hours = float(work_edit.value)
                                                obj2.water_intake = float(water_edit.value)
                                                obj2.friends = int(bool(friends_edit.value))
                                                obj2.exercise = int(bool(exercise_edit.value))
                                                obj2.hobbies = int(bool(hobbies_edit.value))
                                                obj2.meds = int(bool(meds_edit.value))
                                                if is_female and period_edit is not None and period_edit.value:
                                                    obj2.period = 1
                                                    obj2.period_pain = int(period_pain_edit.value) if period_pain_edit is not None else None
                                                    obj2.period_flow = int(period_flow_edit.value) if period_flow_edit is not None else None
                                                else:
                                                    obj2.period = 0
                                                    obj2.period_pain = None
                                                    obj2.period_flow = None

                                                score, _ = wellness.calculate_score(obj2)
                                                obj2.score = score
                                                s2.add(obj2)

                                            confirm_dialog.close()
                                            card.remove()
                                            refresh()
                                            ui.notify('Saved — existing entry for that date was overwritten', type='positive')

                                        with ui.row().classes('w-full justify-end gap-2'):
                                            ui.button('Overwrite', on_click=do_overwrite).classes('bg-emerald-600 hover:bg-emerald-700 text-white font-semibold')
                                            ui.button('Cancel', on_click=confirm_dialog.close).classes('bg-emerald-600 hover:bg-emerald-700 text-white font-semibold')
                                    return

                                # no existing conflict — perform save
                                with db.session_scope() as session:
                                    obj = session.get(DailyEntry, entry.id)
                                    if obj is None or obj.user_id != int(user_id):
                                        ui.notify('Entry not found for this user', color='red')
                                        return

                                    obj.date = chosen
                                    obj.sleep_quality = int(sleep_edit.value)
                                    obj.stress = int(stress_edit.value)
                                    obj.mood = int(mood_edit.value)
                                    obj.steps = int(steps_edit.value)
                                    obj.work_hours = float(work_edit.value)
                                    obj.water_intake = float(water_edit.value)
                                    obj.friends = int(bool(friends_edit.value))
                                    obj.exercise = int(bool(exercise_edit.value))
                                    obj.hobbies = int(bool(hobbies_edit.value))
                                    obj.meds = int(bool(meds_edit.value))
                                    if is_female and period_edit is not None and period_edit.value:
                                        obj.period = 1
                                        obj.period_pain = int(period_pain_edit.value) if period_pain_edit is not None else None
                                        obj.period_flow = int(period_flow_edit.value) if period_flow_edit is not None else None
                                    else:
                                        obj.period = 0
                                        obj.period_pain = None
                                        obj.period_flow = None

                                    score, _ = wellness.calculate_score(obj)
                                    obj.score = score
                                    session.add(obj)

                                card.remove()
                                refresh()
                                ui.notify('Saved', type='positive')

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

            # Add new entry form (dashboard-style daily check-in)
            gender = app.storage.user.get('gender')
            is_female = gender == 'female'

            with ui.card().classes('bg-emerald-500/10 border border-emerald-500/30 backdrop-blur-sm rounded-lg text-slate-900 w-full'):
                with ui.expansion('Start daily check-in', icon='edit_note').classes('w-full'):
                    with ui.column().classes('gap-4'):
                        sleep = ui.slider(min=0, max=10, value=5).props(
                            'label-always')
                        ui.label('Sleep quality (0-10)')

                        stress = ui.slider(
                            min=0, max=10, value=5).props('label-always')
                        ui.label('Stress (0-10)')

                        mood = ui.slider(min=0, max=10, value=5).props(
                            'label-always')
                        ui.label('Mood (0-10)')

                        with ui.row().classes('w-full gap-4'):
                            water = ui.number(
                                label='Water intake (litres)', min=0, max=5, value=1.5).classes('w-full')
                            steps = ui.number(
                                label='Step count', min=0, max=50000, value=0).classes('w-full')
                            work_hours = ui.number(
                                label='Work hours', min=0, max=16, value=8).classes('w-full')

                        # Optional custom date for catch-up entries
                        set_date_cb = ui.checkbox('Set custom date (catch-up)')
                        with ui.row().classes('gap-2 items-center'):
                            with ui.input(placeholder='31.01.2026') as date_input:
                                date_input.visible = False
                                with ui.menu() as menu:
                                    ui.date(on_change=lambda e: (date_input.set_value(datetime.strptime(
                                        e.value, '%Y-%m-%d').strftime('%d.%m.%Y')), menu.close()))
                            ui.icon('calendar_month').classes(
                                'cursor-pointer').on('click', menu.open)

                        def toggle_date_visibility() -> None:
                            date_input.visible = bool(set_date_cb.value)

                        set_date_cb.on('update:model-value',
                                       lambda _: toggle_date_visibility())

                        with ui.row().classes('w-full gap-4 flex-wrap'):
                            friends = ui.checkbox('Did you see friends today?')
                            exercise = ui.checkbox('Did you exercise today?')
                            hobbies = ui.checkbox('Did you do a hobby today?')
                            meds = ui.checkbox('Did you take your meds today?')
                            period = None
                            period_pain_input = None
                            period_flow_input = None

                            if is_female:
                                period = ui.checkbox('Are you on your period?')

                                with ui.dialog() as period_dialog:
                                    with ui.card().classes('w-96 text-slate-900 period-dialog'):
                                        ui.label('Period details').classes(
                                            'text-lg font-semibold text-slate-900')
                                        period_pain_input = ui.slider(
                                            min=0, max=10, value=5).props('label-always')
                                        ui.label('Pain level (0-10)')
                                        ui.label('Flow level (1=low, 2=medium, 3=strong)').classes(
                                            'text-slate-900')
                                        period_flow_input = ui.select(
                                            [1, 2, 3], value=2).classes('w-full text-slate-900')

                                        with ui.row().classes('w-full justify-end gap-2'):
                                            ui.button('Save', on_click=period_dialog.close).classes(
                                                'bg-emerald-600 hover:bg-emerald-700 text-white font-semibold')
                                            ui.button('Close', on_click=period_dialog.close).classes(
                                                'bg-emerald-600 hover:bg-emerald-700 text-white font-semibold')

                                def on_period_change() -> None:
                                    if period.value:
                                        period_dialog.open()

                                period.on('update:model-value',
                                          lambda _: on_period_change())

                    result_label = ui.markdown('')

                    def submit_checkin() -> None:
                        period_value = 0
                        period_pain_value = None
                        period_flow_value = None

                        if is_female and period is not None and period.value:
                            period_value = 1
                            period_pain_value = int(period_pain_input.value)
                            period_flow_value = int(period_flow_input.value)

                        # choose date: custom (if set) or today
                        if set_date_cb.value:
                            try:
                                chosen_dt = datetime.strptime(
                                    date_input.value, "%d.%m.%Y").date()
                            except Exception:
                                ui.notify(
                                    'Invalid date format, use DD.MM.YYYY', color='red')
                                return
                        else:
                            chosen_dt = date.today()

                        entry = DailyEntry(
                            user_id=int(user_id),
                            date=chosen_dt,
                            sleep_quality=int(sleep.value),
                            stress=int(stress.value),
                            mood=int(mood.value),
                            water_intake=float(water.value),
                            steps=int(steps.value),
                            work_hours=float(work_hours.value),
                            friends=int(friends.value),
                            exercise=int(exercise.value),
                            hobbies=int(hobbies.value),
                            meds=int(meds.value),
                            period=period_value,
                            period_pain=period_pain_value,
                            period_flow=period_flow_value,
                        )

                        score, advice = wellness.calculate_score(entry)
                        entry.score = score

                        with db.session_scope() as session:
                            # prevent duplicate for today
                            stmt = (
                                select(DailyEntry)
                                .where(DailyEntry.user_id == int(user_id))
                                .where(DailyEntry.date == entry.date)
                            )
                            existing = session.exec(stmt).first()
                            if existing:
                                ui.notify(
                                    'Entry for today has already been submitted', type='warning')
                                return

                            session.add(entry)

                        stamp = entry.created_at.strftime(
                            '%d.%m.%Y %H:%M') if entry.created_at else 'unknown'
                        formatted = []
                        for tip in advice:
                            formatted.append(tip)

                        body = '\n\n'.join(formatted)
                        result_label.content = (
                            f"**Your wellness score: {score}**  \n" f"Logged at: {stamp}\n\n" f"{body}")

                        ui.notify('Check-in submitted successfully!',
                                  type='positive')
                        refresh()

                    ui.button('Submit check-in', on_click=submit_checkin).classes(
                        'px-4 py-2 rounded-full bg-emerald-600 hover:bg-emerald-700 text-white font-semibold')

            ui.separator()
            ui.label('Entries').classes('text-lg font-medium')
            avg_label
            ui.button('Refresh', on_click=refresh).classes(
                'bg-emerald-600 hover:bg-emerald-700 text-white font-semibold text-sm px-3 py-1')

            refresh()


__all__ = ['create_daily_entry_page']
