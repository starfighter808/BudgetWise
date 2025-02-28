import flet as ft

class AccountScene(ft.Container):
    """
    Represents the scene that manages accounts, allowing users to view, edit, and delete their accounts.
    It displays a table with sliders for adjusting account allocations and text fields to show their current values.

    Attributes:
        change_scene_callback (function): Callback function to change scenes.
        width (float): Width of the scene container.
        height (float): Height of the scene container.
        show_budget_creation_form (function): Function to show the budget creation form.
        budget_creation_form (object): Instance of the budget creation form.
        data_manager (object): Instance of the DataManager for managing account data.
        sliders (dict): Dictionary to hold sliders for each account.
        text_fields (dict): Dictionary to hold text fields for each account.
    """
    
    def __init__(self, change_scene_callback, p_width, p_height, show_budget_creation_form, budget_creation_form, data_manager):
        """
        Initializes the AccountScene with necessary parameters and sets up the layout.

        Arguments:
            change_scene_callback (function): Function to switch between scenes.
            p_width (float): The width of the scene container.
            p_height (float): The height of the scene container.
            show_budget_creation_form (function): Callback to show the budget creation form.
            budget_creation_form (object): Instance of the budget creation form.
            data_manager (object): DataManager instance for managing account data.
        """
        super().__init__()

        # Initialize attributes based on parameters
        self.change_scene_callback = change_scene_callback
        self.width = p_width
        self.height = p_height
        self.show_budget_creation_form = show_budget_creation_form
        self.budget_creation_form = budget_creation_form
        self.data_manager = data_manager
        self.sliders = {}  # Dictionary to store sliders for each account
        self.text_fields = {}  # Dictionary to store text fields for each account

        # Register as a listener for any updates in DataManager
        self.data_manager.add_listener(self.refresh_table)

        # Set background color for the scene
        self.bgcolor = "#0d0d10" 

        # **Header**: Title for the scene
        self.header = ft.Container(
            content=ft.Text("Accounts", size=24, weight="bold", color=ft.colors.WHITE),
            alignment=ft.alignment.center,
            padding=20
        )

        # **Table container**: This will hold the rows for each account
        self.table = ft.Column(spacing=10)

        # **Main Layout**: Organize the header and table into a container
        self.content = ft.Container(
            content=ft.Column(
                controls=[
                    self.header,  # Title
                    self.table  # Table holding account data
                ],
                expand=True
            ),
            bgcolor="#0d0d10"  # Dark background for the entire container
        )

        # Initial call to populate the table
        self.refresh_table()  # Load and display the current account data

    def refresh_table(self):
        """
        Updates the table whenever account data changes. This method:
        - Clears the current table.
        - Adds rows for each account with sliders, text fields, and delete buttons.
        """
        self.table.controls.clear()  # Clear the table contents

        # **Table Header**: Add column headers for the table
        self.table.controls.append(ft.Row([
            ft.Text("Account", weight="bold", width=150, color=ft.colors.WHITE),
            ft.Text("Balance", weight="bold", width=100, color=ft.colors.WHITE),
            ft.Text("Allocation", weight="bold", width=250, color=ft.colors.WHITE),
            ft.Text("", weight="bold", width=50)  # Empty column for delete button
        ]))

        # Retrieve the list of accounts from the data manager
        accounts = self.data_manager.list_accounts()

        # Handle the case where no accounts are available
        if not accounts:
            self.table.controls.append(ft.Text("No accounts available.", italic=True, color=ft.colors.GREY_300))

        # **Table Rows**: Add a row for each account with a slider, text field, and delete button
        for account, balance in accounts.items():
            max_value = balance  # Set slider max value equal to the account balance

            # **Slider**: A slider for allocating budget to the account
            slider = ft.Slider(
                min=0, max=max_value, value=max_value,  # Default to max value
                divisions=max_value if max_value > 0 else 1,  # Ensure proper slider divisions
                on_change=lambda e, a=account: self.debounced_update_slider_value(e, a)  # Update on change
            )

            # **Text Field**: A field displaying the account value (linked to the slider)
            text_field = ft.TextField(
                value=str(max_value),  # Display the current balance
                width=70,
                text_align=ft.TextAlign.RIGHT,
                color=ft.colors.GREY_300,
                bgcolor="#0d0d10",  # Dark background to match the theme
                on_blur=lambda e, a=account: self.update_text_value(e, a)  # Update when text field loses focus
            )

            # Save the references to sliders and text fields for later use
            self.sliders[account] = slider
            self.text_fields[account] = text_field

            # **Delete Button**: A button to delete the account
            delete_button = ft.IconButton(
                icon=ft.icons.DELETE,
                icon_color=ft.colors.RED_ACCENT,
                on_click=lambda e, a=account: self.delete_account(a)  # Delete on click
            )

            # Add the account row to the table
            self.table.controls.append(ft.Row([
                ft.Text(account, width=150, color=ft.colors.WHITE),  # Account name
                ft.Text(f"${balance:.2f}", width=100, color=ft.colors.WHITE),  # Account balance
                ft.Row([slider, text_field], spacing=10, width=250),  # Slider and text field
                ft.Container(delete_button, alignment=ft.alignment.center_right, width=50)  # Delete button
            ]))

        # Ensure the table updates visually if the page is active
        if self.page:
            self.table.update()

    def debounced_update_slider_value(self, e, account):
        """
        Delays the slider value update to avoid excessive updates during smooth adjustments.

        Arguments:
            e (Event): The event triggered when the slider value changes.
            account (str): The account associated with the slider.
        """
        if hasattr(self, "_slider_timer") and self._slider_timer is not None:
            self._slider_timer.cancel()  # Cancel any previous timer to avoid stacking events

        # Use threading to delay the update by 200 milliseconds
        import threading
        self._slider_timer = threading.Timer(0.2, lambda: self.update_slider_value(e, account))
        self._slider_timer.start()

    def update_slider_value(self, e, account):
        """
        Updates the text field value when the slider is adjusted.

        Arguments:
            e (Event): The event triggered when the slider value changes.
            account (str): The account associated with the slider.
        """
        new_value = round(e.control.value)  # Round the slider value to the nearest integer
        self.text_fields[account].value = str(new_value)  # Update the text field with the new value
        self.text_fields[account].update()  # Refresh the text field UI

    def update_text_value(self, e, account):
        """
        Updates the slider value when the corresponding text field value changes.

        This method ensures that the text field value is within the valid range for the slider.

        Arguments:
            e (Event): The event triggered when the text field loses focus.
            account (str): The account associated with the text field.
        """
        try:
            new_value = int(e.control.value)  # Try to convert the text field value to an integer
            new_value = max(0, min(new_value, self.sliders[account].max))  # Clamp the value within valid range
            self.sliders[account].value = new_value  # Update the slider value
            self.sliders[account].update()  # Refresh the slider UI
        except ValueError:
            pass  # Ignore invalid input

    def delete_account(self, account):
        """
        Deletes the specified account and refreshes the table to reflect the change.

        Arguments:
            account (str): The account to be deleted.
        """
        self.data_manager.remove_account(account)  # Remove the account from DataManager
        self.refresh_table()  # Refresh the table to update the displayed accounts

    def get_content(self):
        """
        Returns the main content container of the scene.

        Returns:
            ft.Container: The main container holding the UI elements for the account scene.
        """
        return self.content  # Return the content container
