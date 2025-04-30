import flet as ft

class EditBudget(ft.AlertDialog):
    def __init__(self, Page, user_data, colors, on_close=None):
        super().__init__(modal=True, bgcolor=colors.BLUE_BACKGROUND)

        self.page = Page
        self.user_data = user_data
        self.colors = colors
        self.on_close = on_close

        self.initial_name = ""
        self.initial_amount = 0.0

        current_name = self.user_data.budget_name
        current_amount = self.user_data.budget_amount

        self.budget_name = ft.TextField(label="Budget Name", value=current_name)
        self.budget_amount = ft.TextField(
            label="Budget Amount", value=str(current_amount),
            keyboard_type=ft.KeyboardType.NUMBER
        )

        self.save_button = ft.TextButton(
            "Save Changes",
            on_click=self.prompt_confirmation,
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
            width=800,
            height=500,
            bgcolor=self.colors.GREY_BACKGROUND,
            border_radius=10,
            padding=20,
            alignment=ft.alignment.center,
            content=ft.Column(
                controls=[
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
                        controls=[self.save_button, cancel_button],
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
        self.budget_name.error_text = ""
        self.budget_amount.error_text = ""

        name = self.budget_name.value.strip()
        amount_str = self.budget_amount.value.strip()

        if not name:
            self.budget_name.error_text = "Budget name cannot be empty"
            self.budget_name.update()
            return

        try:
            amount = float(amount_str)
            if round(amount, 2) != amount:
                raise ValueError()
        except ValueError:
            self.budget_amount.error_text = "Enter a valid amount (up to 2 decimal places)"
            self.budget_amount.update()
            return

        if name == self.initial_name and amount == self.initial_amount:
            self.close_dialog()
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("No changes made."),
                bgcolor=self.colors.GREY_BACKGROUND
            )
            self.page.snack_bar.open = True
            self.page.update()
            return

        def on_confirm_update(e):
            print("Confirmed update, closing both dialogs...")

            # Close the confirmation dialog
            self.page.close(self.confirmation_dialog)

            # Close the edit budget dialog
            self.page.close(self)

            # Now update the budget data
            self.update_budget(name, amount)

            # Navigate to the accounts page
            self.page.go("/accounts")


        def on_cancel(e):
            self.confirmation_dialog.open = False
            self.page.dialog = None
            self.page.update()

        self.confirmation_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirm Update"),
            content=ft.Text("Are you sure you want to update this budget?"),
            actions=[
                ft.TextButton("Yes", on_click=on_confirm_update),
                ft.TextButton("Cancel", on_click=on_cancel),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            on_dismiss=on_cancel
        )

        self.page.dialog = self.confirmation_dialog
        self.page.open(self.confirmation_dialog)

    def update_budget(self, name, amount):
        print(f"Updating budget to {name}, {amount}")
        self.user_data.budget_name = name
        self.user_data.budget_amount = amount
        self.user_data.update_budget(name, amount)

        if self.on_close:
            self.on_close()

        self.page.snack_bar = ft.SnackBar(
            content=ft.Text("Budget updated successfully!"),
            bgcolor=self.colors.GREEN_BUTTON
        )
        self.page.snack_bar.open = True
        self.page.update()

