from nicegui import ui, app
from datetime import date
from elife_app.domain.models import DailyEntry
from elife_app.services.wellness_service import WellnessService


def create_dashboard_page(entry_dao, wellness_service: WellnessService) -> None:
    @ui.page('/dashboard')
    def dashboard_page() -> None:
        user_id = app.storage.user.get('user_id')
        username = app.storage.user.get('username')
        gender = app.storage.user.get('gender')
        is_female = gender == 'female'

        if not user_id or not username:
            ui.navigate.to('/')
            return

        def logout() -> None:
            app.storage.user.clear()
            ui.navigate.to('/')

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

        with ui.column().classes('w-full items-center gap-6 p-6 md:p-10 text-slate-900 min-h-screen'):
            with ui.row().classes('w-full max-w-6xl items-center justify-between gap-4'):
                with ui.column().classes('gap-2'):
                    ui.label(f'Welcome back, {username}!').classes(
                        'font-display text-3xl md:text-4xl font-bold text-emerald-700')
                    ui.label('Pick an action below or start a new check-in.').classes(
                        'text-emerald-800')
                ui.button('Logout', on_click=logout).classes(
                    'px-6 py-2 rounded-full bg-emerald-600 hover:bg-emerald-700 text-white font-semibold')

            with ui.row().classes('w-full max-w-6xl gap-4 md:gap-6'):
                with ui.card().classes('bg-emerald-500/10 border border-emerald-500/30 backdrop-blur-sm rounded-lg w-full md:w-1/3 p-5 gap-3'):
                    ui.label('Manage Entries').classes(
                        'text-xl font-semibold text-emerald-700')
                    ui.label(
                        'Edit, delete, or review previous check-ins.').classes('text-emerald-800')
                    ui.button('Open entries', on_click=lambda: ui.navigate.to('/daily-entry')).classes(
                        'px-4 py-2 rounded-full bg-emerald-600 hover:bg-emerald-700 text-white font-semibold')

                with ui.card().classes('bg-emerald-500/10 border border-emerald-500/30 backdrop-blur-sm rounded-lg w-full md:w-1/3 p-5 gap-3'):
                    ui.label('Daily Report').classes(
                        'text-xl font-semibold text-emerald-700')
                    ui.label('See today\'s score and recommendations.').classes(
                        'text-emerald-800')
                    ui.button('View report', on_click=lambda: ui.navigate.to('/daily-report')).classes(
                        'px-4 py-2 rounded-full bg-emerald-600 hover:bg-emerald-700 text-white font-semibold')

                with ui.card().classes('bg-emerald-500/10 border border-emerald-500/30 backdrop-blur-sm rounded-lg w-full md:w-1/3 p-5 gap-3'):
                    ui.label('Monthly Report').classes(
                        'text-xl font-semibold text-emerald-700')
                    ui.label('Review the last 28 days at a glance.').classes(
                        'text-emerald-800')
                    ui.button('View monthly', on_click=lambda: ui.navigate.to('/monthly-report')).classes(
                        'px-4 py-2 rounded-full bg-emerald-600 hover:bg-emerald-700 text-white font-semibold')

            with ui.card().classes('bg-emerald-500/10 border border-emerald-500/30 backdrop-blur-sm rounded-lg w-full max-w-6xl p-6'):
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
                            water = ui.number(label='Water intake (litres)',
                                              min=0, max=5, value=1.5).classes('w-full')
                            steps = ui.number(label='Step count', min=0,
                                              max=50000, value=0).classes('w-full')
                            work_hours = ui.number(label='Work hours', min=0,
                                                   max=16, value=8).classes('w-full')

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
                                        ui.label(
                                            'Flow level (1=low, 2=medium, 3=strong)'
                                        ).classes('text-slate-900')
                                        period_flow_input = ui.select(
                                            [1, 2, 3],
                                            value=2,
                                        ).classes('w-full text-slate-900')

                                        with ui.row().classes('w-full justify-end gap-2'):
                                            ui.button(
                                                'Save', on_click=period_dialog.close).classes('bg-emerald-600 hover:bg-emerald-700 text-white font-semibold')
                                            ui.button(
                                                'Close', on_click=period_dialog.close).classes('bg-emerald-600 hover:bg-emerald-700 text-white font-semibold')

                                def on_period_change() -> None:
                                    if period.value:
                                        period_dialog.open()

                                period.on('update:model-value',
                                          lambda _: on_period_change())

                        result_label = ui.markdown('')

                        def format_tip(tip: str) -> str:
                            if ':' in tip:
                                label, rest = tip.split(':', 1)
                                if label in {'Friends', 'Exercise', 'Hobbies', 'Meds'}:
                                    return f"**{label}:** {rest.strip()}"
                            if tip.startswith('Hydrated queen!'):
                                return f"**Hydrated queen!**{tip[len('Hydrated queen!'):]}"
                            return tip

                        def submit():
                            period_value = 0
                            period_pain_value = None
                            period_flow_value = None

                            if is_female and period is not None and period.value:
                                period_value = 1
                                period_pain_value = int(
                                    period_pain_input.value)
                                period_flow_value = int(
                                    period_flow_input.value)

                            entry = DailyEntry(
                                user_id=int(user_id),
                                date=date.today(),
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
                            score, advice = wellness_service.calculate_score(
                                entry)
                            entry.score = score
                            created_entry = entry_dao.create(entry)
                            stamp = (
                                entry.created_at.strftime('%d.%m.%Y %H:%M')
                                if entry.created_at
                                else 'unknown'
                            )

                            formatted = [format_tip(tip) for tip in advice]
                            body = '\n\n'.join(formatted)
                            result_label.content = (
                                f"**Your wellness score: {score}**  \n"
                                f"Logged at: {stamp}\n\n"
                                f"{body}"
                            )

                        ui.button('Submit check-in', on_click=submit).classes(
                            'px-4 py-2 rounded-full bg-emerald-600 hover:bg-emerald-700 text-white font-semibold')
