import flet as ft

class ForgotPasswordQuestions(ft.View):
    def __init__(self, page: ft.Page, user_data):
        super().__init__(route="/forgot_password_questions", bgcolor="#5C9DFF")
        self.page = page
        self.user_data = user_data
        self.username = None  # Stores username after navigation

        # Error message
        self.error_text = ft.Text("", color=ft.Colors.RED, size=14)

        # Dropdown for selecting security question
        self.question_dropdown = ft.Dropdown(
            label="Select Security Question",
            options=[],  # Will be populated dynamically
            value=None,
            filled=True,
            width=500,
            on_change=self.toggle_continue_button,
        )

        # Answer input field
        self.answer_field = ft.TextField(
            label="Enter your answer",
            password=True,
            width=500,
            on_change=lambda e: (self.clear_error(), self.toggle_continue_button(e))
        )

        # Continue button (initially disabled)
        self.continue_button = ft.ElevatedButton(
            text="Continue",
            on_click=self.validate_security_answer,
            width=500,
            disabled=True,
            style=ft.ButtonStyle(
                color={ft.ControlState.DEFAULT: ft.Colors.WHITE},
                bgcolor={ft.ControlState.DEFAULT: ft.Colors.GREEN},
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
                        width=900,
                        height=410,
                        bgcolor="#40444B",
                        border_radius=10,
                        padding=20,
                        alignment=ft.alignment.center_right,
                        content=ft.Row(
                            controls=[
                                # Left column - User Input
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
                                        ft.TextButton(
                                            "Back to Username Verification",
                                            on_click=lambda e: self.page.go("/username_verification"),
                                        ),
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    expand=2,
                                ),
                                # Right column - Branding/Icon
                                ft.Column(
                                    controls=[
                                        ft.Icon(name=ft.Icons.QUESTION_ANSWER, color=ft.Colors.GREEN, size=200),
                                        ft.Text("BudgetWise", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                                        ft.Text("Security Verification", size=12, weight=ft.FontWeight.NORMAL, color=ft.Colors.WHITE),
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    expand=1,
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

    def on_page_load(self, username):
        """Called when navigating to this page. Fetches security questions dynamically."""
        self.username = username  # Store the username

        # Fetch and populate dropdown options
        self.populate_security_questions()

        # Reset selection
        self.question_dropdown.value = None
        self.page.update()

    def populate_security_questions(self):
        """Populates the dropdown with security questions."""
        self.question_dropdown.options = [
            ft.dropdown.Option(text=question, key=str(key))
            for key, question in self.user_data.temp_questions.items() if question
        ]
        self.page.update()

    def clear_error(self):
        """Clears error messages when user interacts with input fields."""
        if self.error_text.value:
            self.error_text.value = ""
            self.page.update()

    def toggle_continue_button(self, e=None):
        """Enables the 'Continue' button when both question and answer are provided."""
        selected_key = self.question_dropdown.value
        user_answer = self.answer_field.value.strip()
        self.continue_button.disabled = not (selected_key and user_answer)
        self.page.update()

    def validate_security_answer(self, e):
        """Verifies the security answer for the selected question."""
        selected_key = self.question_dropdown.value  # Example: "1", "2", or "3"
        user_answer = self.answer_field.value.strip()

        if not selected_key or not user_answer:
            self.error_text.value = "Please select a question and enter an answer!"
            self.page.update()
            return

        # Convert `selected_key` to string to match stored dictionary keys
        selected_key = str(selected_key)

        # Verify the security answer
        if self.user_data.verify_security_answer(selected_key, user_answer):
            print("Security answer verified successfully!")
            self.page.go("/reset_password")
        else:
            self.error_text.value = "Incorrect answer! Try again."
            self.page.update()
