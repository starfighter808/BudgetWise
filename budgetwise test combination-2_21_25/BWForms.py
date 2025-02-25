import flet as ft
from login import Login
import json

class LoginScene(ft.AlertDialog):
    def __init__(self, change_scene_callback):
        self.change_scene_callback = change_scene_callback
        # Create username and password fields
        self.Login_text = ft.Text("Log in", size=100, color="grey", weight="bold")
        self.username_field = ft.TextField(label="Username", width=300)
        self.password_field = ft.TextField(label="Password", password=True, can_reveal_password=True, width=300)
        self.login_button = ft.ElevatedButton(text="Login", on_click=self.login)  # Update the on_click method
        self.error_message = ft.Text("", color="red")

        self.login_manager = Login()

        # Create a column with the fields and button, aligned to the center
        self.login_column = ft.Column(
            controls=[self.Login_text, self.username_field, self.password_field, self.login_button, self.error_message],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        )

        # Wrap the column in a container and set alignment to center
        centered_container = ft.Container(
            content=self.login_column,
            alignment=ft.alignment.center,
            bgcolor="#0d0d10",  # Change the background color here
            width=720,  # Adjust the width
            height=960,  # Adjust the height
            padding=20  # Optional: Add padding inside the container
        )

        # Initialize the AlertDialog with the container as content
        super().__init__(content=centered_container)

    def login(self, e):
        user_input_username = self.username_field.value
        user_input_password = self.password_field.value

        print("Login button clicked")  # Debugging print statement
        print(f"Username: {user_input_username}, Password: {user_input_password}")  # Debugging print statement

        userID = self.login_manager.login(user_input_username, user_input_password)

        if userID:
            print("Login successful, transitioning to Dashboard...")
            self.open = False  # Close the login form
            self.update()  # Ensure the UI updates to reflect changes
            self.change_scene_callback(1)  # Index of Dashboard scene
        else:
            print("Invalid login attempt")
            self.error_message.value = "Invalid username or password."
            self.error_message.update()  # Ensure the UI updates

        self.update()  # Ensure the UI is updated


class SignInScene(ft.AlertDialog):
    def __init__(self, change_scene_callback, show_security_questions_form):
        self.change_scene_callback = change_scene_callback
        self.show_security_questions_form = show_security_questions_form
        signup_text = ft.Text("Sign-up", size=100, color="grey", weight="bold")
        self.username_field = ft.TextField(label="Username", width=300)
        self.password_field = ft.TextField(label="Password", password=True, can_reveal_password=True, width=300)
        self.confPassword_field = ft.TextField(label="Confirm Password", password=True, can_reveal_password=True, width=300)
        self.error_message = ft.Text("", color="red")

        self.login_manager = Login()

        signup_button = ft.ElevatedButton(text="Next", on_click=self.validate_password)

        signup_column = ft.Column(
            controls=[signup_text, self.username_field, self.password_field, self.confPassword_field, self.error_message, signup_button],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        )

        centered_container = ft.Container(
            content=signup_column,
            alignment=ft.alignment.center,
            bgcolor="#0d0d10",
            width=720,
            height=960,
            padding=20
        )

        super().__init__(content=centered_container)

    def validate_password(self, e):
        if not self.username_field.value or not self.password_field.value or not self.confPassword_field.value:
            self.error_message.value = "All fields are required."
        elif self.password_field.value != self.confPassword_field.value:
            self.error_message.value = "Passwords do not match."
        else:
            self.error_message.value = ""
            print("Sign-Up clicked")
            self.show_security_questions_form()

        inputed_username = self.username_field.value
        inputed_password = self.password_field.value
        
        self.login_manager.signUp(inputed_username, inputed_password)

        self.update()
        

