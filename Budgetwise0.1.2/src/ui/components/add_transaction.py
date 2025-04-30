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

        # Amount input
        self.amount_field = ft.TextField(label="Amount", width=400, keyboard_type=ft.KeyboardType.NUMBER)

        # Description input
        self.description_field = ft.TextField(label="Description", width=400)

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
            on_click=self.confirm_transaction,
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
        self.page.update()

    def did_mount(self):
        self.populate_vendor_dropdown()
        self.populate_account_dropdown()
        self.page.update()

    def populate_vendor_dropdown(self):
        vendors = self.vend_funcs.get_all_vendors()
        self.vendor_dropdown.options = [
            ft.dropdown.Option(key=vendor[0], text=vendor[1]) for vendor in vendors
        ]

        self.page.update()

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
        status = 1 if transaction_date <= date.today() else 2  # 1: Processed, 2: Scheduled

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
        self.page.update()
