import flet as ft

class TransactionScene(ft.Container):
    def __init__(self, change_scene_callback, p_width, p_height, data_manager):
        super().__init__()
        self.change_scene_callback = change_scene_callback
        self.p_width = p_width
        self.p_height = p_height
        self.data_manager = data_manager
        self.bgcolor = "#0d0d10"
        self.data = [
            {"account_name": "Housing or Rent", "transaction_date": "9/1/23", "recurring_date": "10/1/23", "amount": "$1000"},
            {"account_name": "Transportation", "transaction_date": "9/2/23", "recurring_date": "10/2/23", "amount": "$300"},
            {"account_name": "Food and groceries", "transaction_date": "9/3/23", "recurring_date": "N/A", "amount": "$200"},
            {"account_name": "Utility bills", "transaction_date": "9/4/23", "recurring_date": "10/1/23", "amount": "$100"},
            {"account_name": "Health", "transaction_date": "9/5/23", "recurring_date": "10/5/23", "amount": "$200"},
            {"account_name": "Savings", "transaction_date": "9/6/23", "recurring_date": "10/6/23", "amount": "$333"},
            {"account_name": "Other", "transaction_date": "9/7/23", "recurring_date": "10/7/23", "amount": "$10"},
            {"account_name": "Subcategory 1", "transaction_date": "9/8/23", "recurring_date": "N/A", "amount": "$5"},
            {"account_name": "Subcategory 2", "transaction_date": "9/9/23", "recurring_date": "N/A", "amount": "$10"}
        ]

        # Create the table and add it to the container's content
        self.content = ft.Column(
            controls=[
                self.create_table(),
                ft.Container(
                    content=ft.ElevatedButton(
                        text="Transaction Menu",
                        on_click=self.on_submit_click
                    ),
                    alignment=ft.alignment.center_right,
                    padding=ft.Padding(10, 10, 10, 10)  # Provide all four values for padding
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            expand=True
        )

    def create_table(self):
        # Create the table columns
        columns = [
            ft.DataColumn(ft.Text("Account Name")),
            ft.DataColumn(ft.Text("Transaction Date")),
            ft.DataColumn(ft.Text("Recurring Date")),
            ft.DataColumn(ft.Text("Amount")),
        ]

        # Create the table rows
        rows = [ft.DataRow(cells=[
            ft.DataCell(ft.Text(row["account_name"])),
            ft.DataCell(ft.Text(row["transaction_date"])),
            ft.DataCell(ft.Text(row["recurring_date"])),
            ft.DataCell(ft.Text(row["amount"])),
        ]) for row in self.data]

        # Create and return the table
        return ft.DataTable(columns=columns, rows=rows)

    def on_submit_click(self, event):
        # Handle the submit button click event
        print("Submit button clicked!")
        # You can add your custom logic here

    def get_content(self):
        """Returns the main dashboard content."""
        return self.content
        