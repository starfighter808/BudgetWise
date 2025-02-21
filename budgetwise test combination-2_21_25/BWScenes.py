import flet as ft
from BWForms import LoginScene, SignInScene, BudgetCreationForm
from BWMenu import MenuBar
from FormManager import FormManager
from UiUpdater import UIUpdater

class Scene:
    def __init__(self, title, content):
        self.title = title
        self.content = content

    def get_content(self):
        return ft.Container(content=self.content, alignment=ft.alignment.center, expand=True)

class WelcomeScene(Scene):
    def __init__(self, change_scene_callback, show_login_form, show_signin_form):
        self.change_scene_callback = change_scene_callback
        self.show_login_form = show_login_form
        self.show_signin_form = show_signin_form

        welcome_text = ft.Text("Welcome", size=100, color="grey", weight="bold")
        login_button = ft.ElevatedButton(
            text="Login", 
            on_click=lambda _: self.show_login_form()
        )
        signup_button = ft.ElevatedButton(
            text="Sign Up", 
            on_click=lambda _: self.show_signin_form()
        )

        self.centered_column = ft.Column(
            controls=[welcome_text, login_button, signup_button],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        )

        centered_container = ft.Container(
            content=self.centered_column,
            alignment=ft.alignment.center,
            expand=True,
            padding=ft.Padding(0, 0, 0, 0),  # Adjusted padding
            margin=ft.Padding(0, 0, 0, 0)  # Adjusted margin
        )

        super().__init__("Welcome", centered_container)

# class DashboardScene(Scene):
#     def __init__(self, change_scene_callback, p_width, p_height):
#         self.change_scene_callback = change_scene_callback

#         self.window_width = p_width
#         self.window_height = p_height
#         self.menu_width = 200  # Set a fixed width for the menu bar

#         # Create a centered dashboard header
#         dashboard_header = ft.Container(
#             content=ft.Text("Dashboard", size=24, weight="bold"),
#             alignment=ft.alignment.center,  # Center the content
#             padding=20,
#         )

#         # Create a table for the left container
#         table_data = [
#             ["Row 1, Cell 1", "Row 1, Cell 2", "Row 1, Cell 3"],
#             ["Row 2, Cell 1", "Row 2, Cell 2", "Row 2, Cell 3"],
#             ["Row 3, Cell 1", "Row 3, Cell 2", "Row 3, Cell 3"]
#         ]

#         table = ft.DataTable(
#             columns=[
#                 ft.DataColumn(label=ft.Text("Column 1")),
#                 ft.DataColumn(label=ft.Text("Column 2")),
#                 ft.DataColumn(label=ft.Text("Column 3"))
#             ],
#             rows=[
#                 ft.DataRow(cells=[
#                     ft.DataCell(ft.Text(cell)) for cell in row
#                 ]) for row in table_data
#             ],
#             width=400
#         )

#         left_container = ft.Container(
#             content=table,
#             padding=10,
#             width=450,
#             height=self.window_height - 100  # Adjust height as needed
#         )

#         scrollable_content = ft.Column(
#             controls=[
#                 ft.Text(f"Item {i}") for i in range(1, 101)  # Add 100 items for testing
#             ],
#             scroll=ft.ScrollMode.AUTO,
#             expand=True
#         )

#         scrollable_container = ft.Container(
#             content=scrollable_content,
#             padding=10,
#             bgcolor="#2D2D2D",
#             width=450,
#             height=self.window_height - 100  # Adjust height as needed
#         )

#         # Sliders for budgeting preference
#         sliders = [
#             ("Housing or rent", 1000),
#             ("Transportation", 499),
#             ("Food and groceries", 666),
#             ("Utility bills", 333),
#             ("Health", 333),
#             ("Savings", 333),
#             ("Other", 166),
#         ]

#         slider_controls = [
#             ft.Column([ft.Text(f"{label}:"), ft.Slider(value=value, min=0, max=2000)]) for label, value in sliders
#         ]

#         # Daily spending, period amount, and current balance info
#         spending_info = ft.Column([
#             ft.Text("Daily Spending: $27"),
#             ft.Text("Period Amount: $3,333"),
#             ft.Text("Current Balance: $529"),
#         ])

#         # Add Transaction button
#         add_transaction_button = ft.ElevatedButton(text="Add Transaction", on_click=self.add_transaction)

#         # Upcoming payments section
#         upcoming_payments = ft.Column([
#             ft.Text("Upcoming Payments:"),
#             ft.Text("Car Payment - Due: 9/23/23")
#         ])

