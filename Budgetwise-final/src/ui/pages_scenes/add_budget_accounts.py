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
        self.account_name_field = ft.TextField(
            label="Account Name",
            label_style=ft.TextStyle(color=self.colors.BORDERBOX_COLOR), 
            text_style=ft.TextStyle(color=self.colors.TEXT_COLOR),
            hint_text="Enter your account name",
            hint_style=ft.TextStyle(color=self.colors.BLUE_BACKGROUND),
            focused_border_color=self.colors.BORDERBOX_COLOR
            )
        self.account_allocated_field = ft.TextField(
            label="Account Allocated", 
            label_style=ft.TextStyle(color=self.colors.BORDERBOX_COLOR), 
            keyboard_type=ft.KeyboardType.NUMBER,
            text_style=ft.TextStyle(color=colors.TEXT_COLOR),
            hint_text="Enter your allocated amount",
            hint_style=ft.TextStyle(color=colors.BLUE_BACKGROUND),
            focused_border_color= self.colors.BORDERBOX_COLOR)
        self.description_field = ft.TextField(
            label="Description", 
            label_style=ft.TextStyle(color=self.colors.BORDERBOX_COLOR),  # sets the label color
            multiline=True,
            min_lines=1,
            max_lines=4,
            text_style=ft.TextStyle(color=colors.TEXT_COLOR),
            hint_text="What is this account for?",
            hint_style=ft.TextStyle(color=colors.BLUE_BACKGROUND),
            focused_border_color= self.colors.BORDERBOX_COLOR )
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
                # --- Inner function definition for remove_account remains the same ---
                def remove_account(e, idx=idx):
                    # Make sure the index is captured correctly for the lambda/closure
                    current_index = idx
                    # Find the account dictionary to remove based on its content if index causes issues,
                    # though direct indexing should work if the list isn't modified elsewhere unexpectedly.
                    # account_to_remove = self.accounts[current_index] # Get the account before deleting
                    del self.accounts[current_index]
                    self.update_leftover(self.accounts)
                    self.refresh_accounts_list() # Re-render the list

                # --- Create a Column to hold Name/Amount and Description ---
                account_details_column = ft.Column(
                    [
                        # Line 1: Account Name and Formatted Amount
                        ft.Text(
                            f"{account['name']} - ${account.get('total_allocated', 0):.2f}", # Use .get for safety and format amount
                            weight=ft.FontWeight.BOLD, # Make name/amount stand out
                            color=self.colors.TEXT_COLOR # Ensure text color
                        ),
                        # Line 2: Description (only if it exists)
                        ft.Text(
                            account.get('description', 'No description provided'), # Use .get for safety
                            size=12,              # Slightly smaller text for description
                            italic=True,
                            color=self.colors.TEXT_COLOR # Ensure text color
                        ) if account.get('description') else ft.Text( # Only add if description exists
                            "No description",
                            size=12,
                            italic=True,
                            color=self.colors.BORDERBOX_COLOR # Maybe different color for placeholder
                        )
                    ],
                    spacing=2, # Adjust spacing between lines if needed
                    alignment=ft.MainAxisAlignment.START,
                    horizontal_alignment=ft.CrossAxisAlignment.START
                )

                # --- Create the Row containing the details column and the delete button ---
                account_row = ft.Row(
                    controls=[
                        # Use the Column created above
                        ft.Container(account_details_column, expand=True, padding=ft.padding.only(right=10)), # Expand details, add padding
                        # Delete Button
                        ft.IconButton(
                            ft.Icons.DELETE_OUTLINE, # Use outline icon?
                            on_click=lambda e, captured_idx=idx: remove_account(e, captured_idx), # Ensure index is captured at creation time
                            tooltip="Remove Account"
                        )
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER # Center items vertically in the row
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
                self.account_name_field.value = ""
                self.account_allocated_field.value = ""
                self.description_field.value = ""
                self.page.go("/dashboard")
            else:
                print("Failed to save budget accounts.")
        else:
            print("Error: Budget ID not found.")
