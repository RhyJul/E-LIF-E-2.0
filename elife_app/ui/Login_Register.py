from nicegui import ui, app
from elife_app.domain.models import User


def create_login_page(user_dao) -> None:
    """Register the /login and /register pages with NiceGUI."""

    @ui.page("/")
    def login_page() -> None:
        from elife_app.ui.head_html import inject_head_html

        inject_head_html()
        with ui.column().classes(
            "w-full h-screen items-center justify-center gap-4 text-slate-900"
        ):
            with ui.card().classes(
                "bg-emerald-500/10 border border-emerald-500/30 backdrop-blur-sm rounded-lg w-96 p-6 shadow-lg text-slate-900"
            ):
                ui.label("Login").classes(
                    "text-2xl font-bold text-center text-emerald-700"
                )

                username_input = ui.input("Username").classes("w-full text-center py-3")
                password_input = ui.input("Password", password=True).classes(
                    "w-full text-center py-3"
                )

                def login() -> None:
                    username = username_input.value
                    password = password_input.value

                    user = user_dao.login_user(username, password)

                    if user:
                        app.storage.user["user_id"] = user.id
                        app.storage.user["username"] = user.username
                        app.storage.user["gender"] = user.gender
                        ui.navigate.to("/dashboard")
                    else:
                        ui.notify("Wrong username or password", color="negative")

                ui.button("Login", on_click=login).classes(
                    "w-full bg-emerald-600 hover:bg-emerald-700 text-white font-semibold"
                )
                ui.button(
                    "Register", on_click=lambda: ui.navigate.to("/register")
                ).classes(
                    "w-full bg-emerald-600 hover:bg-emerald-700 text-white font-semibold"
                )

    @ui.page("/register")
    def register_page() -> None:
        from elife_app.ui.head_html import inject_head_html

        inject_head_html()
        with ui.column().classes(
            "w-full h-screen items-center justify-center gap-4 text-slate-900"
        ):
            with ui.card().classes(
                "bg-emerald-500/10 border border-emerald-500/30 backdrop-blur-sm rounded-lg w-96 p-6 shadow-lg text-slate-900"
            ):
                ui.label("Register").classes(
                    "text-2xl font-bold text-center text-emerald-700"
                )

                username_input = ui.input("Username").classes("w-full text-center py-3")
                password_input = ui.input("Password", password=True).classes(
                    "w-full text-center py-3"
                )
                gender_input = ui.select(["male", "female"], label="Gender").classes(
                    "w-full text-center py-3"
                )

                def register() -> None:
                    username = username_input.value
                    password = password_input.value
                    gender = gender_input.value

                    if not username or not password or gender not in ("male", "female"):
                        ui.notify("Please fill all fields correctly", color="negative")
                        return

                    user = User(username=username, password=password, gender=gender)
                    try:
                        user_dao.register_user(user)
                    except Exception as e:
                        ui.notify(f"Error creating user: {e}", color="negative")
                        return

                    ui.notify("Account created!", color="positive")
                    ui.navigate.to("/")

                ui.button("Create account", on_click=register).classes(
                    "w-full bg-emerald-600 hover:bg-emerald-700 text-white font-semibold"
                )
                ui.button(
                    "Back to login", on_click=lambda: ui.navigate.to("/")
                ).classes(
                    "w-full bg-emerald-600 hover:bg-emerald-700 text-white font-semibold"
                )
