import flet as ft

class LoginScene(ft.AlertDialog):
    def __init__(self, change_scene_callback, user_instance=None):
        """
        Initializes the LoginScene with the necessary UI elements.
        
        Arguments:
            change_scene_callback (function): Callback function to change the current scene.
            user_instance (User, optional): User object that handles user-related operations.
        """
        # Store the callback and user manager instance
        self.change_scene_callback = change_scene_callback
        self.user_manager = user_instance

        # UI Components
        self.Login_text = ft.Text("Log in", size=100, color="grey", weight="bold")  # Header text
        self.username_field = ft.TextField(label="Username", width=300, bgcolor="#333333", color = "#B5CBB7") 
        self.password_field = ft.TextField(label="Password", password=True, can_reveal_password=True, width=300, bgcolor="#333333", color = "#B5CBB7")  # Password field
        self.login_button = ft.ElevatedButton(text="Login", on_click=self.login, bgcolor="#333333", color = "#B5CBB7")  # Button to trigger login
        self.error_message = ft.Text("", color="red")  # Placeholder for error messages

        # Column to organize the login form components
        self.login_column = ft.Column(
            controls=[self.Login_text, self.username_field, self.password_field, self.login_button, self.error_message],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        )

        # Container to hold the column and center-align everything
        centered_container = ft.Container(
            content=self.login_column,
            alignment=ft.alignment.center,
            bgcolor="#0d0d10",  # Dark background color
            width=720,  # Set width of the container
            height=960,  # Set height of the container
            padding=20  # Padding inside the container
        )

        # Initialize the AlertDialog with the centered container as content
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
    def __init__(self, change_scene_callback, show_security_questions_form, user_instance=None):
        """
        Initializes the SignInScene with user registration UI elements.
        
        Arguments:
            change_scene_callback (function): Callback function to change scenes.
            show_security_questions_form (function): Function to show the next step (security questions).
            user_instance (User, optional): User object to handle user-related operations.
        """
        self.change_scene_callback = change_scene_callback
        self.show_security_questions_form = show_security_questions_form
        self.user_manager = user_instance

        # UI Components for sign-up form
        signup_text = ft.Text("Sign-up", size=100, color="grey", weight="bold")  # Header text
        self.username_field = ft.TextField(label="Username", width=300, bgcolor="#333333", color = "#B5CBB7")  # Text field for the username
        self.password_field = ft.TextField(label="Password", password=True, can_reveal_password=True, width=300, bgcolor="#333333", color = "#B5CBB7")  # Password field
        self.confPassword_field = ft.TextField(label="Confirm Password", password=True, can_reveal_password=True, width=300, bgcolor="#333333", color = "#B5CBB7")  # Confirm password field
        self.error_message = ft.Text("", color="red")  # Placeholder for error messages

        # Button to submit the form
        signup_button = ft.ElevatedButton(text="Next", bgcolor="#333333", color = "#B5CBB7", on_click=self.validate_password)

        # Column to organize the form components
        signup_column = ft.Column(
            controls=[signup_text, self.username_field, self.password_field, self.confPassword_field, self.error_message, signup_button],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        )

        # Container to hold the sign-up form and center-align it
        centered_container = ft.Container(
            content=signup_column,
            alignment=ft.alignment.center,
            bgcolor="#0d0d10",
            width=720,
            height=960,
            padding=20
        )

        # Initialize the AlertDialog with the centered container as content
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
    def __init__(self, change_scene_callback, show_account_creation_form, user_instance=None):
        """
        Initializes the SecurityQuestionsForm where users answer security questions for account verification.
        
        Arguments:
            change_scene_callback (function): Callback function to change the current scene.
            show_account_creation_form (function): Function to display account creation form after security questions.
            user_instance (User, optional): User object for managing user-related operations.
        """
        super().__init__()

        # Store the callback and user manager instance
        self.change_scene_callback = change_scene_callback
        self.show_account_creation_form = show_account_creation_form
        self.user_manager = user_instance

        # Predefined list of security questions
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

        #trigger element for dropdowns has not color need to fix.
        # Dropdowns for selecting security questions and text fields for answers
        self.question1 = ft.Dropdown(label= "Select a Security Question", filled= True, fill_color = "#333333", bgcolor="#333333", color = "#333333", options=[ft.dropdown.Option(question) for question in self.questions], on_change=self.update_dropdowns)
        self.answer1 = ft.TextField(bgcolor="#333333", color = "#B5CBB7", label="Answer 1", width=300)
        self.question2 = ft.Dropdown(label= "Select a Security Question", filled= True, fill_color = "#333333", bgcolor="#333333", color = "#333333", options=[ft.dropdown.Option(question) for question in self.questions], on_change=self.update_dropdowns)
        self.answer2 = ft.TextField(bgcolor="#333333", color = "#B5CBB7", label="Answer 2", width=300)
        self.question3 = ft.Dropdown(label= "Select a Security Question", filled= True, fill_color = "#333333", bgcolor="#333333", color = "#333333", options=[ft.dropdown.Option(question) for question in self.questions], on_change=self.update_dropdowns)
        self.answer3 = ft.TextField(bgcolor="#333333", color = "#B5CBB7", label="Answer 3", width=300)

        # Button to save the answers and move to account creation
        save_button = ft.ElevatedButton(text="Save", bgcolor="#333333", color = "#B5CBB7", on_click=self.save_security_questions)

        # Column to organize the security questions and answers
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

        # Container to center-align the security questions form
        centered_container = ft.Container(
            content=questions_column,
            alignment=ft.alignment.center,
            bgcolor="#0d0d10",
            width=720,
            height=960,
            padding=20
        )

        # Assign the container as the content of the form
        self.content = centered_container

    def update_dropdowns(self, e):
        """
        Updates the dropdown options for the security questions to prevent duplicate selections.
        
        Arguments:
            e: The event triggered by the dropdown change.
        """
        # Get the selected questions and remove duplicates from the dropdown options
        selected_questions = {self.question1.value, self.question2.value, self.question3.value}

        # Function to return the remaining options for the dropdowns
        def get_remaining_options(selected_question):
            return [ft.dropdown.Option(q) for q in self.questions if q not in selected_questions or q == selected_question]

        # Update options for each dropdown
        self.question1.options = get_remaining_options(self.question1.value)
        self.question2.options = get_remaining_options(self.question2.value)
        self.question3.options = get_remaining_options(self.question3.value)

        # Refresh dropdown UI
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
        """
        Initializes the AccountCreationForm with input fields for budgeting details.
        
        Arguments:
            change_scene_callback (function): Callback function to change the current scene.
        """
        self.change_scene_callback = change_scene_callback
        
        # UI Components
        budget_text = ft.Text("Budget", size=100, color="grey", weight="bold")  # Title text
        self.job_name = ft.TextField(label="Job Name", width=300)  # Field for job name
        self.income = ft.TextField(label="Income", width=300)  # Field for income input
        self.pay_period = ft.Dropdown(
            options=[
                ft.dropdown.Option("Default"),
                ft.dropdown.Option("Weekly"),
                ft.dropdown.Option("Bi-Weekly"),
                ft.dropdown.Option("Monthly")
            ],
            label="Pay Period",
            width=300
        )  # Dropdown for pay period selection

        # Button to trigger budget creation
        create_budget_button = ft.ElevatedButton(text="Create Budget", on_click=self.create_budget)

        # Column to organize the form elements
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

        # Container to hold the form and center-align everything
        centered_container = ft.Container(
            content=entry_column,
            alignment=ft.alignment.center,
            bgcolor="#0d0d10",
            width=720,
            height=960,
            padding=20
        )

        # Initialize the AlertDialog with the centered container as content
        super().__init__(content=centered_container)

    def create_budget(self, e):
        """
        Handles the budget creation process. In a real scenario, this would save the budget data.
        
        Arguments:
            e: The event triggered by the button click.
        """
        # Placeholder for actual budget creation logic
        print("Budget created")
        
        # Close the current form
        self.open = False
        self.update()
        
        # Call the callback to switch to the next scene (e.g., Dashboard)
        self.change_scene_callback(1)


