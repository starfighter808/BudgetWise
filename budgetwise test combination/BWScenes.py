import flet as ft
from BWForms import LoginScene, SignInScene
from BWMenu import MenuBar

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

class DashboardScene(Scene):
    def __init__(self, change_scene_callback, p_width, p_height):
        self.change_scene_callback = change_scene_callback

        self.window_width = p_width
        self.window_height = p_height
        self.menu_width = 200  # Set a fixed width for the menu bar

        # Create a centered dashboard header
        dashboard_header = ft.Container(
            content=ft.Text("Dashboard", size=24, weight="bold"),
            alignment=ft.alignment.center,  # Center the content
            padding=20,
        )

        # Create a table for the left container
        table_data = [
            ["Row 1, Cell 1", "Row 1, Cell 2", "Row 1, Cell 3"],
            ["Row 2, Cell 1", "Row 2, Cell 2", "Row 2, Cell 3"],
            ["Row 3, Cell 1", "Row 3, Cell 2", "Row 3, Cell 3"]
        ]

        table = ft.DataTable(
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

        left_container = ft.Container(
            content=table,
            padding=10,
            width=450,
            height=self.window_height - 100  # Adjust height as needed
        )

        scrollable_content = ft.Column(
            controls=[
                ft.Text(f"Item {i}") for i in range(1, 101)  # Add 100 items for testing
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True
        )

        scrollable_container = ft.Container(
            content=scrollable_content,
            padding=10,
            bgcolor="#2D2D2D",
            width=200,
            height=self.window_height - 100  # Adjust height as needed
        )

        # Sliders for budgeting preference
        sliders = [
            ("Housing or rent", 1000),
            ("Transportation", 499),
            ("Food and groceries", 666),
            ("Utility bills", 333),
            ("Health", 333),
            ("Savings", 333),
            ("Other", 166),
        ]

        slider_controls = [
            ft.Column([ft.Text(f"{label}:"), ft.Slider(value=value, min=0, max=2000)]) for label, value in sliders
        ]

        # Daily spending, period amount, and current balance info
        spending_info = ft.Column([
            ft.Text("Daily Spending: $27"),
            ft.Text("Period Amount: $3,333"),
            ft.Text("Current Balance: $529"),
        ])

        # Add Transaction button
        add_transaction_button = ft.ElevatedButton(text="Add Transaction", on_click=self.add_transaction)

        # Upcoming payments section
        upcoming_payments = ft.Column([
            ft.Text("Upcoming Payments:"),
            ft.Text("Car Payment - Due: 9/23/23")
        ])

        # Combine additional functionality into right container
        right_container = ft.Column(
            controls=[
                spending_info,
                add_transaction_button,
                upcoming_payments,
                *slider_controls
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=20
        )

        # Center the table and scrollable container, and add right container
        centered_row = ft.Container(
            content=ft.Row(
                controls=[
                    left_container,
                    scrollable_container,
                    right_container  # Add the right container here
                ],
                spacing=10,
                alignment=ft.MainAxisAlignment.START,  # Align the row to the start to allow space for menu
                expand=True
            ),
            alignment=ft.alignment.top_left,  # Align the container to the top-left
            expand=True
        )

        # Arrange the dashboard header and centered row with a scrollable container
        self.scrollable_main_content = ft.Column(
            controls=[
                dashboard_header,
                centered_row  # Use centered_row here
            ],
            scroll=ft.ScrollMode.AUTO,  # Enable scrolling
            expand=True
        )

        # Create the MenuBar
        self.menu_bar = MenuBar(change_scene_callback=change_scene_callback)
        self.menu_bar.visible = False  # Start with the menu hidden
        
        # Create the main container that includes the menu bar and scrollable content
        self.menu_container = ft.Container(
            content=self.menu_bar,
            width=0,  # Start with the menu width set to 0
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
            duration=ft.Duration(milliseconds=300)  # Set the animation duration
        )

        # Add the main container to the scene
        super().__init__("Dashboard Scene", self.main_container)

    def add_transaction(self, e):
        print("Add transaction clicked")