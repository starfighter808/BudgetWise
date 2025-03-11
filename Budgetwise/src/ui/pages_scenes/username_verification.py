import flet as ft

class UsernameVerification(ft.View):
    def __init__(self, page: ft.Page, user_repo):
        super().__init__(route="/username_verification", bgcolor="#5C9DFF")
        self.page = page
        self.user_repo = user_repo

        self.username_field = ft.TextField(label="Enter your username", width=400)
        self.error_text = ft.Text("", color=ft.Colors.RED, size=14)

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

        # Main container layout
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
        Validate the entered username. If valid, store it in the user repository's temp_info,
        retrieve security questions, and navigate to the ForgotPasswordQuestions page.
        """
        username = self.username_field.value.strip()
        if not username:
            self.error_text.value = "Username cannot be empty!"
            self.page.update()
            return

        user_data = self.user_repo.get_user_by_username(username)
        if not user_data:
            self.error_text.value = "Invalid username! Please try again."
            self.user_repo.temp_info = {} 
            self.page.update()
            return

        self.user_repo.temp_info = {"username": user_data[0]}
        print("Stored username:", self.user_repo.temp_info["username"]) 

        security_data = self.user_repo.get_security_questions(self.user_repo.temp_info["username"])
        if not security_data:
            self.error_text.value = "No security questions found for this account."
            self.page.update()
            return

        self.page.go("/forgot_password_questions")
