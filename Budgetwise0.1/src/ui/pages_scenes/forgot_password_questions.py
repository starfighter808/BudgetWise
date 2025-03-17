import flet as ft
from argon2 import PasswordHasher

class ForgotPasswordQuestions(ft.View):
    def __init__(self, page: ft.Page, user_repo, password_hasher):
        super().__init__(route="/forgot_password_questions", bgcolor="#5C9DFF")

        self.page = page
        self.user_repo = user_repo
        self.ph = password_hasher  

    
        self.error_text = ft.Text("", color=ft.Colors.RED, size=14)

        self.user_repo.temp_questions = self.user_repo.temp_questions or {}
        self.user_repo.temp_answers = self.user_repo.temp_answers or {}

        def get_dropdown_options():
            """Dynamically generates dropdown options from temp_questions."""
            return [
                ft.dropdown.Option(text=q, key=str(k))
                for k, q in self.user_repo.temp_questions.items() if q
            ]

        # Security Question Dropdown
        self.question_dropdown = ft.Dropdown(
            label="Select Security Question",
            options=get_dropdown_options(),
            value=None,  
            filled=True,
            width=400,
        )

        # Answer input field
        self.answer_field = ft.TextField(label="Enter your answer", password=True, width=400)

        # Continue button
        self.continue_button = ft.ElevatedButton(
            text="Continue",
            on_click=self.validate_security_answer,
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

        # Layout structure
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
                                            "Verify Security Question",
                                            text_align=ft.TextAlign.CENTER,
                                            size=24,
                                            weight=ft.FontWeight.BOLD,
                                            color=ft.Colors.WHITE,
                                        ),
                                        self.question_dropdown,
                                        self.answer_field,
                                        self.error_text,
                                        self.continue_button,
                                        ft.Row(
                                            controls=[
                                                ft.TextButton(
                                                    "Back to Forgot Password",
                                                    on_click=lambda e: self.page.go("/forgot_password"),
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
                                        ft.Icon(name=ft.Icons.QUESTION_ANSWER, color=ft.Colors.GREEN, size=200),
                                        ft.Text("BudgetWise", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                                        ft.Text("Security Verification", size=12, weight=ft.FontWeight.NORMAL, color=ft.Colors.WHITE),
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

    def validate_security_answer(self, e):
        """Verify the security answer using Argon2 hashing."""
        selected_key = self.question_dropdown.value 
        user_answer = self.answer_field.value.strip()

        if not selected_key or not user_answer:
            self.error_text.value = "Please select a question and enter an answer!"
            self.page.update()
            return

        correct_hashed_answer = self.user_repo.temp_answers.get(int(selected_key))  

        if not correct_hashed_answer:
            self.error_text.value = "Error: Could not find stored answer. Please try again."
            self.page.update()
            return

        try:
            self.ph.verify(correct_hashed_answer, user_answer)
            print("Security answer verified successfully!")
            self.page.go("/reset_password_success")

        except Exception:
            self.error_text.value = "Incorrect answer! Try again."
            self.page.update()
