import flet as ft

class Scene:
    def __init__(self, title, content):
        self.title = title
        self.content = content

    def get_content(self):
        return ft.Container(content=self.content, alignment=ft.alignment.center, expand=True)

class WelcomeScene(Scene):
    def __init__(self, change_scene_callback):
        self.change_scene_callback = change_scene_callback
        
        welcome_text = ft.Text("Welcome", size=100, color="grey", weight="bold")
        login_button = ft.ElevatedButton(
            text="Login", 
            on_click=lambda _: self.change_scene_callback(1)  # Assuming LoginScene is at index 4
        )
        signup_button = ft.ElevatedButton(
            text="Sign Up", 
            on_click=lambda _: print("Sign Up clicked")
        )

        centered_column = ft.Column(
            controls=[welcome_text, login_button, signup_button],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        )

        centered_container = ft.Container(
            content=centered_column,
            alignment=ft.alignment.center,
            expand=True
        )

        super().__init__("Welcome", centered_container)

class LoginScene(Scene):
    def __init__(self):
        # Create username and password fields
        Login_text = ft.Text("Log in", size=100, color="grey", weight="bold")
        username_field = ft.TextField(label="Username", width=300)
        password_field = ft.TextField(label="Password", password=True, can_reveal_password=True, width=300)
        login_button = ft.ElevatedButton(text="Login", on_click=lambda _: print("Login clicked"))

        # Create a column with the fields and button, aligned to the center
        login_column = ft.Column(
            controls=[Login_text, username_field, password_field, login_button],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        )

        # Wrap the column in a container and set alignment to center
        centered_container = ft.Container(
            content=login_column,
            alignment=ft.alignment.center,
            expand=True  # Make the container fill the available space
        )

        super().__init__("Login", centered_container)