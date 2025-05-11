import flet as ft
from argon2.exceptions import VerifyMismatchError

class Login(ft.View):
    def __init__(self, page: ft.Page, user_data, colors):
        super().__init__(route="/login", bgcolor= colors.BLUE_BACKGROUND)

        self.page = page
        self.user_data = user_data  # User repository reference
        self.colors = colors

        # Input fields
        self.username_field = ft.TextField(
            label="Username", 
            label_style=ft.TextStyle(color=self.colors.BORDERBOX_COLOR), 
            text_style=ft.TextStyle(color=self.colors.TEXT_COLOR),
            hint_text="Enter your Username",
            hint_style=ft.TextStyle(color=self.colors.BLUE_BACKGROUND),
            focused_border_color=self.colors.BORDERBOX_COLOR,
            on_change=self.clear_error)
        self.password_field = ft.TextField(
            label="Password",
            label_style=ft.TextStyle(color=self.colors.BORDERBOX_COLOR), 
            text_style=ft.TextStyle(color=self.colors.TEXT_COLOR),
            hint_text="Enter your Password",
            hint_style=ft.TextStyle(color=self.colors.BLUE_BACKGROUND),
            focused_border_color=self.colors.BORDERBOX_COLOR,
            password=True, 
            can_reveal_password=True, 
            on_change=self.clear_error,
            on_submit=self.login_attempt  # Pressing Enter will trigger login
        )

        # Error message text
        self.error_text = ft.Text("", color=self.colors.ERROR_RED)

        # Login button
        self.login_button = ft.ElevatedButton(
            "Login",
            on_click=self.login_attempt,
            width=400,
            disabled=True,  # Initially disabled
            style=ft.ButtonStyle(
                color={ft.ControlState.DEFAULT: self.colors.TEXT_COLOR},
                bgcolor={ft.ControlState.DEFAULT: self.colors.GREEN_BUTTON},
                shape={ft.ControlState.DEFAULT: ft.RoundedRectangleBorder(radius=8)},
            ),
        )

        # Listen for input changes to enable/disable login button
        self.username_field.on_change = self.toggle_login_button
        self.password_field.on_change = self.toggle_login_button

        self.controls = [
            ft.Row(
                controls=[ 
                    ft.Container(
                        width=800,
                        height=450,
                        bgcolor=self.colors.GREY_BACKGROUND,
                        border_radius=10,
                        padding=20,
                        alignment=ft.alignment.center_right,
                        content=ft.Row(
                            controls=[
                                ft.Column(
                                    controls=[
                                        ft.Text("Welcome Back!", text_align=ft.TextAlign.CENTER, size=24, weight=ft.FontWeight.BOLD, color=self.colors.TEXT_COLOR),
                                        ft.Text("We're excited to see you again!", text_align=ft.TextAlign.CENTER, color=self.colors.TEXT_COLOR),
                                        self.username_field,
                                        self.password_field,
                                        self.error_text,
                                        ft.Row(
                                            controls=[
                                                ft.TextButton("Forgot your password?", style=ft.ButtonStyle(color=self.colors.TEXT_COLOR), on_click=lambda e: self.page.go("/username_verification")),
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
                                        ft.Icon(name=ft.Icons.SAVINGS_SHARP, color=self.colors.GREEN_BUTTON, size=200),
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

    def toggle_login_button(self, e):
        """Enable or disable the login button based on input fields."""
        self.login_button.disabled = not (self.username_field.value.strip() and self.password_field.value.strip())
        self.page.update()

    def clear_error(self, e):
        """Clear error message when the user starts typing."""
        if self.error_text.value:
            self.error_text.value = ""
            self.page.update()

    def login_attempt(self, e):
        """Handle login attempt."""
        username = self.username_field.value.strip()
        password = self.password_field.value.strip()

        if not self.user_data.is_valid_username(username) or not password:
            self.error_text.value = "Please enter both valid username and password."
        else:
            try:
                is_authenticated = self.user_data.verify_password(username, password)

                if is_authenticated is True:
                    self.user_data.user_id = self.user_data.get_user_id(username)
                    self.username_field.value = ""  
                    self.password_field.value = ""  
                    budget_details = self.user_data.get_budget_details()
                    
                    if budget_details is None:
                        print("No budget details found after login.")
                        self.page.go("/create_budget")
                        return

                    print("Login successful!")
                    self.error_text.value = ""
                    self.page.go("/dashboard")
                    return

                elif is_authenticated is None:
                    self.error_text.value = "User not found."
                else:
                    self.error_text.value = "Incorrect password."

            except Exception as err:
                print(f"Unexpected error during login: {err}")
                self.error_text.value = "Something went wrong. Please try again."

        self.page.update()


