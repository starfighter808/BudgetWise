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

class SignInScene(ft.AlertDialog):
    def __init__(self):
        # Create username and password fields
        signup_text = ft.Text("Sign-up", size=100, color="grey", weight="bold")
        self.username_field = ft.TextField(label="Username", width=300)
        self.password_field = ft.TextField(label="Password", password=True, can_reveal_password=True, width=300)
        self.confPassword_field = ft.TextField(label="Confirm Password", password=True, can_reveal_password=True, width=300)
        self.error_message = ft.Text("", color="red")

        signup_button = ft.ElevatedButton(text="Sign-up", on_click=self.validate_password)
        security_questions_button = ft.ElevatedButton(text="Security Questions", on_click=self.show_security_questions)

        # Create a column with the fields and button, aligned to the center
        login_column = ft.Column(
            controls=[signup_text, self.username_field, self.password_field, self.confPassword_field, self.error_message, signup_button, security_questions_button],
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

        super().__init__(content=centered_container)

        self.security_questions_dialog = SecurityQuestionsDialog()

    def validate_password(self, e):
        if self.password_field.value != self.confPassword_field.value:
            self.error_message.value = "Passwords do not match."
        else:
            self.error_message.value = "Sign-Up clicked."
            print("Sign-Up clicked")
        self.update()

    def show_security_questions(self, e):
        self.security_questions_dialog.open = True
        self.security_questions_dialog.update()

class SecurityQuestionsDialog(ft.AlertDialog):
    def __init__(self):
        self.questions = [
            "What is your mother's maiden name?",
            "What was your first pet's name?",
            "What is your favorite book?",
            "What is the name of your first school?",
            "What is your favorite movie?"
        ]

        self.question1 = ft.Dropdown(options=[ft.dropdown.Option(question) for question in self.questions])
        self.answer1 = ft.TextField(label="Answer 1", width=300)
        self.question2 = ft.Dropdown(options=[ft.dropdown.Option(question) for question in self.questions])
        self.answer2 = ft.TextField(label="Answer 2", width=300)
        self.question3 = ft.Dropdown(options=[ft.dropdown.Option(question) for question in self.questions])
        self.answer3 = ft.TextField(label="Answer 3", width=300)

        save_button = ft.ElevatedButton(text="Save", on_click=self.save_security_questions)

        questions_column = ft.Column(
            controls=[
                self.question1, self.answer1,
                self.question2, self.answer2,
                self.question3, self.answer3,
                save_button
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        )

        centered_container = ft.Container(
            content=questions_column,
            alignment=ft.alignment.center,
            bgcolor="#0d0d10",
            width=720,
            height=960,
            padding=20
        )

        super().__init__(content=centered_container)

    def save_security_questions(self, e):
        # Implement your save logic here
        print("Security questions saved")
        self.open = False
        self.update()