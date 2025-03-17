import flet as ft
import re

class ResetPassword(ft.View):
    def __init__(self, page: ft.Page, user_repo, password_hasher):
        super().__init__(route="/sign_up", bgcolor="#5C9DFF")

        self.page = page
        self.user_repo = user_repo
        self.password_hasher = password_hasher
        
        # Input fields
        self.username = ft.TextField(label="Username")
        self.password = ft.TextField(label="Password", password=True, can_reveal_password=True)
        self.confirm_password = ft.TextField(label="Confirm Password", password=True, can_reveal_password=True)
        self.error_text = ft.Text("", color=ft.Colors.RED)

        # Continue Button
        self.continue_button = ft.ElevatedButton(
            "Continue",
            on_click=self.validate_and_continue,
            width=400,
            style=ft.ButtonStyle(
                color={ft.ControlState.DEFAULT: ft.Colors.WHITE},
                bgcolor={ft.ControlState.DEFAULT: ft.Colors.GREEN},
                padding={ft.ControlState.HOVERED: 20},
                overlay_color=ft.Colors.TRANSPARENT,
                elevation={"pressed": 0, "": 2},
                side={ft.ControlState.DEFAULT: ft.BorderSide(1, ft.Colors.GREEN)},
                shape={ft.ControlState.DEFAULT: ft.RoundedRectangleBorder(radius=8)},
            ),
        )

        self.controls = [
            ft.Row(
                controls=[ 
                    ft.Container(
                        width=800,
                        height=410,
                        bgcolor="#40444B",
                        border_radius=10,
                        padding=20,
                        alignment=ft.alignment.center_right,
                        content=ft.Row(
                            controls=[
                                # First column
                                ft.Column(
                                    controls=[
                                        ft.Text("Create an account", text_align=ft.TextAlign.CENTER, size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                                        self.username,
                                        self.password,
                                        self.confirm_password,
                                        self.error_text,
                                        self.continue_button,
                                        ft.Row(
                                            controls=[
                                                ft.TextButton("Already have an account?", on_click=lambda e: self.page.go("/login")),
                                            ],
                                            alignment=ft.MainAxisAlignment.START
                                        ),
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    expand=True,
                                ),
                                # Second column
                                ft.Column(
                                    controls=[
                                        ft.Icon(name=ft.Icons.LOCK_RESET, color=ft.Colors.GREEN, size=200),
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
    
    def validate_and_continue(self, e):
        """Validates inputs and moves to the next step if successful."""
        username = self.username.value.strip()
        password = self.password.value
        confirm_password = self.confirm_password.value

        if not username or not password or not confirm_password:
            self.error_text.value = "All fields are required!"
            self.page.update()
            return

        if not self.is_valid_password(password):
            self.error_text.value = "Password must be at least 8 characters long, include 1 uppercase letter, 1 lowercase letter, and 1 number."
            self.page.update()
            return

        if password != confirm_password:
            self.error_text.value = "Passwords do not match!"
            self.page.update()
            return

        self.user_repo.temp_info = {
            "username": username,
            "password_hash": self.ph.hash(password), 
        }

        self.page.go("/reset_password_success")

    def is_valid_password(self, password):
        """Checks if password meets the required complexity."""
        return bool(re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$', password))
