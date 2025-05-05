import flet as ft
import re

class SignUp(ft.View):
    def __init__(self, page: ft.Page, user_data, colors):
        super().__init__(route="/sign_up", bgcolor= colors.BLUE_BACKGROUND)

        self.page = page
        self.user_data = user_data
        self.colors = colors

        # Input fields
        self.username = ft.TextField(
            label="Username",
            label_style=ft.TextStyle(color=self.colors.BORDERBOX_COLOR), 
            text_style=ft.TextStyle(color=self.colors.TEXT_COLOR),
            hint_text="Enter your Username",
            hint_style=ft.TextStyle(color=self.colors.BLUE_BACKGROUND),
            focused_border_color=self.colors.BORDERBOX_COLOR, 
            on_change=self.clear_error)
        self.password = ft.TextField(
            label="Password",
            label_style=ft.TextStyle(color=self.colors.BORDERBOX_COLOR), 
            text_style=ft.TextStyle(color=self.colors.TEXT_COLOR),
            hint_text="Enter your Password",
            hint_style=ft.TextStyle(color=self.colors.BLUE_BACKGROUND),
            focused_border_color=self.colors.BORDERBOX_COLOR, 
            password=True, 
            can_reveal_password=True, 
            on_change=self.clear_error)
        self.confirm_password = ft.TextField(
            label="Confirm Password",
            label_style=ft.TextStyle(color=self.colors.BORDERBOX_COLOR), 
            text_style=ft.TextStyle(color=self.colors.TEXT_COLOR),
            hint_text="Confirm your Password",
            hint_style=ft.TextStyle(color=self.colors.BLUE_BACKGROUND),
            focused_border_color=self.colors.BORDERBOX_COLOR, 
            password=True, 
            can_reveal_password=True, 
            on_change=self.clear_error)

        # Error message text
        self.error_text = ft.Text("", color=self.colors.ERROR_RED)

        # Continue Button
        self.continue_button = ft.ElevatedButton(
            "Continue",
            on_click=self.validate_and_continue,
            width=400,
            disabled=True,  # Initially disabled
            style=ft.ButtonStyle(
                color={ft.ControlState.DEFAULT: self.colors.TEXT_COLOR},
                bgcolor={ft.ControlState.DEFAULT: self.colors.GREEN_BUTTON},
                shape={ft.ControlState.DEFAULT: ft.RoundedRectangleBorder(radius=8)},
            ),
        )

        # Enable/disable button when input changes
        self.username.on_change = self.toggle_continue_button
        self.password.on_change = self.toggle_continue_button
        self.confirm_password.on_change = self.toggle_continue_button

        self.controls = [
            ft.Row(
                controls=[ 
                    ft.Container(
                        width=820,
                        height=510,
                        bgcolor= self.colors.GREY_BACKGROUND,
                        border_radius=10,
                        padding=20,
                        alignment=ft.alignment.center_right,
                        content=ft.Row(
                            controls=[
                                # First column
                                ft.Column(
                                    controls=[
                                        ft.Text("Create an account", text_align=ft.TextAlign.CENTER, size=24, weight=ft.FontWeight.BOLD, color=self.colors.TEXT_COLOR),
                                        self.username,
                                        self.password,
                                        self.confirm_password,
                                        ft.Text("Password must have: Minimum 8 characters, 1 Upper Case, 1 Lower Case, 1 Number, and can have special characters", color=self.colors.TEXT_COLOR),
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
                                        ft.Icon(name=ft.Icons.ACCOUNT_BALANCE_WALLET_SHARP, color=self.colors.GREEN_BUTTON, size=200),
                                        ft.Text("BudgetWise", size=24, weight=ft.FontWeight.BOLD, color=self.colors.TEXT_COLOR),
                                        ft.Text("The Future of Budgeting", size=12, weight=ft.FontWeight.NORMAL, color=self.colors.TEXT_COLOR),
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

    def toggle_continue_button(self, e):
        """Enable or disable the continue button based on input fields."""
        self.continue_button.disabled = not (self.username.value.strip() and self.password.value.strip() and self.confirm_password.value.strip())
        self.page.update()

    def clear_error(self, e):
        """Clear error message when the user starts typing."""
        if self.error_text.value:
            self.error_text.value = ""
            self.page.update()

    def validate_and_continue(self, e):
        """Validates inputs and moves to the next step if successful."""
        username = self.username.value.strip()
        password = self.password.value.strip()
        confirm_password = self.confirm_password.value.strip()

        # Check if all fields are filled
        if not username or not password or not confirm_password:
            self.error_text.value = "All fields are required!"
            self.error_text.visible = True  # Ensure the error text is visible
            self.page.update()
            return

        # Validate username
        if not self.user_data.is_valid_username(username):
            self.error_text.value = "Username must be at least 3 characters and alphanumeric."
            self.error_text.visible = True
            self.page.update()
            return

        # Check if username is taken
        if self.user_data.username_exists(username):
            self.error_text.value = "Username is already taken. Please choose another."
            self.error_text.visible = True
            self.page.update()
            return

        # Validate password
        if not self.user_data.is_valid_password(password):
            self.error_text.value = (
                "Password must be at least 8 characters, include 1 uppercase, 1 lowercase, and 1 number."
            )
            self.error_text.visible = True
            self.page.update()
            return

        # Confirm passwords match
        if password != confirm_password:
            self.error_text.value = "Passwords do not match!"
            self.error_text.visible = True
            self.page.update()
            return

        # Store user info and proceed
        self.user_data.temp_sign_up_data = {
            "username": username,
            "password_hash": self.user_data.hash_password(password),
        }

        print("Sign-up step completed successfully")
        
        # Hide error text if it was previously shown
        self.error_text.visible = False
        self.page.update()
        
        # Navigate to the next step
        self.username.value = ""
        self.password.value = ""
        self.confirm_password.value = ""	
        self.page.go("/security_questions")




