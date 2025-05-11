import flet as ft

class SecurityQuestions(ft.View):
    def __init__(self, page: ft.Page, user_data, colors):
        super().__init__(route="/security_questions", bgcolor= colors.BLUE_BACKGROUND)
        
        self.page = page
        self.user_data = user_data  # Store user repository for temp_info storag
        self.colors = colors

        # Security questions dictionary
        self.security_questions = {
            "1": "What was the name of your first pet?",
            "2": "What is your mother’s maiden name?",
            "3": "What was the make and model of your first car?",
            "4": "What is the name of the town where you were born?",
            "5": "What was your childhood best friend’s name?",
            "6": "What is the name of your favorite teacher?",
            "7": "What is the name of your first school?",
            "8": "What is the name of your favorite childhood book?",
            "9": "What was the name of the first company you worked for?",
            "10": "What is your favorite movie?",
        }
        
        # Track selected questions
        self.selected_questions = {"q1": None, "q2": None, "q3": None}

        def get_dropdown_options(current_key=None):
            """Generate dropdown options excluding already selected questions."""
            selected_ids = set(filter(None, self.selected_questions.values()))
            if current_key and self.selected_questions[current_key] in selected_ids:
                selected_ids.remove(self.selected_questions[current_key])
            return [
                ft.dropdown.Option(key=k, text=v)
                for k, v in self.security_questions.items()
                if k not in selected_ids
            ]

        def dropdown_changed(e, key):
            """Handle dropdown selection changes."""
            selected_key = e.control.value
            self.selected_questions[key] = selected_key
            
            # Refresh all dropdowns
            self.dd1.options = get_dropdown_options("q1")
            self.dd2.options = get_dropdown_options("q2")
            self.dd3.options = get_dropdown_options("q3")
            self.dd1.update()
            self.dd2.update()
            self.dd3.update()

        # Dropdowns with Containers for full expansion
        self.dd1 = ft.Dropdown(
            label="Select Security Question 1",
            options=get_dropdown_options("q1"),
            value=None,
            on_change=lambda e: dropdown_changed(e, "q1"),
            filled=True,
            width=500,
            expand=True,
        )
        self.answer1 = ft.TextField(
            width=500,
            label="Answer 1", 
            label_style=ft.TextStyle(color=self.colors.BORDERBOX_COLOR), 
            text_style=ft.TextStyle(color=self.colors.TEXT_COLOR),
            hint_text="Answer your first security question",
            hint_style=ft.TextStyle(color=self.colors.BLUE_BACKGROUND),
            focused_border_color=self.colors.BORDERBOX_COLOR 
            )

        self.dd2 = ft.Dropdown(
            label="Select Security Question 2",
            options=get_dropdown_options("q2"),
            value=None,
            on_change=lambda e: dropdown_changed(e, "q2"),
            filled=True,
            width=500,
            expand=True,
        )
        self.answer2 = ft.TextField(
            width=500, 
            label="Answer 2", 
            label_style=ft.TextStyle(color=self.colors.BORDERBOX_COLOR), 
            text_style=ft.TextStyle(color=self.colors.TEXT_COLOR),
            hint_text="Answer your second security question",
            hint_style=ft.TextStyle(color=self.colors.BLUE_BACKGROUND),
            focused_border_color=self.colors.BORDERBOX_COLOR, 
            )

        self.dd3 = ft.Dropdown(
            label="Select Security Question 3",
            options=get_dropdown_options("q3"),
            value=None,
            on_change=lambda e: dropdown_changed(e, "q3"),
            filled=True,
            width=500,
            expand=True,
        )
        self.answer3 = ft.TextField(
            width= 500, 
            label="Answer 3", 
            label_style=ft.TextStyle(color=self.colors.BORDERBOX_COLOR), 
            text_style=ft.TextStyle(color=self.colors.TEXT_COLOR),
            hint_text="Answer your third security question",
            hint_style=ft.TextStyle(color=self.colors.BLUE_BACKGROUND),
            focused_border_color=self.colors.BORDERBOX_COLOR, 
            )

        def validate_and_continue(e):
            """Validates security questions, updates temp_sign_in_data with the questions and answers, and initiates user creation."""
            
            # Get selected security questions and answers
            q1, q2, q3 = self.dd1.value, self.dd2.value, self.dd3.value
            a1 = self.user_data.hash_password(self.answer1.value.strip()) if self.answer1.value else None
            a2 = self.user_data.hash_password(self.answer2.value.strip()) if self.answer2.value else None
            a3 = self.user_data.hash_password(self.answer3.value.strip()) if self.answer3.value else None

            # Validate that all questions and answers are provided
            if not all([q1, q2, q3, a1, a2, a3]):
                self.error_text.value = "All questions and answers must be filled!"
                self.error_text.visible = True
                self.page.update()
                return

            # Update temp_sign_in_data with security questions and answers without overwriting existing keys
            self.user_data.temp_sign_up_data.update({
                "security_question1": self.security_questions.get(q1, ""),
                "security_question2": self.security_questions.get(q2, ""),
                "security_question3": self.security_questions.get(q3, ""),
                "security_question1_answer": a1,
                "security_question2_answer": a2,
                "security_question3_answer": a3,
            })

            # Start user creation process using the updated temp_sign_in_data
            success = self.user_data.create_user()

            if success:
                print("User account created successfully!")
                self.error_text.visible = False
                self.answer1.value = ""
                self.answer2.value = ""
                self.answer3.value = ""
                self.page.go("/create_budget")  # Proceed to the next step
            else:
                self.error_text.value = "Failed to create user. Please try again."
                self.error_text.visible = True
                self.page.update()
            



        self.error_text = ft.Text("", color= colors.ERROR_RED)

        question_answer_groups = ft.Column(
            controls=[
                ft.Container(content=ft.Column([self.dd1, self.answer1]), expand=True),
                ft.Divider(height=20, color= colors.TEXT_COLOR, thickness=1),
                ft.Container(content=ft.Column([self.dd2, self.answer2]), expand=True),
                ft.Divider(height=20, color= colors.TEXT_COLOR, thickness=1),
                ft.Container(content=ft.Column([self.dd3, self.answer3]), expand=True),
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.START,
            width=500,
            expand=True,
        )


        # Main container layout
        self.controls = [
            ft.Row(
                controls=[ 
                    ft.Container(
                        width=900,
                        height=650,
                        bgcolor=self.colors.GREY_BACKGROUND,
                        border_radius=10,
                        padding=20,
                        content=ft.Row(
                            controls=[
                                # First column
                                ft.Column(
                                    controls=[
                                        ft.Row(
                                            controls=[

                                                ft.Text(
                                                "Security Questions", 
                                                text_align=ft.TextAlign.CENTER, 
                                                size=24, 
                                                weight=ft.FontWeight.BOLD, 
                                                color=self.colors.TEXT_COLOR
                                                ),
                                            ],
                                            alignment=ft.MainAxisAlignment.CENTER,
                                        ),
                                        ft.Row(
                                            controls=[
                                                ft.Text(
                                                "These are used for password recovery", 
                                                text_align=ft.TextAlign.CENTER, 
                                                color=self.colors.TEXT_COLOR
                                                ),
                                            ],
                                            alignment=ft.MainAxisAlignment.CENTER,
                                        ),
                                        question_answer_groups,
                                        self.error_text,  

                                        ft.Column(
                                            controls=
                                            [
                                                ft.ElevatedButton(
                                                    "Continue", 
                                                    on_click=validate_and_continue, 
                                                    width=500,
                                                    style=ft.ButtonStyle(
                                                        color={ft.ControlState.DEFAULT: self.colors.TEXT_COLOR, ft.ControlState.HOVERED: self.colors.TEXT_COLOR},
                                                        bgcolor={ft.ControlState.DEFAULT: self.colors.GREEN_BUTTON},
                                                        padding={ft.ControlState.HOVERED: 20},
                                                        overlay_color=self.colors.TRANSPARENT,
                                                        elevation={"pressed": 0, "": 0},
                                                        animation_duration=0,
                                                        side={ft.ControlState.DEFAULT: ft.BorderSide(1, self.colors.GREEN_BUTTON)},
                                                        shape={ft.ControlState.DEFAULT: ft.RoundedRectangleBorder(radius=8)},
                                                    ),
                                                ),
                                            ],
                                        ),
 
                                        ft.Row(
                                            controls=[
                                                ft.TextButton(
                                                    "Previous?", 
                                                    on_click=lambda e: page.go("/sign_up"),
                                                ),
                                            ],
                                            alignment=ft.MainAxisAlignment.START,
                                        ),
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    horizontal_alignment=ft.CrossAxisAlignment.START,
                                    expand=2,
                                ),
                                # Second column
                                ft.Column(
                                    controls=[
                                        ft.Icon(name=ft.Icons.SECURITY, color=self.colors.GREEN_BUTTON, size=300),
                                        ft.Text("BudgetWise", size=24, weight=ft.FontWeight.BOLD, color=self.colors.TEXT_COLOR),
                                        ft.Text("Select Security Questions", size=12, weight=ft.FontWeight.NORMAL, color=self.colors.TEXT_COLOR),
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    expand=1,
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

