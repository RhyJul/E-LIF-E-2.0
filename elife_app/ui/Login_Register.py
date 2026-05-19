from nicegui import ui, app
from elife_app.domain.models import User


def create_login_page(user_dao) -> None:
    @ui.page('/')
    def login_page() -> None:
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
        .q-menu {
            background: #1f2937 !important;
            color: white !important;
        }
        .q-item__label {
            color: white !important;
        }
    </style>
''')
        with ui.column().classes('w-full h-screen items-center justify-center gap-4'):
            with ui.card().classes('glass-card text-white w-96 p-6 shadow-lg'):
                ui.label('Login').classes('text-2xl font-bold text-center')

                username_input = ui.input('Username').classes('w-full')
                password_input = ui.input(
                    'Password', password=True).classes('w-full')

                def login() -> None:
                    username = username_input.value
                    password = password_input.value

                    user = user_dao.login_user(username, password)

                    if user:
                        app.storage.user['user_id'] = user.id
                        app.storage.user['username'] = user.username
                        app.storage.user['gender'] = user.gender
                        ui.navigate.to('/dashboard')
                    else:
                        ui.notify('Wrong username or password',
                                  color='negative')

                ui.button('Login', on_click=login).classes('w-full')
                ui.button('Register', on_click=lambda: ui.navigate.to(
                    '/register')).classes('w-full')

    @ui.page('/register')
    def register_page() -> None:
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
        .q-menu {
            background: #1f2937 !important;
            color: white !important;
        }
        .q-item__label {
            color: white !important;
        }
    </style>
''')
        with ui.column().classes('w-full h-screen items-center justify-center gap-4'):
            with ui.card().classes('glass-card text-white w-96 p-6 shadow-lg'):
                ui.label('Register').classes('text-2xl font-bold text-center')

                username_input = ui.input('Username').classes('w-full')
                password_input = ui.input(
                    'Password', password=True).classes('w-full')
                gender_input = ui.select(
                    ['male', 'female'], label='Gender').classes('w-full')

                def register() -> None:
                    username = username_input.value
                    password = password_input.value
                    gender = gender_input.value

                    if not username or not password or gender not in ('male', 'female'):
                        ui.notify('Please fill all fields correctly',
                                  color='negative')
                        return

                    user = User(username=username,
                                password=password, gender=gender)
                    try:
                        user_dao.register_user(user)
                    except Exception as e:
                        ui.notify(
                            f'Error creating user: {e}', color='negative')
                        return

                    ui.notify('Account created!', color='positive')
                    ui.navigate.to('/')

                ui.button('Create account',
                          on_click=register).classes('w-full')
                ui.button('Back to login', on_click=lambda: ui.navigate.to(
                    '/')).classes('w-full')