class BudgetCreationForm(ft.AlertDialog):
    def __init__(self, change_scene_callback, data_manager):
        """
        Initializes the BudgetCreationForm where users can create and manage budget accounts.
        
        Arguments:
            change_scene_callback (function): Callback function to change scenes after the form is completed.
            data_manager (DataManager): An object responsible for managing account data.
        """
        super().__init__()
        self.change_scene_callback = change_scene_callback
        self.data_manager = data_manager
        
        # UI Components
        self.title = ft.Text("Create Accounts", size=24, weight="bold")  # Title for the form
        self.account_name_field = ft.TextField(label="Account name:")  # Field to enter account name
        self.amount_field = ft.TextField(label="Amount:")  # Field to enter account amount
        self.create_account_button = ft.TextButton("Create Account", on_click=self.submit_form)  # Button to create a new account
        self.finish_button = ft.TextButton("Finish", on_click=self.close_form)  # Button to finish and close the form

        # Summary box to display created accounts
        self.summary_box = ft.Column()

        # Container to hold the form and summary box
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

        # Define actions (buttons) for the form
        self.actions = [self.finish_button]

    def submit_form(self, e):
        """
        Handles the creation of a new account. Validates the inputs and adds the account if valid.
        
        Arguments:
            e: The event triggered by the button click.
        """
        # Get account name and amount from input fields
        account_name = self.account_name_field.value
        try:
            amount = float(self.amount_field.value)  # Convert amount to a float
        except ValueError:
            print("Error: Amount must be a valid number.")  # Display error if amount is invalid
            return

        # If account name is provided, add it to the data manager
        if account_name:
            self.data_manager.add_account(account_name, amount)  # Add account to data manager
            self.refresh_summary()  # Refresh the summary of accounts
            self.account_name_field.value = ""  # Clear the input fields
            self.amount_field.value = ""
            self.account_name_field.update()
            self.amount_field.update()
        else:
            print("Error: Account name must be provided.")  # Display error if account name is empty

    def refresh_summary(self):
        """
        Refreshes the summary box with the list of accounts and associated actions.
        Displays created accounts with options to edit or delete them.
        """
        self.summary_box.controls.clear()  # Clear the existing summary
        for account, value in self.data_manager.list_accounts().items():  # List accounts using the data manager
            self.summary_box.controls.append(
                ft.Row([
                    ft.Text(f"{account}: ${value:.2f}", expand=True),  # Display account name and amount
                    ft.IconButton(ft.icons.EDIT, on_click=lambda e, a=account: self.edit_account(a)),  # Button to edit account
                    ft.IconButton(ft.icons.DELETE, on_click=lambda e, a=account: self.delete_account(a)),  # Button to delete account
                ])
            )
        self.summary_box.update()  # Update the summary display

    def edit_account(self, account_name):
        """
        Fills the input fields with the selected account details for editing.
        
        Arguments:
            account_name (str): The name of the account to be edited.
        """
        # Check if the account exists in the data manager
        if account_name in self.data_manager.accounts:
            # Set the fields with the account's existing details
            self.account_name_field.value = account_name
            self.amount_field.value = str(self.data_manager.accounts[account_name])
            self.account_name_field.update()
            self.amount_field.update()

    def delete_account(self, account_name):
        """
        Deletes an account from the data manager and refreshes the summary.
        
        Arguments:
            account_name (str): The name of the account to be deleted.
        """
        # Check if the account exists before deleting it
        if account_name in self.data_manager.accounts:
            self.data_manager.remove_account(account_name)  # Remove the account from data manager
            self.refresh_summary()  # Refresh the summary to reflect the changes
        else:
            print("Error: Account not found.")  # Display error if account is not found

    def close_form(self, e):
        """
        Handles closing the form and transitioning to the next scene (e.g., Dashboard).
        
        Arguments:
            e: The event triggered by the finish button click.
        """
        # Close the current form and update the UI
        self.open = False
        self.page.update()
        
        # Switch to the next scene (Dashboard)
        self.change_scene_callback(1)