class SecurityQuestionsForm(ft.AlertDialog):
    def __init__(self, change_scene_callback, show_account_creation_form):
        super().__init__()
        self.change_scene_callback = change_scene_callback
        self.show_account_creation_form = show_account_creation_form
        self.questions = [
            "What was the name of your first pet?",
            "What is your mother’s maiden name?",
            "What was the make and model of your first car?",
            "What is the name of the town where you were born?",
            "What was your childhood best friend’s name?",
            "What is the name of your favorite teacher?",
            "What is the name of your first school?",
            "What is the name of your favorite childhood book?",
            "What was the name of the first company you worked for?",
            "What is your favorite movie?",
            "What is your favorite food?",
            "What is the middle name of your oldest sibling?",
            "What was your first phone number?",
            "Where did you go on your first vacation?",
            "What was the name of your first stuffed animal?",
            "What is the name of your first love?",
            "What is the street name of your childhood home?",
            "What is the name of the hospital where you were born?",
            "What is your father’s middle name?",
            "What was the first concert you attended?",
        ]

        self.question1 = ft.Dropdown(options=[ft.dropdown.Option(question) for question in self.questions], on_change=self.update_dropdowns)
        self.answer1 = ft.TextField(label="Answer 1", width=300)
        self.question2 = ft.Dropdown(options=[ft.dropdown.Option(question) for question in self.questions], on_change=self.update_dropdowns)
        self.answer2 = ft.TextField(label="Answer 2", width=300)
        self.question3 = ft.Dropdown(options=[ft.dropdown.Option(question) for question in self.questions], on_change=self.update_dropdowns)
        self.answer3 = ft.TextField(label="Answer 3", width=300)

        save_button = ft.ElevatedButton(text="Save", on_click=self.save_security_questions)

        questions_column = ft.Column(
            controls=[
                self.question1, self.answer1,
                self.question2, self.answer2,
                self.question3, self.answer3,
                save_button
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        )

        centered_container = ft.Container(
            content=questions_column,
            alignment=ft.alignment.center,
            bgcolor="#0d0d10",
            width=720,
            height=960,
            padding=20
        )

        self.content = centered_container

    def update_dropdowns(self, e):
        selected_questions = {self.question1.value, self.question2.value, self.question3.value}

        def get_remaining_options(selected_question):
            return [ft.dropdown.Option(q) for q in self.questions if q not in selected_questions or q == selected_question]

        self.question1.options = get_remaining_options(self.question1.value)
        self.question2.options = get_remaining_options(self.question2.value)
        self.question3.options = get_remaining_options(self.question3.value)

        self.question1.update()
        self.question2.update()
        self.question3.update()

    def save_security_questions(self, e):
        # Collecting selected questions and answers
        security_data = {
            "question1": self.question1.value,
            "answer1": self.answer1.value,
            "question2": self.question2.value,
            "answer2": self.answer2.value,
            "question3": self.question3.value,
            "answer3": self.answer3.value
        }

        # Saving security questions and answers to a JSON file
        with open("security_questions.json", "w") as file:
            json.dump(security_data, file)

        print("Security questions saved")
        self.open = False
        self.update()

        # Directly call the AccountCreationForm (BudgetEntryDialog) after saving security questions
        self.show_account_creation_form()



class AccountCreationForm(ft.AlertDialog):
    def __init__(self, change_scene_callback):
        self.change_scene_callback = change_scene_callback
        budget_text = ft.Text("Budget", size=100, color="grey", weight="bold")
        self.job_name = ft.TextField(label="Job Name", width=300)
        self.income = ft.TextField(label="Income", width=300)
        self.pay_period = ft.Dropdown(
            options=[
                ft.dropdown.Option("Default"),
                ft.dropdown.Option("Weekly"),
                ft.dropdown.Option("Bi-Weekly"),
                ft.dropdown.Option("Monthly")
            ],
            label="Pay Period",
            width=300
        )
        create_budget_button = ft.ElevatedButton(text="Create Budget", on_click=self.create_budget)

        entry_column = ft.Column(
            controls=[
                budget_text,
                self.job_name,
                self.income,
                self.pay_period,
                create_budget_button
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        )

        centered_container = ft.Container(
            content=entry_column,
            alignment=ft.alignment.center,
            bgcolor="#0d0d10",
            width=720,
            height=960,
            padding=20
        )

        super().__init__(content=centered_container)

    def create_budget(self, e):
        # Implement your create budget logic here
        print("Budget created")
        
        # Close the current form
        self.open = False
        self.update()
        
        # Call back to the dashboard scene
        self.change_scene_callback(1) 

class BudgetCreationForm(ft.AlertDialog):
    def __init__(self, change_scene_callback, data_manager):
        super().__init__()
        self.change_scene_callback = change_scene_callback
        self.data_manager = data_manager
        
        self.title = ft.Text("Create Accounts", size=24, weight="bold")
        self.account_name_field = ft.TextField(label="Account name:")
        self.amount_field = ft.TextField(label="Amount:")
        self.create_account_button = ft.TextButton("Create Account", on_click=self.submit_form)
        self.finish_button = ft.TextButton("Finish", on_click=self.close_form)

        self.summary_box = ft.Column()

        self.content = ft.Container(
            content=ft.Row([
                ft.Column([
                    self.title,
                    self.account_name_field,
                    self.amount_field,
                    self.create_account_button,
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Budget Accounts:", size=18, weight="bold", color="Grey"),
                            self.summary_box,
                        ]),
                        padding=10,
                        border=ft.Border(
                            left=ft.BorderSide(1, "Grey"),
                            top=ft.BorderSide(1, "Grey"),
                            right=ft.BorderSide(1, "Grey"),
                            bottom=ft.BorderSide(1, "Grey")
                        ),
                        border_radius=5,
                        width=400,
                        height=300,
                    ),
                ], width=450),
            ]),
            width=900,
            padding=10,
            bgcolor="#0d0d10"
        )

        self.actions = [self.finish_button]
        
    def submit_form(self, e):
        """Handles creating a new account."""
        account_name = self.account_name_field.value
        try:
            amount = float(self.amount_field.value)
        except ValueError:
            print("Error: Amount must be a valid number.")
            return

        if account_name:
            self.data_manager.add_account(account_name, amount)
            self.refresh_summary()
            self.account_name_field.value = ""
            self.amount_field.value = ""
            self.account_name_field.update()
            self.amount_field.update()
        else:
            print("Error: Account name must be provided.")

    def refresh_summary(self):
        """Refreshes the summary box with accounts and action buttons."""
        self.summary_box.controls.clear()
        for account, value in self.data_manager.list_accounts().items():  # ✅ Uses `.items()` for dict
            self.summary_box.controls.append(
                ft.Row([
                    ft.Text(f"{account}: ${value:.2f}", expand=True),
                    ft.IconButton(ft.icons.EDIT, on_click=lambda e, a=account: self.edit_account(a)),
                    ft.IconButton(ft.icons.DELETE, on_click=lambda e, a=account: self.delete_account(a)),
                ])
            )
        self.summary_box.update()

    def edit_account(self, account_name):
        """Fills the fields with selected account info for editing."""
        if account_name in self.data_manager.accounts:  # ✅ Check if account exists
            self.account_name_field.value = account_name
            self.amount_field.value = str(self.data_manager.accounts[account_name])  # ✅ Direct dict lookup
            self.account_name_field.update()
            self.amount_field.update()

    def delete_account(self, account_name):
        """Deletes an account and updates the summary."""
        if account_name in self.data_manager.accounts:
            self.data_manager.remove_account(account_name)
            self.refresh_summary()
        else:
            print("Error: Account not found.")

    def close_form(self, e):
        """Handles closing the form."""
        self.open = False
        self.page.update()
        self.change_scene_callback(1)