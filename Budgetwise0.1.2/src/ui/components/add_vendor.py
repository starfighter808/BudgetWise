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
        self.db = self.user_data.db
        self.cursor = self.db.cursor()
        self.vendor_name_list = []
        # Vendor input fields
        self.vendor_name_field = ft.TextField(
            label="Vendor Name",
            label_style=ft.TextStyle(color=self.colors.BORDERBOX_COLOR), 
            text_style=ft.TextStyle(color=colors.TEXT_COLOR),
            hint_text="Enter Vendor Name",
            hint_style=ft.TextStyle(color=colors.BLUE_BACKGROUND),
            focused_border_color= self.colors.BORDERBOX_COLOR
        )

        # added code here ----------------
        # Container to hold the list of added vendors
        self.vendors_column = ft.Column(spacing=5)
        self.vendors_container = ft.Container(
            content=self.vendors_column,
            height=200,
            border=ft.border.all(1, self.colors.TEXT_COLOR),
            padding=10,
            expand=True, # Added expand for better layout
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
                    self.vendors_container, #new code
                ],
            ),
        )

        self.title = ft.Text("Add New Vendor", color=self.colors.TEXT_COLOR)

    def add_vendor(self, e):
        name = self.vendor_name_field.value.strip()
        print(f"AddVendorDialog.add_vendor: name: {name}")

        if name:
            try:
                self.user_id = self.user_data.user_id #get user-ID at vendor creation time
                #debug print
                #print(f"adding to DB userID: {self.user_id}  vendor name: {name}" )
                
                # Create vendor in the database using vend_funcs
                self.vend_funcs.create_vendor(self.user_id, name)

                # update displayed vendor list (new code)
                self.fill_vendor_names()
                
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

    def fill_vendor_names(self):
        self.user_id = self.user_data.user_id #get user-ID at vendor filling time
        self.vendor_name_list = self.vend_funcs.get_all_vendors(self.user_data.user_id)
        self.vendors_column.controls = [
            ft.Text(
                vendor, 
                color=self.colors.TEXT_COLOR
                ) for vendor in self.vendor_name_list
                ]
        self.vendors_column.update()