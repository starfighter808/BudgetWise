import flet as ft
from datetime import datetime, timedelta

class AddVendor(ft.AlertDialog):
    def __init__(self, user_data, colors, vend_funcs):
        super().__init__()
        self.bgcolor = colors.GREY_BACKGROUND
        self.user_data = user_data
        self.colors = colors
        self.vend_funcs = vend_funcs
        self.refresh = None
        self.user_id = self.user_data.user_id
        self.db = self.user_data.db
        self.cursor = self.db.cursor()

        # Vendor input fields
        self.vendor_name_field = ft.TextField(
            label="Vendor Name",
            text_style=ft.TextStyle(color=colors.TEXT_COLOR),
            hint_text="Enter Vendor Name",
            hint_style=ft.TextStyle(color=colors.BLUE_BACKGROUND)
        )

        # Dialog content
        self.content = ft.Container(
            width=500,
            bgcolor=self.bgcolor,
            content=ft.Column(
                spacing=10,
                controls=[
                    ft.Text("Create Vendor:", weight=ft.FontWeight.BOLD, color=self.colors.TEXT_COLOR),
                    ft.Row(
                        controls=[
                            ft.Container(self.vendor_name_field, expand=True),
                        ],
                        spacing=10,
                    ),
                    ft.Row(
                        controls=[
                            ft.ElevatedButton("Add Vendor", on_click=self.add_vendor)
                        ],
                        alignment=ft.MainAxisAlignment.START,
                    ),
                    ft.Divider(),
                    ft.Text("Added vendors:", weight=ft.FontWeight.BOLD, color=self.colors.TEXT_COLOR),
                    # Placeholder for future vendor list view
                    ft.Container(
                        content=ft.Text("No vendors yet."),  # Or self.vendors_list_view when implemented
                        height=200,
                        border=ft.border.all(1, self.colors.TEXT_COLOR),
                        padding=10,
                    ),
                ],
            ),
        )

        self.title = ft.Text("Add New Vendor", color=self.colors.TEXT_COLOR)

    def add_vendor(self, e):
        name = self.vendor_name_field.value.strip()
        print(f"AddVendorDialog.add_vendor: name: {name}")

        if name:
            try:
                # Create vendor in the database using vend_funcs
                self.vend_funcs.create_vendor(self.user_id, name)
                
                # Optionally update the vendor list view (refresh if needed)
                if self.refresh:
                    self.refresh()

                # Reset the form and close the dialog
                self.open = False
                self.vendor_name_field.value = ""
                self.update()
            except Exception as err:
                print(f"Error adding vendor: {err}")
        else:
            print("Please enter a name.")  # Replace with Snackbar for UI feedback

    def close_dialog(self, e):
        print("AddVendorDialog.close_dialog called")
        self.open = False
        self.update()
