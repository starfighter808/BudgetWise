import flet as ft
from src.ui.pages_scenes.forgot_password_questions import ForgotPasswordQuestions

class UsernameVerification(ft.View):
    def __init__(self, page: ft.Page, user_data, colors):
        super().__init__(route="/username_verification", bgcolor= colors.BLUE_BACKGROUND)
        self.page = page
        self.user_data = user_data
        self.colors = colors

        # UI Components
        self.username_field = ft.TextField(
            label="Enter your username",
            label_style=ft.TextStyle(color=self.colors.BORDERBOX_COLOR), 
            text_style=ft.TextStyle(color=self.colors.TEXT_COLOR),
            hint_text="Enter your Username",
            hint_style=ft.TextStyle(color=self.colors.BLUE_BACKGROUND),
            focused_border_color=self.colors.BORDERBOX_COLOR, 
            width=400
            )
        self.error_text = ft.Text("", color=self.colors.ERROR_RED, size=14)

        # Continue button
        self.continue_button = ft.ElevatedButton(
            text="Continue",
            on_click=self.validate_username,
            width=400,
            style=ft.ButtonStyle(
                color={ft.ControlState.DEFAULT: self.colors.TEXT_COLOR},
                bgcolor={ft.ControlState.DEFAULT: self.colors.GREEN_BUTTON},
                padding={ft.ControlState.HOVERED: 20},
                overlay_color=self.colors.TRANSPARENT,
                elevation={"pressed": 0, "": 2},
                side={ft.ControlState.DEFAULT: ft.BorderSide(1, self.colors.GREEN_BUTTON)},
                shape={ft.ControlState.DEFAULT: ft.RoundedRectangleBorder(radius=8)},
            ),
        )

        # Main layout
        self.controls = [
            ft.Row(
                controls=[
                    ft.Container(
                        width=800,
                        height=410,
                        bgcolor= self.colors.GREY_BACKGROUND,
                        border_radius=10,
                        padding=20,
                        alignment=ft.alignment.center_right,
                        content=ft.Row(
                            controls=[
                                # Left column 
                                ft.Column(
                                    controls=[
                                        ft.Text(
                                            "Username Verification",
                                            text_align=ft.TextAlign.CENTER,
                                            size=24,
                                            weight=ft.FontWeight.BOLD,
                                            color=self.colors.TEXT_COLOR,
                                        ),
                                        self.username_field,
                                        self.error_text,
                                        self.continue_button,
                                        ft.Row(
                                            controls=[
                                                ft.TextButton(
                                                    "Back to Login?",
                                                    on_click=lambda e: self.page.go("/login"),
                                                ),
                                            ],
                                            alignment=ft.MainAxisAlignment.START,
                                        ),
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    expand=True,
                                ),
                                # Right column 
                                ft.Column(
                                    controls=[
                                        ft.Icon(name=ft.Icons.CONFIRMATION_NUM, color=self.colors.GREEN_BUTTON, size=200),
                                        ft.Text("Forgot Password?", size=24, weight=ft.FontWeight.BOLD, color=self.colors.TEXT_COLOR),
                                        ft.Text("Verify Username to start", size=12, weight=ft.FontWeight.NORMAL, color=self.colors.TEXT_COLOR),
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    expand=True,
                                ),
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

    def validate_username(self, e):
        """
        Validates the entered username. If valid, stores it in the user repository's temp_username,
        retrieves security questions, and navigates to the ForgotPasswordQuestions page.
        """
        username = self.username_field.value.strip()
        if not self.user_data.is_valid_username(username):
            self.error_text.value = "Username cannot be empty or invalid!"
            self.page.update()
            return

        # Check if user exists
        username_in_db = self.user_data.get_user_by_username(username)
        if not username_in_db:
            self.error_text.value = "Invalid username! Please try again."
            self.user_data.username = ""
            self.page.update()
            return

        # Store username before fetching questions
        self.user_data.username = username

        # Fetch security questions 
        security_data = self.user_data.get_security_questions()

        # Ensure security questions were retrieved before navigating
        if not self.user_data.temp_questions:
            self.error_text.value = "Failed to retrieve security questions. Please try again."
            self.page.update()
            return

        # Update the ForgotPasswordQuestions instance correctly
        self.username_field.value = ""
        self.page.update()
        self.page.go("/forgot_password_questions")  
