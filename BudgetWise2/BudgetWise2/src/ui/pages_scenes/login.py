import flet as ft
from argon2.exceptions import VerifyMismatchError, Argon2Error

class Login(ft.View):
    def __init__(self, page: ft.Page, user_repo, password_hasher):
        super().__init__(route="/login", bgcolor="#5C9DFF")

        self.page = page
        self.user_repo = user_repo  # Reference to user repository
        self.ph = password_hasher  # Argon2 password hasher

        # Input fields
        self.username_field = ft.TextField(label="Username")
        self.password_field = ft.TextField(label="Password", password=True, can_reveal_password=True)

        # Error message text
        self.error_text = ft.Text("", color=ft.Colors.RED_400)

        # Login button
        self.login_button = ft.ElevatedButton(
            "Login",
            on_click=self.login_attempt,
            width=400,
            style=ft.ButtonStyle(
                color={
                    ft.ControlState.HOVERED: ft.Colors.WHITE,
                    ft.ControlState.FOCUSED: ft.Colors.GREEN_200,
                    ft.ControlState.DEFAULT: ft.Colors.WHITE,
                },
                bgcolor={
                    ft.ControlState.FOCUSED: ft.Colors.GREEN,
                    "": ft.Colors.GREEN,
                },
                padding=0,
                overlay_color=ft.Colors.TRANSPARENT,
                elevation={"pressed": 0, "": 0},
                animation_duration=0,
                side={
                    ft.ControlState.DEFAULT: ft.BorderSide(1, ft.Colors.GREEN),
                    ft.ControlState.HOVERED: ft.BorderSide(2, ft.Colors.GREEN),
                },
                shape={
                    ft.ControlState.HOVERED: ft.RoundedRectangleBorder(radius=20),
                    ft.ControlState.DEFAULT: ft.RoundedRectangleBorder(radius=8),
                },
            ),
        )

        self.controls = [
            ft.Row(
                controls=[ 
                    ft.Container(
                        width=800,
                        height=450,
                        bgcolor="#40444B",
                        border_radius=10,
                        padding=20,
                        alignment=ft.alignment.center_right,
                        content=ft.Row(
                            controls=[
                                ft.Column(
                                    controls=[
                                        ft.Text("Welcome Back!", text_align=ft.TextAlign.CENTER, size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                                        ft.Text("We're excited to see you again!", text_align=ft.TextAlign.CENTER, color=ft.Colors.WHITE),
                                        self.username_field,
                                        self.password_field,
                                        self.error_text,
                                        ft.Row(
                                            controls=[
                                                ft.TextButton("Forgot your password?", style=ft.ButtonStyle(color=ft.Colors.WHITE), on_click=lambda e: self.page.go("/username_verification")),
                                            ],
                                            alignment=ft.MainAxisAlignment.START,
                                            spacing=0,
                                        ),
                                        self.login_button,
                                        ft.Row(
                                            controls=[
                                                ft.TextButton("Need an account? Register", on_click=lambda e: self.page.go("/sign_up")),
                                            ],
                                            alignment=ft.MainAxisAlignment.START,
                                            spacing=0,
                                        ),
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    expand=True,
                                ),
                                # Second column 
                                ft.Column(
                                    controls=[
                                        ft.Icon(name=ft.Icons.SAVINGS_SHARP, color=ft.Colors.GREEN, size=200),
                                        ft.Text("BudgetWise", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                                        ft.Text("The Future of Budgeting", size=12, weight=ft.FontWeight.NORMAL, color=ft.Colors.WHITE),
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    expand=True,
                                )   
                            ],
                            expand=True,
                        ),
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True,
            ),
        ]

    def login_attempt(self, e):
        """Handle login attempt when the login button is clicked."""
        if not self.username_field.value.strip() or not  self.password_field.value.strip():
            self.error_text.value = "Please enter both username and password."
            self.page.update()
            return

        
        if self.verify_password(self.username_field.value.strip(), self.password_field.value.strip()) is True:
            print("Login successful!")
            self.page.go("/dashboard")  
        elif self.verify_password(self.username_field.value.strip(), self.password_field.value.strip()) is None:
            self.error_text.value = "User not found."
        else:
            self.error_text.value = "Incorrect password."

        self.page.update()


    def verify_password(self, provided_username, provided_password):
        """Verifies the user's password against the stored hash."""
        password_hash_from_db = self.user_repo.get_user_password_hash(provided_username)

        if password_hash_from_db is None:
            return None  

        try:
            return self.ph.verify(password_hash_from_db, provided_password) 
        except VerifyMismatchError:
            return False  
        except Argon2Error as e:
            print(f"Error verifying password: {e}")
            return False
