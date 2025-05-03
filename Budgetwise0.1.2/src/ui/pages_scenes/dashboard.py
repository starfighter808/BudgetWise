import flet as ft
import datetime

class Dashboard(ft.View):
    def __init__(self, page: ft.Page, user_data, NavRail, colors):
        super().__init__(route="/dashboard", bgcolor=colors.GREY_BACKGROUND)
    
        self.page = page
        self.user_data = user_data
        self.controls.append(ft.Text("Dashboard"))
        self.colors = colors

        # Database
        self.db = user_data.db
        self.cursor = user_data.db.cursor()

        if self.page.session.get("userID") != None:
            print("Dashboard successfully retrieved userID")
            self.userID = self.page.session.get("userID")
        else:
            self.userID = 1
        
        # Get budget data
        self.budget_name_label = ft.Row(
            controls=[
                ft.Text("Budget:", size=18, weight="bold", color=self.colors.TEXT_COLOR),
                ft.Text("", size=18, weight="w500", color=self.colors.TEXT_COLOR),
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )

        self.total_budget = self.get_total_budget()
        self.budget_accounts = self.get_accounts()

        # Convert accounts to input format
        input_accounts = [{
            'name': account['account_name'],
            'allocated': account['total_allocated_amount'],
            'current_amount': account['current_amount'],
            'original_data': account
        } for account in self.budget_accounts]

        self.pie_chart = None
        
        self.input_panel = BudgetInputPanel(
            dashboard=self,
            total_budget=self.total_budget,
            accounts=input_accounts,
            colors=colors
        )

        title_row = ft.Row(
            [ft.Text("Dashboard", size=30, weight="bold")],
            alignment=ft.MainAxisAlignment.CENTER, 
            expand=False
        )

        self.transaction_table = ft.Column(
            spacing=10, 
            alignment=ft.alignment.top_center,
            controls=[]
        )

        page_content = ft.ResponsiveRow(
            [   
                ft.Column(col=7, controls=[
                    ft.Container(
                        expand=5,
                        content=ft.Column([
                            self.budget_name_label,
                            self.build_pie_chart(),
                        ]),
                        margin=10,
                        padding=10,
                        alignment=ft.alignment.center,
                        bgcolor=self.colors.BLACK,
                        width=None,
                        border_radius=10,
                    ),
                    ft.Container(
                        expand=2,
                        content=self.transaction_table,
                        margin=10,
                        padding=10,
                        alignment=ft.alignment.top_center,
                        bgcolor=self.colors.BLACK,
                        width=None,
                        border_radius=10,
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                expand=True
                ),
                ft.Column(col=5, controls=[
                    ft.Container(
                        content=self.input_panel.build(),
                        margin=10,
                        padding=10,
                        alignment=ft.alignment.top_center,
                        bgcolor=self.colors.BLACK,
                        width=None,
                        height=None,
                        border_radius=10,
                        expand=True
                    ),
                    ft.ElevatedButton(
                        "Save",
                        on_click=self.save_budget,
                        tooltip="Save current budget account settings",
                        icon=ft.icons.SAVE,
                        bgcolor=self.colors.BLACK,
                        color=self.colors.TEXT_COLOR,
                        style=ft.ButtonStyle(
                            padding=20,
                            icon_size=30,
                            icon_color=self.colors.TEXT_COLOR,
                            text_style=ft.TextStyle(size=25)
                        )
                    )
                ],
                alignment=ft.CrossAxisAlignment.CENTER,
                expand=True
                ),
            ],
            expand=True
        )
                
        content = ft.Column(
            [
                title_row,
                page_content,              
            ],
            expand=True,
        )

        self.controls = [
            ft.Row(
                [
                    NavRail.rail,
                    ft.VerticalDivider(width=1),
                    content,
                ],
                expand=True,
            )                    
        ]

    def did_mount(self):
        self.budget_name_label.controls[1].value = self.user_data.budget_name
        self.draw_transaction_table()
        self.page.update()

    def get_accounts(self):
        self.cursor.execute("SELECT budget_accounts_id, account_name, total_allocated_amount, current_amount FROM budget_accounts WHERE user_id = ?", (self.userID,))
        accounts = self.cursor.fetchall()
        return [{
            'budget_accounts_id': account[0], 
            'account_name': account[1], 
            'total_allocated_amount': account[2], 
            'current_amount': account[3]
        } for account in accounts]
    
    def get_transactions(self):
        query = """SELECT v.vendor_name, t.description, t.transaction_date, t.amount 
                   FROM transactions t 
                   JOIN vendors v ON t.vendor_id = v.vendor_id 
                   WHERE t.user_id = ? AND t.transaction_date > CURRENT_TIMESTAMP"""
        self.cursor.execute(query, (self.userID,))
        transactions = self.cursor.fetchall()
        return [{
            'vendor_name': transaction[0], 
            'description': transaction[1], 
            'transaction_date': transaction[2], 
            'amount': transaction[3]
        } for transaction in transactions]

    def get_total_budget(self):
        self.cursor.execute("SELECT total_budgeted_amount FROM budgets WHERE user_id = ?", (self.userID,))
        result = self.cursor.fetchone()
        return result[0] if result else 5000
    
    def save_budget(self, e):
        for account in self.input_panel.accounts:
            original_data = account['original_data']
            self.cursor.execute(
                "UPDATE budget_accounts SET total_allocated_amount = ? WHERE budget_accounts_id = ?",
                (account['allocated'], original_data['budget_accounts_id'])
            )
        self.db.commit_db()

        snackbar = ft.SnackBar(
            content=ft.Text("Budget saved successfully!"),
            action="OK",
            action_color=self.colors.GREEN_BUTTON,
            duration=3000
        )
        self.page.snack_bar = snackbar
        snackbar.open = True
        self.update_pie_chart()
        self.page.update()

    def draw_transaction_table(self):
        self.transaction_table.controls.clear()
        self.transaction_table.controls.append(
            ft.Text("Upcoming Transactions", 
                   color=self.colors.TEXT_COLOR,
                   weight="bold",
                   size=20))
        
        transactions = self.get_transactions()

        if len(transactions) == 0:
            self.transaction_table.controls.append(
                ft.Text("No upcoming transactions", 
                       italic=True, 
                       color=self.colors.TEXT_COLOR,
                       size=15))
        else:
            self.transaction_table.controls.append(
                ft.Row([
                    ft.Text("Vendors", weight="bold", width=150, color=self.colors.TEXT_COLOR, text_align="center", size=15),
                    ft.Text("Transaction", weight="bold", width=150, color=self.colors.TEXT_COLOR, text_align="center", size=15),
                    ft.Text("Date", weight="bold", width=150, color=self.colors.TEXT_COLOR, text_align="center", size=15),
                    ft.Text("Amount", weight="bold", width=150, color=self.colors.TEXT_COLOR, text_align="center", size=15),
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=10))
            
            for transaction in transactions:
                vendor_name = transaction['vendor_name']
                description = transaction['description']
                timestamp_str = transaction['transaction_date']
                timestamp = datetime.datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
                date = timestamp.date()
                amount = transaction['amount']

                self.transaction_table.controls.append(ft.Row([
                    ft.Text(vendor_name, width=150, color=self.colors.TEXT_COLOR, text_align="center", size=16),
                    ft.Text(description, width=150, color=self.colors.TEXT_COLOR, text_align="center", size=16),
                    ft.Text(date, width=150, color=self.colors.TEXT_COLOR, text_align="center", size=16),
                    ft.Text(f"${amount:.2f}", width=150, color=self.colors.TEXT_COLOR, text_align="center", size=16),
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=10))

    def create_pie_chart(self):
        self.pie_chart = self._create_pie_chart()
        return self.pie_chart

    def _create_pie_chart(self):
        accounts = self.get_accounts()
        if not accounts:
            return ft.Text("No budget accounts found", color=self.colors.TEXT_COLOR)

        total_allocated = sum(account['total_allocated_amount'] for account in accounts)
        if total_allocated == 0:
            return ft.Text("Budget not allocated", color=self.colors.TEXT_COLOR)

        sections = []
        colors = [
            self.colors.GREEN_BUTTON,
            self.colors.PIE_CHART_YELLOW,
            self.colors.BLUE_BACKGROUND,
            ft.colors.ORANGE,
            ft.colors.PURPLE,
            ft.colors.TEAL
        ]
        
        for i, account in enumerate(accounts):
            percentage = (account['total_allocated_amount'] / total_allocated) * 100
            if percentage < 5:
                show_title = ""
            else:
                show_title = f"{account['account_name']}\n{percentage:.1f}%"
                
            sections.append(
                ft.PieChartSection(
                    percentage,
                    title=show_title,
                    title_style=ft.TextStyle(
                        size=12,
                        color=self.colors.TEXT_COLOR,
                        weight=ft.FontWeight.BOLD,
                        shadow=ft.BoxShadow(blur_radius=2, color=ft.colors.BLACK)
                    ),
                    color=colors[i % len(colors)],
                    radius=100,
                    title_position=1.3,
                )
            )

        return ft.PieChart(
            sections=sections,
            sections_space=0,
            center_space_radius=40,
            expand=True,
        )

    def update_pie_chart(self):
        if not hasattr(self, 'pie_chart') or not self.pie_chart:
            return

        accounts = self.get_accounts()
        total_allocated = sum(account['total_allocated_amount'] for account in accounts)
        if total_allocated == 0:
            return

        colors = [
            self.colors.GREEN_BUTTON,
            self.colors.PIE_CHART_YELLOW,
            self.colors.BLUE_BACKGROUND,
            ft.colors.ORANGE,
            ft.colors.PURPLE,
            ft.colors.TEAL
        ]

        self.pie_chart.sections.clear()

        for i, account in enumerate(accounts):
            percentage = (account['total_allocated_amount'] / total_allocated) * 100
            if percentage < 5:
                show_title = ""
            else:
                show_title = f"{account['account_name']}\n{percentage:.1f}%"

            self.pie_chart.sections.append(
                ft.PieChartSection(
                    percentage,
                    title=show_title,
                    title_style=ft.TextStyle(
                        size=12,
                        color=self.colors.TEXT_COLOR,
                        weight=ft.FontWeight.BOLD,
                        shadow=ft.BoxShadow(blur_radius=2, color=ft.colors.BLACK)
                    ),
                    color=colors[i % len(colors)],
                    radius=100,
                    title_position=1.3,
                )
            )

        self.pie_chart.update()

    def build_pie_chart(self):
        return self.create_pie_chart()
    
class BudgetInputPanel:
    def __init__(self, dashboard, total_budget, accounts, colors):
        self.dashboard = dashboard
        self.total_budget = total_budget
        self.accounts = accounts
        self.colors = colors
        self.input_fields = {}
        self.account_rows = {}
        self.remaining_label = ft.Text(
            f"Remaining Budget: ${self.calculate_remaining():.2f}",
            size=16,
            color=self.colors.TEXT_COLOR
        )
        
    def calculate_remaining(self):
        total_allocated = sum(acc['allocated'] for acc in self.accounts)
        return max(0, self.total_budget - total_allocated)
        
    def create_input_change_handler(self, account):
        def handler(e):
            try:
                new_value = float(e.control.value) if e.control.value else 0.0
                
                proposed_total = sum(
                    acc['allocated'] if acc['name'] != account['name'] else new_value 
                    for acc in self.accounts
                )
                
                if proposed_total > self.total_budget:
                    snackbar = ft.SnackBar(
                        content=ft.Text(
                            f"Error: Total budget would exceed ${self.total_budget:,.2f}",
                            color=self.colors.TEXT_COLOR
                        ),
                        bgcolor=self.colors.RED_ERROR,
                        duration=2000
                    )
                    self.dashboard.page.snack_bar = snackbar
                    snackbar.open = True
                    e.control.value = str(account['allocated'])
                    self.dashboard.page.update()
                    return
                
                account['allocated'] = new_value
                
                for acc in self.dashboard.budget_accounts:
                    if acc['account_name'] == account['name']:
                        acc['total_allocated_amount'] = account['allocated']
                        break
                
                self.remaining_label.value = f"Remaining Budget: ${self.calculate_remaining():.2f}"
                self.dashboard.update_pie_chart()
                self.dashboard.page.update()
                
            except ValueError:
                e.control.value = str(account['allocated'])
                self.dashboard.page.update()
        return handler
    
    def build(self):
        header = ft.Column([
            ft.Text("Budget Allocation", 
                   size=20, 
                   weight=ft.FontWeight.BOLD,
                   color=self.colors.TEXT_COLOR),
            ft.Row([
                ft.Text("Total Budget:", size=16, color=self.colors.TEXT_COLOR),
                ft.Text(f"${self.total_budget:,.2f}", size=16, color=self.colors.TEXT_COLOR),
            ]),
            self.remaining_label,
            ft.Divider(color=self.colors.TEXT_COLOR)
        ])
        
        scroll_content = ft.Column(spacing=10)
        
        for account in self.accounts:
            row = ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            )
            
            account_name = ft.Text(
                account['name'],
                size=16,
                color=self.colors.TEXT_COLOR,
                width=150
            )
            
            input_field = ft.TextField(
                value=str(account['allocated']),
                width=150,
                text_size=16,
                text_align=ft.TextAlign.RIGHT,
                color=self.colors.TEXT_COLOR,
                border_color=self.colors.TEXT_COLOR,
                on_change=self.create_input_change_handler(account),
                input_filter=ft.NumbersOnlyInputFilter(),
                prefix_text="$",
                border_radius=5,
                border_width=1,
                content_padding=5
            )
            
            self.input_fields[account['name']] = input_field
            self.account_rows[account['name']] = row
            
            row.controls.extend([
                account_name,
                input_field
            ])
            
            scroll_content.controls.append(row)
            scroll_content.controls.append(ft.Divider(height=10, color=ft.colors.TRANSPARENT))
        
        scrollable_container = ft.Container(
            content=ft.ListView(
                controls=[scroll_content],
                expand=True,
                spacing=10,
                padding=10
            ),
            height=400,
            expand=True
        )
        
        return ft.Column([
            header,
            scrollable_container
        ], expand=True)
