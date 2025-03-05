import flet as ft
from login import Login
import json

class LoginScene(ft.AlertDialog):
    def __init__(self, change_scene_callback, user_instance = None):
        self.change_scene_callback = change_scene_callback
        # Create username and password fields
        self.Login_text = ft.Text("Log in", size=100, color="grey", weight="bold")
        self.username_field = ft.TextField(label="Username", width=300)
        self.password_field = ft.TextField(label="Password", password=True, can_reveal_password=True, width=300)
        self.login_button = ft.ElevatedButton(text="Login", on_click=self.login)  # Update the on_click method
        self.error_message = ft.Text("", color="red")

        self.user_manager = user_instance

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
        """
        Handles login logic. If credentials are correct, transitions to the Dashboard.
        
        Arguments:
            e: The event triggered by the button click.
        """
        # Verify the entered username and password
        if self.user_manager.verify_password(self.username_field.value.strip(), self.password_field.value.strip()):
            print("Login successful, transitioning to Dashboard...")
            self.open = False  # Close the login form
            self.update()  # Ensure the UI is updated
            self.change_scene_callback(1)  # Move to the next scene (Dashboard)
        else:
            print("Invalid login attempt")
            self.error_message.value = "Invalid username or password."  # Show error message
            self.error_message.update()  # Update error message UI

        self.update()  # Ensure the UI is updated


class SignInScene(ft.AlertDialog):
    def __init__(self, change_scene_callback, show_security_questions_form, user_instance = None):
        self.change_scene_callback = change_scene_callback
        self.show_security_questions_form = show_security_questions_form
        signup_text = ft.Text("Sign-up", size=100, color="grey", weight="bold")
        self.username_field = ft.TextField(label="Username", width=300)
        self.password_field = ft.TextField(label="Password", password=True, can_reveal_password=True, width=300)
        self.confPassword_field = ft.TextField(label="Confirm Password", password=True, can_reveal_password=True, width=300)
        self.error_message = ft.Text("", color="red")

        self.user_manager = user_instance

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
        """
        Validates the user's password input during sign-up. Checks if the passwords match.
        
        Arguments:
            e: The event triggered by the button click.
        """
        # Check if all fields are filled in and if passwords match
        if not self.username_field.value.strip() or not self.password_field.value.strip() or not self.confPassword_field.value.strip():
            self.error_message.value = "All fields are required."
        elif self.password_field.value.strip() != self.confPassword_field.value.strip():
            self.error_message.value = "Passwords do not match."
        else:
            self.error_message.value = ""  # Clear error message
            print("Sign-Up clicked")
            self.show_security_questions_form()  # Move to the next step: security questions

        # Store temporary user info (username and password hash)
        self.user_manager.temp_info.update({
            "username": self.username_field.value.strip(),
            "password_hash": self.user_manager.hash_input(self.password_field.value.strip())
        })
        
        self.update()  # Ensure the UI is updated

        

class SecurityQuestionsForm(ft.AlertDialog):
    def __init__(self, change_scene_callback, show_account_creation_form, user_instance = None):
        super().__init__()
        self.change_scene_callback = change_scene_callback
        self.show_account_creation_form = show_account_creation_form
        self.user_manager = user_instance
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
        """
        Saves the user's selected security questions and their answers.
        
        Arguments:
            e: The event triggered by the save button click.
        """
        # Update temporary user info with security questions and hashed answers
        self.user_manager.temp_info.update({
            "security_question1": self.question1.value,
            "security_question1_answer": self.user_manager.hash_input(self.answer1.value.strip()),
            "security_question2": self.question2.value,
            "security_question2_answer": self.user_manager.hash_input(self.answer2.value.strip()),
            "security_question3": self.question3.value,
            "security_question3_answer": self.user_manager.hash_input(self.answer3.value.strip())
        })

        # Create the user in the system
        self.user_manager.create_user(**self.user_manager.temp_info)

        print("Security questions saved")
        self.open = False  # Close the security questions form
        self.update()  # Update the UI

        # Move to the next form (Account Creation)
        self.show_account_creation_form()