#         # Combine additional functionality into right container
#         right_container = ft.Column(
#             controls=[
#                 spending_info,
#                 add_transaction_button,
#                 upcoming_payments,
#                 *slider_controls
#             ],
#             alignment=ft.MainAxisAlignment.START,
#             spacing=20
#         )

#         # Center the table and scrollable container, and add right container
#         centered_row = ft.Container(
#             content=ft.Row(
#                 controls=[
#                     left_container,
#                     scrollable_container,
#                     right_container  # Add the right container here
#                 ],
#                 spacing=10,
#                 alignment=ft.MainAxisAlignment.START,  # Align the row to the start to allow space for menu
#                 expand=True
#             ),
#             alignment=ft.alignment.top_left,  # Align the container to the top-left
#             expand=True
#         )

#         # Arrange the dashboard header and centered row with a scrollable container
#         self.scrollable_main_content = ft.Column(
#             controls=[
#                 dashboard_header,
#                 centered_row  # Use centered_row here
#             ],
#             scroll=ft.ScrollMode.AUTO,  # Enable scrolling
#             expand=True
#         )

#         # Create the MenuBar
#         self.menu_bar = MenuBar(change_scene_callback=change_scene_callback)
        
#         # Create the main container that includes the menu bar and scrollable content
#         self.main_container = ft.Row(
#             controls=[
#                 self.menu_bar,
#                 ft.Container(
#                     content=self.scrollable_main_content,
#                     expand=True
#                 )
#             ],
#             spacing=0,
#             expand=True
#         )

#         # Add the main container to the scene
#         super().__init__("Dashboard Scene", self.main_container)

#     # Method to toggle the menu bar and shift main content
#     def toggle_menu(self):
#         self.menu_bar.visible = not self.menu_bar.visible
#         self.main_container.controls[1].width = 0 if not self.menu_bar.visible else self.menu_width
#         self.main_container.update()  # Update the container to reflect changes

#     def add_transaction(self, e):
#         print("Add transaction clicked")

