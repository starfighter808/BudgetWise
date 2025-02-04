import flet as ft

class LoginScene(ft.AlertDialog):
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
            bgcolor="#0d0d10",  # Change the background color here
            width=720,  # Adjust the width
            height=960,  # Adjust the height
            padding=20  # Optional: Add padding inside the container
        )

        # Initialize the AlertDialog with the container as content
        super().__init__(content=centered_container)

def main(page: ft.Page):
    login_dialog = LoginScene()

    def open_login_dialog(e):
        login_dialog.open = True
        page.update()

    page.overlay.append(login_dialog)
    page.add(ft.ElevatedButton("Show Login", on_click=open_login_dialog))

ft.app(target=main)
