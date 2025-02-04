import flet as ft
from BWForms import LoginScene, SignInScene

class Scene:
    def __init__(self, title, content):
        self.title = title
        self.content = content

    def get_content(self):
        return ft.Container(content=self.content, alignment=ft.alignment.center, expand=True)

class WelcomeScene(Scene):
    def __init__(self, change_scene_callback, show_login_form, show_signin_form):
        self.change_scene_callback = change_scene_callback
        self.show_login_form = show_login_form
        self.show_signin_form = show_signin_form

        welcome_text = ft.Text("Welcome", size=100, color="grey", weight="bold")
        login_button = ft.ElevatedButton(
            text="Login", 
            on_click=lambda _: self.show_login_form()
        )
        signup_button = ft.ElevatedButton(
            text="Sign Up", 
            on_click=lambda _: self.show_signin_form()
        )

        self.centered_column = ft.Column(
            controls=[welcome_text, login_button, signup_button],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        )

        centered_container = ft.Container(
            content=self.centered_column,
            alignment=ft.alignment.center,
            expand=True,
            padding=ft.Padding(0, 0, 0, 0),  # Adjusted padding
            margin=ft.Padding(0, 0, 0, 0)  # Adjusted margin
        )

        super().__init__("Welcome", centered_container)