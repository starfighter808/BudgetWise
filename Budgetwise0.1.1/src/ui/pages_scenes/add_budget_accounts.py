import flet as ft

class AddBudgetAccounts(ft.View):
    def __init__(self, page: ft.Page, user_data, colors):
        super().__init__(route="/add_budget_accounts", bgcolor=colors.BLUE_BACKGROUND)
        self.page = page
        self.user_data = user_data
        self.colors = colors

        # Initialize accounts list
        self.accounts = []

        # Ensure the user_data is valid; otherwise, redirect to the budget creation page
        if not self.user_data or not hasattr(self.user_data, "budget_name") or not hasattr(self.user_data, "budget_amount"):
            print("User data missing, redirecting to create budget...")
            self.page.go("/create_budget")
            return

        # Display budget information
        self.budget_name_display = ft.Text(value="", size=20, color=colors.TEXT_COLOR)
        self.budget_amount_display = ft.Text(value="", size=20, color=colors.TEXT_COLOR)
        self.leftover_text = ft.Text(value="", size=20, color=colors.TEXT_COLOR)

        # Input fields
        self.account_name_field = ft.TextField(label="Account Name", width=300)
        self.account_allocated_field = ft.TextField(label="Total Allocated Amount", keyboard_type=ft.KeyboardType.NUMBER, width=300)
        self.account_type_dropdown = ft.Dropdown(
            label="Account Type",
            options=[ft.dropdown.Option("Checking"), ft.dropdown.Option("Savings"), ft.dropdown.Option("Investment")],
            width=300
        )

        # Account List
        self.accounts_list = ft.Column(scroll=True, spacing=10)

        # Add Account Button
        self.add_account_button = ft.ElevatedButton("Add Account", on_click=self.add_account, width=300)

        # Continue Button
        self.continue_button = ft.ElevatedButton("Continue", on_click=self.continue_to_db, width=300)

        # Layout
        self.controls = [
            ft.Container(
                expand=True,
                bgcolor=colors.GREY_BACKGROUND,
                border_radius=10,
                padding=20,
                content=ft.Column(
                    controls=[
                        self.budget_name_display,
                        self.budget_amount_display,
                        self.leftover_text,
                        ft.Divider(height=20, color=colors.TEXT_COLOR),
                        self.account_name_field,
                        self.account_type_dropdown,
                        self.account_allocated_field,
                        self.add_account_button,
                        ft.Divider(height=20, color=colors.TEXT_COLOR),
                        ft.Text("Accounts Added:", size=20, color=colors.TEXT_COLOR),
                        self.accounts_list,
                        ft.Divider(height=20, color=colors.TEXT_COLOR),
                        self.continue_button,
                        ft.TextButton("Previous?", on_click=lambda e: self.page.go("/create_budget")),
                    ],
                    spacing=10,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                )
            )
        ]

    def did_mount(self):
        """ Ensure budget data is fully initialized before mounting """
        if not self.user_data or not hasattr(self.user_data, "budget_name") or not hasattr(self.user_data, "budget_amount"):
            print("Budget data not found, redirecting user to /create_budget")
            self.page.go("/create_budget")
            return

        # Set budget values now that the page has mounted
        self.budget_name_display.value = f"Budget Name: {self.user_data.budget_name}"
        self.budget_amount_display.value = f"Budget Amount: ${self.user_data.budget_amount}"

        # Ensure leftover amount is calculated correctly
        self.leftover_amount = self.user_data.budget_amount  # Set initial leftover amount
        self.leftover_text.value = f"Leftover Amount: ${self.leftover_amount}"  # Assign UI text

        # Explicitly update UI elements
        self.budget_name_display.update()
        self.budget_amount_display.update()
        self.leftover_text.update()

    def add_account(self, e):
        name = self.account_name_field.value.strip()
        allocated_str = self.account_allocated_field.value.strip()
        account_type = self.account_type_dropdown.value

        if not name:
            self.account_name_field.error_text = "Account name cannot be empty"
            self.account_name_field.update()
            return

        try:
            allocated = float(allocated_str)
        except ValueError:
            self.account_allocated_field.error_text = "Please enter a valid number"
            self.account_allocated_field.update()
            return

        if allocated > self.leftover_amount:
            self.account_allocated_field.error_text = f"Amount exceeds leftover (${self.leftover_amount})"
            self.account_allocated_field.update()
            return

        account = {
            "name": name,
            "type": account_type,
            "total_allocated": allocated,
            "current_amount": allocated,
            "savings_goal": 0.0
        }
        self.accounts.append(account)
        self.update_leftover(self.accounts)

        self.refresh_accounts_list()

        # Clear input fields
        self.account_name_field.value = ""
        self.account_allocated_field.value = ""
        self.account_name_field.update()
        self.account_allocated_field.update()

    def refresh_accounts_list(self):
        self.accounts_list.controls.clear()
        for idx, account in enumerate(self.accounts):
            def remove_account(e, idx=idx):
                del self.accounts[idx]
                self.update_leftover(self.accounts)
                self.refresh_accounts_list()

            account_row = ft.Row(
                controls=[
                    ft.Text(f"{account['name']} ({account['type']}) - Allocated: ${account['total_allocated']}")
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            )
            self.accounts_list.controls.append(account_row)
        self.accounts_list.update()

    def update_leftover(self, accounts):
        """ Updates the leftover amount based on allocated amounts """
        total_allocated = sum(account["total_allocated"] for account in accounts)
        self.leftover_amount = self.leftover_amount - total_allocated

    def continue_to_db(self, e):
        print("Saving budget accounts to database:", self.accounts)
        self.user_data.save_budget_and_accounts(self.accounts)
        self.page.go("/dashboard")


        