class DashboardScene(ft.Container):
    def __init__(self, change_scene_callback, p_width, p_height, show_budget_creation_form, budget_creation_form):
        super().__init__()
        self.change_scene_callback = change_scene_callback
        self.p_width = p_width
        self.p_height = p_height
        self.show_budget_creation_form = show_budget_creation_form
        self.budget_creation_form = budget_creation_form
        
        self.ui_updater = UIUpdater(self)
        self.form_manager = FormManager(budget_creation_form, self)

        self.slider_controls = []
        self.slider_values = []

        self.daily_spending = 0
        self.period_amount = 0
        self.current_balance = 0

        self.spending_info = self.create_spending_info()
        self.add_transaction_button = ft.ElevatedButton(text="Modify Budget", on_click=self.add_transaction)

        self.scrollable_right_container = self.create_scrollable_right_container()

        self.scrollable_main_content = ft.Column(
            controls=[
                self.create_dashboard_header(),
                self.create_centered_row()
            ],
            expand=True
        )

        self.menu_container = ft.Container(
            content=MenuBar(change_scene_callback=change_scene_callback),
            width=200,
            expand=False
        )
        
        self.main_container = ft.AnimatedSwitcher(
            content=ft.Row(
                controls=[
                    self.menu_container,
                    ft.Container(
                        content=self.scrollable_main_content,
                        expand=True
                    )
                ],
                spacing=0,
                expand=True
            ),
            duration=ft.Duration(milliseconds=300)
        )

        super().__init__("Dashboard Scene", self.main_container)

    def create_dashboard_header(self):
        return ft.Container(
            content=ft.Text("Dashboard", size=24, weight="bold"),
            alignment=ft.alignment.center,
            padding=20,
        )

    def create_table(self):
        table_data = [
            ["Row 1, Cell 1", "Row 1, Cell 2", "Row 1, Cell 3"],
            ["Row 2, Cell 1", "Row 2, Cell 2", "Row 2, Cell 3"],
            ["Row 3, Cell 1", "Row 3, Cell 2", "Row 3, Cell 3"]
        ]

        return ft.DataTable(
            columns=[
                ft.DataColumn(label=ft.Text("Column 1")),
                ft.DataColumn(label=ft.Text("Column 2")),
                ft.DataColumn(label=ft.Text("Column 3"))
            ],
            rows=[
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(cell)) for cell in row
                ]) for row in table_data
            ],
            width=400
        )

    def create_left_container(self):
        return ft.Container(
            content=self.create_table(),
            padding=10,
            width=450,
            height=self.p_height - 100
        )

    def create_scrollable_container(self):
        scrollable_content = ft.Column(
            controls=[
                ft.Text(f"Item {i}") for i in range(1, 101)
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True
        )

        return ft.Container(
            content=scrollable_content,
            padding=10,
            bgcolor="#2D2D2D",
            width=200,
            height=self.p_height - 100
        )

    def create_spending_info(self):
        return ft.Column([
            ft.Text(f"Daily Spending: ${self.daily_spending:.2f}", key="daily_spending"),
            ft.Text(f"Period Amount: ${self.period_amount:.2f}", key="period_amount"),
            ft.Text(f"Current Balance: ${self.current_balance:.2f}", key="current_balance"),
        ])

    def create_scrollable_right_container(self):
        upcoming_payments = ft.Column([
            ft.Text("Upcoming Payments:"),
            ft.Text("Car Payment - Due: 9/23/23")
        ])

        return ft.Column(
            controls=[
                self.spending_info,
                self.add_transaction_button,
                upcoming_payments,
                *self.slider_controls
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=20,
            scroll=ft.ScrollMode.AUTO,
            height=self.p_height - 100
        )

    def create_centered_row(self):
        return ft.Container(
            content=ft.Row(
                controls=[
                    self.create_left_container(),
                    self.create_scrollable_container(),
                    self.scrollable_right_container
                ],
                spacing=10,
                alignment=ft.MainAxisAlignment.START,
                expand=True
            ),
            alignment=ft.alignment.top_left,
            expand=True
        )

    def add_transaction(self, e):
        self.form_manager.show_form(self.budget_creation_form)

    def add_slider(self, account_name, amount):
        max_amount = amount * 2
        print(f"Adding slider for {account_name} with amount {amount:.2f} and max {max_amount:.2f}")

        def on_slider_change(e):
            new_value = e.control.value
            amount_field.value = f"{new_value:.2f}"
            amount_field.update()
            self.ui_updater.update_daily_spending()

        slider = ft.Slider(value=amount, min=0, max=max_amount, on_change=on_slider_change)

        amount_field = ft.TextField(value=f"{amount:.2f}", on_submit=lambda e: self.on_amount_change(e, slider, max_amount))

        delete_button = ft.IconButton(
            icon=ft.icons.DELETE,
            icon_color=ft.colors.RED,
            on_click=lambda e: self.delete_slider(account_name, amount, slider)
        )

        self.slider_controls.append(
            ft.Column([
                ft.Text(f"{account_name}:"),
                ft.Row([slider, amount_field, delete_button])
            ])
        )
        self.slider_values.append(slider.value)
        self.ui_updater.update_amounts(amount)
        self.ui_updater.refresh_sliders()
        self.ui_updater.update_daily_spending()  # Ensure initial update

    def on_amount_change(self, e, slider, max_amount):
        try:
            new_value = float(e.control.value)
            if 0 <= new_value <= max_amount:
                slider.value = new_value
                slider.update()
                self.ui_updater.update_daily_spending()
            else:
                print(f"Error: Amount {new_value} is out of bounds. Should be between 0 and {max_amount:.2f}")
        except ValueError:
            print("Error: Invalid input. Please enter a valid number.")

    def delete_slider(self, account_name, amount, slider):
        print(f"Deleting slider for {account_name} with amount {amount:.2f}")

        # Find and remove the control containing the slider
        initial_count = len(self.slider_controls)
        self.slider_controls = [control for control in self.slider_controls if control.controls[1].controls[0] != slider]
        final_count = len(self.slider_controls)

        print(f"Initial slider count: {initial_count}, Final slider count: {final_count}")

        # Verify if the slider was removed
        if initial_count == final_count:
            print(f"Warning: Slider for {account_name} was not removed from the list")

        # Update the UI to remove the slider
        self.ui_updater.update_amounts(-amount)
        self.ui_updater.refresh_sliders()

        # Manually update the scrollable_right_container to reflect the deletion
        self.scrollable_right_container.controls = [
            self.spending_info,
            self.add_transaction_button,
            ft.Text("Upcoming Payments:"),
            ft.Text("Car Payment - Due: 9/23/23"),
            *self.slider_controls
        ]
        self.scrollable_right_container.update()
        self.scrollable_main_content.update()

        # Update daily spending without the deleted slider
        self.ui_updater.update_daily_spending()

        # Remove the account from the form manager
        self.form_manager.remove_account(account_name)

        print(f"Slider for {account_name} deleted successfully.")

    def get_content(self):
        return self.scrollable_main_content