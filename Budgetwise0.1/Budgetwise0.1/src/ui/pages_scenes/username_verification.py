import flet as ft
from src.ui.pages_scenes.forgot_password_questions import ForgotPasswordQuestions

class UsernameVerification(ft.View):
    def __init__(self, page: ft.Page, user_data, fpq_instance: ForgotPasswordQuestions):
        super().__init__(route="/username_verification", bgcolor="#5C9DFF")
        self.page = page
        self.user_data = user_data
        self.fpq_instance = fpq_instance  # Store instance for function calls

        # UI Components
        self.username_field = ft.TextField(label="Enter your username", width=400)
        self.error_text = ft.Text("", color=ft.Colors.RED, size=14)

        # Continue button
        self.continue_button = ft.ElevatedButton(
            text="Continue",
            on_click=self.validate_username,
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

        # Main layout
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
                                # Left column 
                                ft.Column(
                                    controls=[
                                        ft.Text(
                                            "Username Verification",
                                            text_align=ft.TextAlign.CENTER,
                                            size=24,
                                            weight=ft.FontWeight.BOLD,
                                            color=ft.Colors.WHITE,
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
                                        ft.Icon(name=ft.Icons.CONFIRMATION_NUM, color=ft.Colors.GREEN, size=200),
                                        ft.Text("Forgot Password?", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                                        ft.Text("Verify Username to start", size=12, weight=ft.FontWeight.NORMAL, color=ft.Colors.WHITE),
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
        if not username:
            self.error_text.value = "Username cannot be empty!"
            self.page.update()
            return

        # Check if user exists
        username_in_db = self.user_data.get_user_by_username(username)
        if not username_in_db:
            self.error_text.value = "Invalid username! Please try again."
            self.user_data.temp_username = {}  # Clear any temp data from failed validation
            self.page.update()
            return

        # Store username before fetching questions
        self.user_data.temp_username = {"username": username}

        # Fetch security questions 
        security_data = self.user_data.get_security_questions()

        # Ensure security questions were retrieved before navigating
        if not self.user_data.temp_questions:
            self.error_text.value = "Failed to retrieve security questions. Please try again."
            self.page.update()
            return

        # Update the ForgotPasswordQuestions instance correctly
        self.fpq_instance.on_page_load(username)  
        self.page.update()
        self.page.go("/forgot_password_questions")  
