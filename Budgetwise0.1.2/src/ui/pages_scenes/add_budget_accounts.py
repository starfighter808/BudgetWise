from time import sleep
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

        # Budget Information Display
        self.budget_name_display = ft.Text(value="", size=16, color=colors.TEXT_COLOR)
        self.budget_amount_display = ft.Text(value="", size=16, color=colors.TEXT_COLOR)
        self.remaining_amount_display = ft.Text(value="", size=16, color=colors.TEXT_COLOR)

        # Create Account Section
        self.create_account_text = ft.Text("Create account:", weight=ft.FontWeight.BOLD, color=colors.TEXT_COLOR)
        self.account_name_field = ft.TextField(label="Account Name")
        self.account_allocated_field = ft.TextField(label="Account Allocated", keyboard_type=ft.KeyboardType.NUMBER)
        self.description_field = ft.TextField(label="Description", multiline=True, min_lines=1, max_lines=4)
        self.add_account_button = ft.ElevatedButton("Add Account", on_click=self.add_account)

        # Added Accounts Section
        self.added_accounts_text = ft.Text("Added accounts:", weight=ft.FontWeight.BOLD, color=colors.TEXT_COLOR)
        self.accounts_list_view = ft.ListView(
            expand=True,
            spacing=5,
            padding=5,
            auto_scroll=False,
            height=150
        )

        # Continue Button
        self.continue_button = ft.ElevatedButton("Continue", on_click=self.continue_to_db)
        self.previous_button = ft.TextButton("Previous?", on_click=lambda e: self.page.go("/create_budget"))

        # Layout
        self.controls = [
            ft.Container(
                expand=True,
                bgcolor=colors.GREY_BACKGROUND,
                border_radius=10,
                padding=20,
                height = 800,
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.START,
                    spacing=15,
                    controls=[
                        ft.Row(
                            [
                                ft.Text("Budget Name:", weight=ft.FontWeight.BOLD, color=colors.TEXT_COLOR),
                                self.budget_name_display,
                                ft.VerticalDivider(),
                                ft.Text("Budget Amount:", weight=ft.FontWeight.BOLD, color=colors.TEXT_COLOR),
                                self.budget_amount_display,
                                ft.VerticalDivider(),
                                ft.Text("Remaining/Leftover amount:", weight=ft.FontWeight.BOLD, color=colors.TEXT_COLOR),
                                self.remaining_amount_display,
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_AROUND
                        ),
                        ft.Divider(height=20, color=colors.TEXT_COLOR),
                        self.create_account_text,
                        ft.Row(
                            [
                                ft.Container(self.account_name_field, expand=True),
                            ],
                            spacing=10
                        ),
                        ft.Row(
                            [
                                ft.Container(self.account_allocated_field, expand=True),
                            ],
                            spacing=10
                        ),
                        self.description_field,
                        ft.Row(
                            [
                                ft.Container(),  # Spacer
                                self.add_account_button,
                            ],
                            alignment=ft.MainAxisAlignment.START
                        ),
                        ft.Divider(height=20, color=colors.TEXT_COLOR),
                        self.added_accounts_text,
                        ft.Container(
                            content=self.accounts_list_view,
                            height=200,
                            border=ft.border.all(1, colors.TEXT_COLOR),
                            padding=10,
                        ),
                        ft.Divider(height=20, color=colors.TEXT_COLOR),
                        ft.Row(
                            [
                                self.previous_button,
                                ft.Container(expand=True),
                                self.continue_button,
                            ],
                            alignment=ft.MainAxisAlignment.START
                        ),
                    ]
                )
            )
        ]

    def did_mount(self):
        if not self.user_data or not hasattr(self.user_data, "budget_name") or not hasattr(self.user_data, "budget_amount"):
            print("Budget data not found, redirecting user to /create_budget")
            self.page.go("/create_budget")
            return

        self.budget_name_display.value = self.user_data.budget_name
        self.budget_amount_display.value = f"${self.user_data.budget_amount}"
        self.leftover_amount = self.user_data.budget_amount
        self.remaining_amount_display.value = f"${self.leftover_amount}"

        self.budget_name_display.update()
        self.budget_amount_display.update()
        self.remaining_amount_display.update()

    def add_account(self, e):
        name = self.account_name_field.value.strip()
        allocated_str = self.account_allocated_field.value.strip()
        description = self.description_field.value.strip()

        # Reset error states
        self.account_name_field.error_text = None
        self.account_allocated_field.error_text = None

        # Validate fields
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

        # Add account
        account = {
            "name": name,
            "total_allocated": allocated,
            "current_amount": allocated,
            "savings_goal": 0.0,
            "description": description,
        }
        self.accounts.append(account)
        self.update_leftover(self.accounts)
        self.refresh_accounts_list()

        # Clear input fields
        self.account_name_field.value = ""
        self.account_allocated_field.value = ""
        self.description_field.value = ""
        self.account_name_field.update()
        self.account_allocated_field.update()
        self.description_field.update()

    def refresh_accounts_list(self):
        self.accounts_list_view.controls.clear()

        for idx, account in enumerate(self.accounts):
            def remove_account(e, idx=idx):
                del self.accounts[idx]
                self.update_leftover(self.accounts)
                self.refresh_accounts_list()

            account_row = ft.Row(
                controls=[
                    ft.Text(f"{account['name']} {account['total_allocated']}", expand=True),
                    ft.IconButton(ft.Icons.DELETE, on_click=remove_account)
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            )
            self.accounts_list_view.controls.append(account_row)

        self.accounts_list_view.update()

    def update_leftover(self, accounts):
        total_allocated = sum(account["total_allocated"] for account in accounts)
        self.leftover_amount = self.user_data.budget_amount - total_allocated
        self.remaining_amount_display.value = f"${self.leftover_amount}"
        self.remaining_amount_display.update()

    def continue_to_db(self, e):
        if hasattr(self.user_data, 'budget_id'):
            budget_id = self.user_data.budget_id
            if self.user_data.add_budget_accounts(budget_id, self.accounts):
                print("Budget accounts saved successfully!")
                self.page.go("/dashboard")
            else:
                print("Failed to save budget accounts.")
        else:
            print("Error: Budget ID not found.")