class AccountCreationForm(ft.AlertDialog):
    def __init__(self, change_scene_callback):
        self.change_scene_callback = change_scene_callback
        budget_text = ft.Text("Budget", size=100, color="grey", weight="bold")
        self.job_name = ft.TextField(label="Job Name", width=300, color="grey")
        self.income = ft.TextField(label="Income", width=300, color="grey")
        self.pay_period = ft.Dropdown(
            options=[
                ft.dropdown.Option("Default"),
                ft.dropdown.Option("Weekly"),
                ft.dropdown.Option("Bi-Weekly"),
                ft.dropdown.Option("Monthly")
            ],
            label="Pay Period",
            width=300, 
            color="grey"
        )
        create_transaction_button = ft.ElevatedButton(text="Create Transaction", on_click=self.create_budget)

        entry_column = ft.Column(
            controls=[
                budget_text,
                self.job_name,
                self.income,
                self.pay_period,
                create_transaction_button
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
    def __init__(self, change_scene_callback, data_manager, total_budget):
        super().__init__()
        self.change_scene_callback = change_scene_callback
        self.data_manager = data_manager
        self.total_budget = total_budget  # Total budget allocated
        self.remaining_amount = total_budget
        
        self.title = ft.Text("Create Accounts", size=24, weight="bold")
        self.account_name_field = ft.TextField(label="Account name:")
        self.amount_field = ft.TextField(label="Amount:")
        self.create_account_button = ft.TextButton("Create Account", on_click=self.submit_form)
        self.finish_button = ft.TextButton("Finish", on_click=self.close_form)

        self.total_budget_label = ft.Text(f"Total Budget: ${self.total_budget:.2f}", size=18)
        self.remaining_amount_label = ft.Text(f"Remaining: ${self.remaining_amount:.2f}", size=18, weight="bold", color="orange")

        self.summary_box = ft.ListView(expand=True)

        self.content = ft.Container(
            content=ft.Row([
                ft.Column([
                    self.title,
                    self.account_name_field,
                    self.amount_field,
                    self.create_account_button,
                    ft.Container(
                        content=ft.Column([
                            self.total_budget_label,  # Display total budget at the top
                            ft.Text("Budget Accounts:", size=18, weight="bold", color="Grey"),
                            # Wrap the summary_box in a scrollable container using ListView
                            self.summary_box,  # ListView already handles scrolling
                            self.remaining_amount_label,  # Display remaining amount at the bottom
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
                        height=250,
                    ),
                ], width=450),
            ]),
            width=900,
            padding=10,
            bgcolor="#0d0d10"
        )
            
        self.actions = [self.finish_button]

        self.data_manager.add_listener(self.refresh_summary)
        
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
            self.remaining_amount -= amount
            self.refresh_summary()  # Refresh summary after adding the account
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
            self.remaining_amount_label.value = f"Remaining: ${self.remaining_amount:.2f}"
            self.content.update()

    def edit_account(self, account_name):
        """Fills the fields with selected account info for editing."""
        if account_name in self.data_manager.accounts:  # Check if account exists
            self.account_name_field.value = account_name
            self.amount_field.value = str(self.data_manager.accounts[account_name])  # Direct dict lookup
            self.account_name_field.update()
            self.amount_field.update()

    def delete_account(self, account_name):
        """Deletes an account and updates the summary."""
        if account_name in self.data_manager.accounts:
            # Retrieve the amount to increase the remaining amount
            amount = self.data_manager.accounts[account_name]
            self.data_manager.remove_account(account_name)
            # Increase the remaining amount by the deleted account's amount
            self.remaining_amount += amount
            self.refresh_summary()  # Refresh summary after deleting the account
        else:
            print("Error: Account not found.")

    def close_form(self, e):
        """Handles closing the form."""
        self.open = False
        self.page.update()
        self.change_scene_callback(1)

class TransactionsForm(ft.AlertDialog):
    def __init__(self, change_scene_callback, data_manager):
        super().__init__()
        self.change_scene_callback = change_scene_callback
        self.data_manager = data_manager

        # Listen for changes in DataManager
        self.data_manager.add_listener(self.refresh_dropdown)

        self.job_name = ft.TextField(label="Transaction Name", width=300, color="grey")
        self.transaction_amount = ft.TextField(label="Transaction Amount", width=300)
        self.transaction_date = ft.TextField(label="Transaction Date", width=300)

        self.accounts = ft.Dropdown(
            options=self.get_account_options(),  # Get initial options
            label="Accounts",
            width=300
        )

        create_transaction_button = ft.ElevatedButton(text="Create Transaction", on_click=self.create_transaction)

        entry_column = ft.Column(
            controls=[
                ft.Text("Transaction", size=100, color="grey", weight="bold"),
                self.job_name,
                self.transaction_amount,
                self.transaction_date,
                self.accounts,
                create_transaction_button
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

        self.content = centered_container

    def get_account_options(self):
        """Fetches the latest accounts from DataManager and converts them to dropdown options."""
        return [ft.dropdown.Option(account) for account in self.data_manager.list_accounts()]

    def refresh_dropdown(self):
        """Updates the dropdown when accounts change."""
        self.accounts.options = self.get_account_options()  # Refresh options
        self.accounts.update()  # Ensure the dropdown updates in UI

    def create_transaction(self, e):
        """Creates a new transaction and updates the data manager."""
        name = self.job_name.value
        amount = self.transaction_amount.value
        date = self.transaction_date.value
        account = self.accounts.value

        if not name or not amount or not date or not account:
            print("Error: Missing transaction details")  # Handle validation properly
            return

        # Add transaction to DataManager
        transaction_id = self.data_manager.add_transaction(name, amount, date, account)
        print(f"Transaction added with ID: {transaction_id}")

        # Close the form
        self.open = False
        self.update()

        # Return to the dashboard or transaction scene
        self.change_scene_callback(4)

    def close_form(self, e):
        """Handles closing the form."""
        self.open = False
        self.page.update()
        self.change_scene_callback(4)