import flet as ft
from datetime import date

class AddTransaction(ft.AlertDialog):
    def __init__(self, page, user_data, colors, trans_funcs, vend_funcs):
        super().__init__(modal=True, bgcolor=colors.GREY_BACKGROUND)

        self.page = page
        self.user_data = user_data
        self.colors = colors
        self.trans_funcs = trans_funcs  # Should be an instance of TransClass
        self.vend_funcs = vend_funcs
        self.refresh = None  # To be set externally

        self.selected_vendor = None
        self.selected_account = None

        self.update_trans = False
        self.transaction_id = None

        # Amount input
        self.amount_field = ft.TextField(
            label="Amount",
            label_style=ft.TextStyle(color=self.colors.BORDERBOX_COLOR), 
            text_style=ft.TextStyle(color=self.colors.TEXT_COLOR),
            hint_text="How much did you spend",
            hint_style=ft.TextStyle(color=self.colors.BLUE_BACKGROUND),
            focused_border_color=self.colors.BORDERBOX_COLOR, 
            width=400, 
            keyboard_type=ft.KeyboardType.NUMBER)

        # Description input
        self.description_field = ft.TextField(
            label="Description",
            label_style=ft.TextStyle(color=self.colors.BORDERBOX_COLOR), 
            text_style=ft.TextStyle(color=self.colors.TEXT_COLOR),
            hint_text="A short description",
            hint_style=ft.TextStyle(color=self.colors.BLUE_BACKGROUND),
            focused_border_color=self.colors.BORDERBOX_COLOR, 
            width=400)

        # Recurring checkbox
        self.recurring_checkbox = ft.Checkbox(label="Recurring")

        # Initialize the selected date to today’s date
        self.selected_date = date.today()

        # Date Picker Button (Opens the DatePicker dialog)
        self.date_button = ft.TextButton(
            f"Select Transaction Date: {self.selected_date.strftime('%m/%d/%Y')}",
            on_click=self.open_date_picker_dialog,
            width=400,
            style=ft.ButtonStyle(
                color={ft.ControlState.DEFAULT: self.colors.TEXT_COLOR},
                bgcolor={ft.ControlState.DEFAULT: self.colors.GREY_BACKGROUND},
                shape={ft.ControlState.DEFAULT: ft.RoundedRectangleBorder(radius=8)},
            ),
        )

        # Dropdowns
        self.vendor_dropdown = ft.Dropdown(
            label="Select Vendor", options=[], value=None, filled=True, width=400,
            on_change=lambda e: self.dropdown_changed(e, "vendor"),
        )

        self.account_dropdown = ft.Dropdown(
            label="Select Budget Account", options=[], value=None, filled=True, width=400,
            on_change=lambda e: self.dropdown_changed(e, "account"),
        )

        # Buttons
        self.confirm_button = ft.TextButton(
            "Add Transaction",
            on_click=self.save_transaction,
            style=ft.ButtonStyle(
                color={ft.ControlState.DEFAULT: self.colors.TEXT_COLOR},
                bgcolor={ft.ControlState.DEFAULT: self.colors.GREEN_BUTTON},
                shape={ft.ControlState.DEFAULT: ft.RoundedRectangleBorder(radius=8)},
            ),
        )

        cancel_button = ft.TextButton(
            "Cancel", on_click=self.close_dialog,
            style=ft.ButtonStyle(
                color={ft.ControlState.DEFAULT: self.colors.TEXT_COLOR},
                bgcolor={ft.ControlState.DEFAULT: self.colors.GREY_BACKGROUND},
                shape={ft.ControlState.DEFAULT: ft.RoundedRectangleBorder(radius=8)},
            ),
        )

        x_button = ft.IconButton(
            icon=ft.Icons.CLOSE,
            icon_color=self.colors.TEXT_COLOR,
            tooltip="Close",
            on_click=self.close_dialog,
            style=ft.ButtonStyle(
                padding=5,
                shape={ft.ControlState.DEFAULT: ft.RoundedRectangleBorder(radius=12)},
                bgcolor=self.colors.TRANSPARENT,
            )
        )

        self.content = ft.Container(
            width=600,
            height=600,
            bgcolor=self.colors.GREY_BACKGROUND,
            border_radius=10,
            padding=20,
            alignment=ft.alignment.center,
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[ft.Container(content=x_button, alignment=ft.alignment.top_right, padding=10)],
                        alignment=ft.MainAxisAlignment.END,
                    ),
                    ft.Text("Add New Transaction", size=22, weight=ft.FontWeight.BOLD, color=self.colors.TEXT_COLOR),
                    ft.Container(height=10),
                    self.vendor_dropdown,
                    self.account_dropdown,
                    self.amount_field,
                    self.description_field,
                    self.date_button,  # Use the button to open date picker
                    self.recurring_checkbox,
                    ft.Container(height=20),
                    ft.Row(
                        controls=[self.confirm_button, cancel_button],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True,
            ),
        )

    def open_date_picker_dialog(self, e):
        """Opens a DatePicker dialog to select a transaction date."""
        def handle_date_change(e):
            self.selected_date = e.control.value
            self.date_button.text = f"Select Transaction Date: {self.selected_date.strftime('%m/%d/%Y')}"
            self.page.update()
            self.close_date_picker_dialog()

        # Open DatePicker dialog from the existing page
        self.page.open(
            ft.DatePicker(
                value=self.selected_date,
                first_date=date(2000, 1, 1),
                last_date=date(2025, 12, 31),
                on_change=handle_date_change,
            )
        )

    def close_date_picker_dialog(self):
        """Closes the DatePicker dialog."""
        self.page.update()

    def open_and_refresh(self):
        """Refreshes the dropdowns and opens the dialog."""
        self.populate_vendor_dropdown()
        self.populate_account_dropdown()
        self.open = True
        self.update_trans = False
        self.page.update()
    
    def load_transaction_info(self, transaction):
        """
        Populate the dialog fields with an existing transaction's data.
        
        Expected keys in transaction:
            - transaction_id
            - vendor_id
            - account_id
            - amount
            - description
            - transaction_date (formatted as "YYYY-MM-DD")
            - recurring (0 or 1)
        """
        # Save the transaction ID for later update operations.
        self.transaction_id = transaction["transaction_id"]

        # Fill in the amount and description.
        self.amount_field.value = str(transaction["amount"])
        self.description_field.value = transaction["description"]
        
        # Set the recurring checkbox (ensure it's interpreted as a boolean)
        self.recurring_checkbox.value = bool(transaction["recurring"])

        # Convert the transaction date string to a date object.
        try:
            from datetime import datetime
            trans_date = datetime.strptime(transaction["transaction_date"], "%Y-%m-%d").date()
        except Exception as e:
            trans_date = date.today()
        self.selected_date = trans_date
        self.date_button.text = f"Select Transaction Date: {self.selected_date.strftime('%m/%d/%Y')}"
        
        # Set the vendor and account dropdowns.
        # Note: if your dropdown values are strings, convert the IDs to strings.
        self.vendor_dropdown.value = str(transaction["vendor_id"])
        self.account_dropdown.value = str(transaction["account_id"])
        
        # Ensure the dialog reflects the updated information.
        self.page.update()


    def did_mount(self):
        self.populate_vendor_dropdown()
        self.populate_account_dropdown()
        self.page.update()

    def populate_vendor_dropdown(self):
        self.user_id = self.user_data.user_id
        vendors = self.vend_funcs.get_all_vendors(self.user_id)
        self.vendor_dropdown.options = [
            ft.dropdown.Option(key=vendor[0], text=vendor[1]) for vendor in vendors
        ]

        self.page.update()

    def save_transaction(self, e = None):
        if self.update_trans:
            # Call the update method if in update mode
            self.update_transaction(e)
        else:
            # Otherwise, create a new transaction
            self.confirm_transaction(e)


    def populate_account_dropdown(self):
        accounts = self.user_data.get_all_budget_accounts()
        self.account_dropdown.options = [
            ft.dropdown.Option(key=acc[0], text=acc[1]) for acc in accounts
        ] if accounts else [ft.dropdown.Option(key=None, text="No Accounts Available")]

        self.page.update()

    def dropdown_changed(self, e, dropdown_type):
        if dropdown_type == "vendor":
            self.selected_vendor = e.control.value
        elif dropdown_type == "account":
            self.selected_account = e.control.value
        self.page.update()

    def confirm_transaction(self, e):
        # Input validation
        if not all([self.selected_vendor, self.selected_account, self.amount_field.value]):
            self.show_snackbar("Please fill all required fields.", self.colors.ERROR_RED)
            return

        try:
            amount = float(self.amount_field.value)
        except ValueError:
            self.show_snackbar("Amount must be a number.", self.colors.ERROR_RED)
            return

        description = self.description_field.value or ""
        recurring = self.recurring_checkbox.value
        transaction_date = self.selected_date

        # Determine status based on the transaction date
        status = 2 if transaction_date.date() <= date.today() else 1  # 2: Processed, 1: Pending



        print(f"Inserting into transactions: user_id: {self.selected_account} vendor_ID: {self.selected_vendor} transaction amount: {amount} description (optional): {description} recurring: {recurring} date: {transaction_date} status: {status}")
        # Perform transaction insert
        success = self.trans_funcs.create_transaction(
            account_id=self.selected_account,
            vendor_id=self.selected_vendor,
            transAmount=amount,
            description=description,
            recurring=recurring,
            transaction_date=transaction_date.strftime("%Y-%m-%d"),
            status=status,
        )


        if success:
            self.show_snackbar("Transaction added successfully.", self.colors.GREEN_BUTTON)
            self.close_dialog()
            if self.refresh:
                self.refresh()
        else:
            self.show_snackbar("Failed to add transaction.", self.colors.ERROR_RED)

    def show_snackbar(self, message, color):
        self.page.snack_bar = ft.SnackBar(content=ft.Text(message), bgcolor=color)
        self.page.snack_bar.open = True
        self.page.update()

    def close_dialog(self, e=None):
        self.open = False
        self.update_trans = False
        self.reset_dialog_fields()
        self.page.update()
    
    def update_transaction(self, e):
        # Validate input fields.
        print("update_transaction called")
        if not all([self.selected_vendor, self.selected_account, self.amount_field.value]):
            print(self.selected_vendor," ",self.selected_account," ", self.amount_field.value)
            self.show_snackbar("Please fill all required fields.", self.colors.ERROR_RED)
            return

        try:
            amount = float(self.amount_field.value)
        except ValueError:
            self.show_snackbar("Amount must be a number.", self.colors.ERROR_RED)
            return

        description = self.description_field.value or ""
        recurring = self.recurring_checkbox.value
        transaction_date = self.selected_date
        # Determine a status value (this logic is carried over from confirm_transaction)
        status = 2 if transaction_date <= date.today() else 1
        print(self.transaction_id)
        # Ensure the transaction_id is set (this should have been set when opening the dialog in edit mode)
        if not hasattr(self, "transaction_id") or self.transaction_id is None:
            self.show_snackbar("No transaction selected for update.", self.colors.ERROR_RED)
            return

        print(f"Updating transaction: {self.transaction_id}, "
            f"Account: {self.selected_account}, Vendor: {self.selected_vendor}, "
            f"Amount: {amount}, Description: {description}, Recurring: {recurring}, "
            f"Date: {transaction_date}, Status: {status}")

        # Call the update_transaction method in trans_funcs
        success = self.trans_funcs.update_transaction(
            transaction_id=self.transaction_id,
            account_id=self.selected_account,
            vendor_id=self.selected_vendor,
            transAmount=amount,
            description=description,
            recurring=recurring,
            transaction_date=transaction_date.strftime("%Y-%m-%d"),
            status=status,
        )

        if success:
            self.show_snackbar("Transaction updated successfully.", self.colors.GREEN_BUTTON)
            self.close_dialog()
            if self.refresh:
                self.refresh()  # Refresh the list of transactions or other related data.
        else:
            self.show_snackbar("Failed to update transaction.", self.colors.ERROR_RED)

    def load_transaction_info(self, transaction_row):
        """
        Populate the dialog fields with an existing transaction's data,
        expecting transaction_row to be in the format:
        [transaction_id, budget_account_name, budget_account_id, amount, description, transaction_date, recurring, vendor_id]
        """
        self.populate_vendor_dropdown()
        self.populate_account_dropdown()

        transaction_dict = {
            "transaction_id": transaction_row[0],
            "account_id": transaction_row[2],
            "vendor_id": transaction_row[7],  # Using index 7 for vendor_id as appended
            "amount": transaction_row[3],
            "description": transaction_row[4],
            "transaction_date": transaction_row[5],
            "recurring": transaction_row[6],
            "budget_account_name": transaction_row[1],
        }
        
        # Now pre-populate your fields using transaction_dict
        self.transaction_id = transaction_dict["transaction_id"]  # Save for updates.
        self.amount_field.value = str(transaction_dict["amount"])
        self.description_field.value = transaction_dict["description"]
        self.recurring_checkbox.value = bool(transaction_dict["recurring"])

        # Convert transaction date from string to date object
        try:
            from datetime import datetime
            trans_date = datetime.strptime(transaction_dict["transaction_date"], "%Y-%m-%d").date()
        except Exception:
            trans_date = date.today()
        self.selected_date = trans_date
        self.date_button.text = f"Select Transaction Date: {self.selected_date.strftime('%m/%d/%Y')}"
        
        # Set the dropdown values.
        # Also update the instance variables that store the currently selected IDs.
        self.vendor_dropdown.value = str(transaction_dict["vendor_id"])
        self.account_dropdown.value = str(transaction_dict["account_id"])
        self.selected_vendor = transaction_dict["vendor_id"]
        self.selected_account = transaction_dict["account_id"]
        
        self.update_trans = True
        self.page.update()

    def reset_dialog_fields(self):
        self.amount_field.value = ""
        self.description_field.value = ""
        self.recurring_checkbox.value = False
        self.selected_date = date.today()
        self.date_button.text = f"Select Transaction Date: {self.selected_date.strftime('%m/%d/%Y')}"
        self.vendor_dropdown.value = None
        self.account_dropdown.value = None
        self.selected_vendor = None
        self.selected_account = None
        self.update_trans = False
        self.transaction_id = None


