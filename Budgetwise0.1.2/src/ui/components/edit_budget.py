import flet as ft

class EditBudget(ft.AlertDialog):
    def __init__(self, user_data, colors, on_close=None):
        super().__init__(modal=True, bgcolor=colors.BLUE_BACKGROUND)

        self.user_data = user_data
        self.colors = colors
        self.on_close = on_close

        self.initial_name = ""
        self.initial_amount = 0.0

        # Prefill with current budget data
        current_name = self.user_data.budget_name
        current_amount = self.user_data.budget_amount

        self.budget_name = ft.TextField(label="Budget Name", value=current_name)
        self.budget_amount = ft.TextField(label="Budget Amount", value=str(current_amount), keyboard_type=ft.KeyboardType.NUMBER)

        # Save button
        self.save_button = ft.TextButton(
            "Save Changes",
            on_click=self.prompt_confirmation,  # Binding the correct click handler
            style=ft.ButtonStyle(
                color={ft.ControlState.FOCUSED: self.colors.GREEN_BUTTON, ft.ControlState.DEFAULT: self.colors.TEXT_COLOR},
                bgcolor={ft.ControlState.FOCUSED: self.colors.GREEN_BUTTON, "": self.colors.GREEN_BUTTON},
                elevation={"pressed": 0, "": 2},
                animation_duration=300,
                side={ft.ControlState.DEFAULT: ft.BorderSide(1, self.colors.GREEN_BUTTON)},
                shape={ft.ControlState.DEFAULT: ft.RoundedRectangleBorder(radius=8)},
            ),
        )

        cancel_button = ft.TextButton(
            "Cancel",
            on_click=self.close_dialog,
            style=ft.ButtonStyle(
                color={ft.ControlState.DEFAULT: self.colors.TEXT_COLOR},
                bgcolor={ft.ControlState.DEFAULT: self.colors.GREY_BACKGROUND},
                shape={ft.ControlState.DEFAULT: ft.RoundedRectangleBorder(radius=8)},
            ),
        )

        x_button = ft.IconButton(
            icon=ft.icons.CLOSE,
            icon_color=self.colors.TEXT_COLOR,
            tooltip="Close",
            on_click=self.close_dialog,
            style=ft.ButtonStyle(
                padding=5,
                shape={ft.ControlState.DEFAULT: ft.RoundedRectangleBorder(radius=12)},
                bgcolor=self.colors.TRANSPARENT,  # Transparent background
            )
        )

        # Adjusted content layout to ensure buttons are not overlapping
        self.content = ft.Container(
            width=800,
            height=500,  # Adjusted height to fit the content better
            bgcolor=self.colors.GREY_BACKGROUND,
            border_radius=10,
            padding=20,
            alignment=ft.alignment.center,
            content=ft.Column(
                controls=[
                    # Close button on the right top corner
                    ft.Row(
                        controls=[
                            ft.Container(
                                content=x_button,
                                alignment=ft.alignment.top_right,
                                padding=10
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.END,
                        expand=False,
                    ),
                    ft.Column(
                        controls=[
 
                            ft.Text("Edit Budget", text_align=ft.TextAlign.CENTER, size=24, weight=ft.FontWeight.BOLD, color=self.colors.TEXT_COLOR),
                            self.budget_name,
                            self.budget_amount,
                            
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        expand=True,
                    ),
                    ft.Row(
                        controls=[
                            self.save_button,  # Save button below the inputs
                            cancel_button,  # Cancel button placed below the save button
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        expand=True,
                    ),
                ]
            )
        )

    def open_dialog(self):
        print("Opening dialog...")
        current_name = self.user_data.budget_name
        current_amount = self.user_data.budget_amount
        self.initial_name = current_name
        self.initial_amount = float(current_amount)

        print(f"Initial name: {self.initial_name}, initial amount: {self.initial_amount}")

        self.budget_name.value = current_name
        self.budget_amount.value = str(current_amount)

        self.open = True
        self.page.dialog = self
        self.page.update()

    def close_dialog(self, e=None):
        print("Closing dialog...")
        self.open = False
        self.page.dialog = None
        self.page.update()

    def prompt_confirmation(self, e):
        print("Save button clicked!")
        # Reset any previous error state
        self.budget_name.error_text = ""
        self.budget_amount.error_text = ""

        name = self.budget_name.value.strip()
        amount_str = self.budget_amount.value.strip()

        print(f"Entered name: {name}, entered amount: {amount_str}")

        # Validate name
        if not name:
            print("Budget name is empty!")
            self.budget_name.error_text = "Budget name cannot be empty"
            self.budget_name.update()
            return

        # Validate amount
        try:
            amount = float(amount_str)
            if round(amount, 2) != amount:
                print(f"Invalid amount: {amount_str}")
                raise ValueError()
        except ValueError:
            print("Amount is invalid!")
            self.budget_amount.error_text = "Enter a valid amount (up to 2 decimal places)"
            self.budget_amount.update()
            return

        # Check if changes actually occurred
        if name == self.initial_name and amount == self.initial_amount:
            print("No changes detected.")
            self.close_dialog()
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("No changes made."),
                bgcolor=self.colors.GREY_BACKGROUND
            )
            self.page.snack_bar.open = True
            self.page.update()
            return

        def on_confirm_update(_):
            print("Confirming update...")
            self.page.dialog = None  # Close confirmation popup
            self.page.update()
            self.update_budget(name, amount)

        def on_cancel(_):
            print("Canceling update...")
            self.page.dialog = None
            self.page.update()

        confirmation_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirm Update", size=20, weight=ft.FontWeight.BOLD),
            content=ft.Text("Are you sure you want to update this budget?"),
            actions=[
                ft.TextButton("Cancel", on_click=on_cancel),
                ft.TextButton("Yes", on_click=on_confirm_update),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        self.page.dialog = confirmation_dialog
        confirmation_dialog.open = True
        self.page.update()

    def update_budget(self, name, amount):
        print(f"Updating budget to {name}, {amount}")
        # Update data and database
        self.user_data.budget_name = name
        self.user_data.budget_amount = amount
        self.user_data.update_budget(name, amount)

        # Close the edit dialog
        self.close_dialog()

        # Refresh main UI
        if self.on_close:
            self.on_close()

        # Snackbar confirmation
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text("Budget updated successfully!"),
            bgcolor=self.colors.GREEN_BUTTON
        )
        self.page.snack_bar.open = True
        self.page.update()
