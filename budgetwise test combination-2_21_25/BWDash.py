from BWForms import BudgetCreationForm
from BWMenu import MenuBar
import functools 
import flet as ft
import threading

class DashboardScene(ft.Container):
    def __init__(self, change_scene_callback, p_width, p_height, show_budget_creation_form, budget_creation_form, data_manager):
        super().__init__()
        self.change_scene_callback = change_scene_callback
        self.p_width = p_width
        self.p_height = p_height
        self.show_budget_creation_form = show_budget_creation_form
        self.budget_creation_form = budget_creation_form
        self.data_manager = data_manager
        self.sliders = {}
        self.text_fields = {}
        self.bgcolor="#0d0d10"

         # **Left Table - Dynamic Values**
        self.daily_value_text = ft.Text("Daily: $0.00")  # Starts at 0
        self.total_accounts_text = ft.Text("Total Accounts: $0.00")
        self.total_budget_text = ft.Text("Total Budget: $0.00")
        # Dashboard Header
        self.header = ft.Container(
            content=ft.Text("Dashboard", size=24, weight="bold"),
            alignment=ft.alignment.center,
            padding=20
        )

        # Left Table Placeholder
        self.left_table = ft.Column([
            ft.Text("Account Summary", size=18, weight="bold"),
            self.daily_value_text,
            self.total_accounts_text,
            self.total_budget_text
        ])

        # Middle Container - Dynamic Itemized List
        self.middle_container = ft.Column(
            controls=[ft.Text("Itemized List", size=18, weight="bold")],
            scroll=ft.ScrollMode.AUTO,
            expand=True
        )

        # Right Container - Dynamic Sliders
        self.slider_container = ft.Column(
            controls=[ft.Text("Budget Sliders", size=18, weight="bold")],
            scroll=ft.ScrollMode.AUTO,
            expand=True
        )

        # ✅ Create New Budget Button at the Bottom
        self.create_budget_button = ft.Container(
            content=ft.ElevatedButton(
                text="Create New Budget",
                on_click=self.show_budget_form,  # Calls method to show budget form
                bgcolor=ft.colors.BLUE_500,
                color=ft.colors.WHITE
            ),
            alignment=ft.alignment.center,
            padding=20
        )

        # Main Layout with fixed width constraints
        self.content = ft.Container(
            content=ft.Column(
                controls=[
                    self.header,
                    ft.Row(
                        controls=[
                            ft.Container(content=self.left_table, width=p_width * 0.25, expand=True),
                            ft.Container(content=self.middle_container, width=p_width * 0.50, expand=True),
                            ft.Container(content=self.slider_container, width=p_width * 0.25, expand=True)
                        ],
                        expand=True,
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    self.create_budget_button  # ✅ Add button at the bottom
                ],
                expand=True
            ),
            width=p_width,
            height=p_height,
            padding=20
        )

    def did_mount(self):
        """Called when the dashboard is mounted to register for data updates."""
        self.data_manager.add_listener(self.refresh_itemized_list)
        self.data_manager.add_listener(self.refresh_sliders)
        self.data_manager.add_listener(self.refresh_left_table)

        self.refresh_itemized_list()
        self.refresh_sliders()
        self.refresh_left_table()
    
    def refresh_ui(self):
        """Refreshes all dynamic elements when the scene is switched to."""
        self.refresh_itemized_list()
        self.refresh_sliders()
        self.refresh_left_table()
    
    def refresh_left_table(self):
        """Updates the left container dynamically based on DataManager."""
        total_accounts = sum(self.data_manager.list_accounts().values())
        total_daily = self.calculate_daily_value()  # Get daily spending

        self.daily_value_text.value = f"Daily: ${total_daily:.2f}"
        self.total_accounts_text.value = f"Total Accounts: ${total_accounts:.2f}"
        self.total_budget_text.value = f"Total Budget: ${total_accounts:.2f}"

        self.daily_value_text.update()
        self.total_accounts_text.update()
        self.total_budget_text.update()

    def refresh_itemized_list(self):
        """Updates the middle container whenever DataManager changes."""
        if not self.middle_container.page:
            return  # Prevent update if not added to the page

        self.middle_container.controls.clear()
        self.middle_container.controls.append(ft.Text("Itemized List", size=18, weight="bold"))

        for account, value in self.data_manager.list_accounts().items():
            self.middle_container.controls.append(ft.Text(f"{account}: ${value:.2f}"))

        self.middle_container.update()  # Refresh UI
    
    def refresh_sliders(self):
        """Dynamically updates the sliders when DataManager changes."""
        if not self.slider_container.page:
            return  # Prevent update if not added to the page

        self.slider_container.controls.clear()
        self.slider_container.controls.append(ft.Text("Adjust Account Allocations", size=18, weight="bold"))

        for account, value in self.data_manager.list_accounts().items():
            max_value = value  # Cap is the inputted amount

            if account not in self.sliders or not isinstance(self.sliders[account], tuple):
                slider = ft.Slider(
                    min=0, 
                    max=max_value, 
                    value=round(value),
                    divisions=max_value,  # Ensures snapping to integers
                    label=f"{account}: {round(value)}",
                    on_change=lambda e, a=account: self.debounced_update_slider_value(e, a)  
                )
                text_field = ft.TextField(
                    value=f"{round(value)}", width=80,
                    on_blur=lambda e, a=account: self.update_text_value(e, a)
                )
                delete_button = ft.IconButton(
                    icon=ft.icons.DELETE, 
                    on_click=lambda e, a=account: self.delete_account(a)
                )
                self.sliders[account] = (slider, text_field, delete_button)
            else:
                slider, text_field, delete_button = self.sliders[account]
                slider.value = round(value)
                slider.label = f"{account}: {round(value)}"
                text_field.value = f"{round(value)}"

            # Add the slider, text field, and delete button to the row
            self.slider_container.controls.append(ft.Row([slider, text_field, delete_button]))

        self.slider_container.update()
        self.refresh_left_table()  # ✅ Update daily spending when sliders change
    
    def debounced_update_slider_value(self, e, account):
        """Delays updating to allow smooth sliding."""
        if hasattr(self, "_slider_timer") and self._slider_timer is not None:
            self._slider_timer.cancel()  # Cancel any pending updates
        
        self._slider_timer = threading.Timer(0.2, lambda: self.update_slider_value(e, account))
        self._slider_timer.start()
    
    def delete_account(self, account):
        """Deletes an account from DataManager and refreshes UI."""
        self.data_manager.remove_account(account)  # Assuming delete_account method is in DataManager
        self.refresh_sliders()  # Refresh the sliders
        self.refresh_itemized_list()  # Refresh the itemized list
        self.refresh_left_table()  # Update the left table (if necessary)

    def update_text_value(self, e, account):
        """Update the slider when the text field loses focus."""
        if account in self.sliders:
            slider, text_field = self.sliders[account]
            try:
                value = int(e.control.value)  # Ensure integer value
                value = min(value, slider.max)  # Prevent exceeding max
                value = max(value, slider.min)  # Prevent going below min

                slider.value = value
                slider.label = f"{account}: {value}"
                text_field.value = str(value)

                self.data_manager.update_account(account, value)  # Sync with DataManager
                self.slider_container.update()
                self.refresh_left_table()  # Update daily spending
            except ValueError:
                text_field.value = str(slider.value)  # Reset invalid input
                self.slider_container.update()

    def update_slider_value(self, e, account):
        """Update the text field when the slider is changed."""
        if account in self.sliders:
            slider, text_field = self.sliders[account]
            slider.value = round(e.control.value)  # Ensure whole numbers
            text_field.value = str(round(e.control.value))  # Update text field
            slider.label = f"{account}: {round(e.control.value)}"
            
            self.data_manager.update_account(account, slider.value)  # Sync with DataManager
            self.slider_container.update()
            self.refresh_left_table()  # Update daily spending
        
    def calculate_daily_value(self):
        """Calculates the sum of all slider values to update 'Daily' spending."""
        total_daily = sum(slider.value for slider, _, _ in self.sliders.values())  # Unpack slider only
        return total_daily

    def show_budget_form(self, e):
        """Opens the budget creation form."""
        self.budget_creation_form.open = True
        self.budget_creation_form.update()

    def get_content(self):
        """Returns the main dashboard content."""
        return self.content
