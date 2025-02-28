import flet as ft

class HistoryScene(ft.Container):
    def __init__(self, change_scene_callback, p_width, p_height, data_manager):
        super().__init__()
        self.change_scene_callback = change_scene_callback
        self.width = p_width
        self.height = p_height
        self.data_manager = data_manager
        self.sliders = {}
        self.text_fields = {}

        # Register as a listener for DataManager changes
        self.data_manager.add_listener(self.refresh_table)

        self.bgcolor = "#0d0d10"  # ✅ Dark background

        self.header = ft.Container(
            content=ft.Text("Accounts", size=24, weight="bold", color=ft.colors.WHITE),
            alignment=ft.alignment.center,
            padding=20
        )

        # Table container, starts empty
        self.table = ft.Column(spacing=10)

        # Main Layout
        self.content = ft.Column(
            controls=[
                self.header,
                self.table
            ],
            expand=True,  # ✅ Background for the entire layout
        )

        self.refresh_table()  # Initial load

    def refresh_ui(self):
        self.refresh_table()

    def refresh_table(self):
        """Updates the table dynamically whenever accounts are changed."""
        self.table.controls.clear()

        # Table Header
        self.table.controls.append(ft.Row([
            ft.Text("Account", weight="bold", width=150, color=ft.colors.WHITE),
            ft.Text("Balance", weight="bold", width=100, color=ft.colors.WHITE),
            ft.Text("Allocation", weight="bold", width=250, color=ft.colors.WHITE),
            ft.Text("", weight="bold", width=50)  # Moved delete button over
        ]))

        accounts = self.data_manager.list_accounts()
        if not accounts:
            self.table.controls.append(ft.Text("No accounts available.", italic=True, color=ft.colors.GREY_300))

        for account, balance in accounts.items():
            max_value = balance  # The slider max is the account balance

            # Create Slider (Start at Max Value)
            slider = ft.Slider(
                min=0, max=max_value, value=max_value,
                divisions=max_value if max_value > 0 else 1,
                on_change=lambda e, a=account: self.debounced_update_slider_value(e, a)
            )

            # Create Text Field (Start at Max Value)
            text_field = ft.TextField(
                value=str(max_value),
                width=70,
                text_align=ft.TextAlign.RIGHT,
                color=ft.colors.GREY_300,  # ✅ Grey text
                bgcolor="#0d0d10",  # ✅ Matches background
                on_blur=lambda e, a=account: self.update_text_value(e, a)
            )

            # Save references for updates
            self.sliders[account] = slider
            self.text_fields[account] = text_field

            # Delete Button (Now moved further right)
            delete_button = ft.IconButton(
                icon=ft.icons.DELETE,
                icon_color=ft.colors.RED_ACCENT,
                on_click=lambda e, a=account: self.delete_account(a)
            )

            # Add Row to Table
            self.table.controls.append(ft.Row([
                ft.Text(account, width=150, color=ft.colors.WHITE),
                ft.Text(f"${balance:.2f}", width=100, color=ft.colors.WHITE),
                ft.Row([slider, text_field], spacing=10, width=250),
                ft.Container(delete_button, alignment=ft.alignment.center_right, width=50)
            ]))

        if self.page:
            self.table.update()

    def debounced_update_slider_value(self, e, account):
        """Delays updating the text field to allow smooth slider movement."""
        if hasattr(self, "_slider_timer") and self._slider_timer is not None:
            self._slider_timer.cancel()

        import threading
        self._slider_timer = threading.Timer(0.2, lambda: self.update_slider_value(e, account))
        self._slider_timer.start()

    def update_slider_value(self, e, account):
        """Updates the text field when the slider moves."""
        new_value = round(e.control.value)
        self.text_fields[account].value = str(new_value)
        self.text_fields[account].update()

    def update_text_value(self, e, account):
        """Updates the slider when the text field is changed."""
        try:
            new_value = int(e.control.value)
            new_value = max(0, min(new_value, self.sliders[account].max))  # Clamp within limits
            self.sliders[account].value = new_value
            self.sliders[account].update()
        except ValueError:
            pass

    def delete_account(self, account):
        """Deletes an account and refreshes the table."""
        self.data_manager.remove_account(account)
        self.refresh_table()

    def get_content(self):
        """Returns the main scene content."""
        return self.content
