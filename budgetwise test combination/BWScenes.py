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

class DashboardScene(Scene):
    def __init__(self, change_scene_callback, p_width, p_height):
        self.change_scene_callback = change_scene_callback

        self.window_width = p_width
        self.window_height = p_height

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
            width=450,
            height=self.window_height - 100  # Adjust height as needed
        )

        # Center the table and scrollable container
        centered_row = ft.Container(
            content=ft.Row(
                controls=[
                    left_container,
                    scrollable_container
                ],
                spacing=10,
                alignment=ft.MainAxisAlignment.CENTER,  # Center align the row
                expand=True
            ),
            alignment=ft.alignment.center,  # Center the container
            expand=True
        )

        # Arrange the dashboard header and centered row
        self.content = ft.Column(
            controls=[
                dashboard_header,
                centered_row  # Use centered_row here
            ],
            expand=True
        )

        # Create the MenuBar
        self.menu_bar = MenuBar(change_scene_callback=change_scene_callback)
        
        # Create the main container that includes the menu bar and content
        self.main_container = ft.Row(
            controls=[
                self.menu_bar,  # Menu bar will be shown/hidden
                ft.Container(content=self.content, expand=True)  # Main content
            ],
            spacing=0
        )

        # Add the main container to the scene
        super().__init__("Dashboard Scene", self.main_container)

    # Method to toggle the menu bar and shift main content
    def toggle_menu(self):
        self.menu_bar.visible = not self.menu_bar.visible
        self.main_container.update()  # Update the container to reflect changes

