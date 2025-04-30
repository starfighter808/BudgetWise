import flet as ft
import datetime

class Dashboard(ft.View):
    def __init__(self, page: ft.Page, user_data, NavRail, colors):
        super().__init__(route="/dashboard", bgcolor= colors.GREY_BACKGROUND)
    
        self.page = page
        self.controls.append(ft.Text("Dashbaord"))
        self.colors = colors

        # Database
        self.db = user_data.db
        self.cursor = user_data.db.cursor()

        # page is initialized before userID is stored, so we must set a default condition
        if self.page.session.get("userID") != None:
            print("Dashboard successfully retrieved userID")
            self.userID = self.page.session.get("userID")
        else:
            self.userID = 1
        
        # Get budget data from database
        self.total_budget = self.get_total_budget()
        self.budget_accounts = self.get_accounts()

        # Convert accounts to slider-compatible format
        slider_accounts = [{
            'name': account['account_name'],
            'allocated': account['total_allocated_amount'],
            'current_amount' : account['current_amount'],
            'original_data': account  # Keep reference to original data
        } for account in self.budget_accounts]

        # Initialize pie chart reference
        self.pie_chart = None
        
        # Create the slider panel
        self.slider_panel = BudgetSliderPanel(
            dashboard=self,
            total_budget=self.total_budget,
            accounts=slider_accounts,
            colors=colors
        )

        title_row = ft.Row( # This is the title of the page
        [
            ft.Text("Dashboard", size=30, weight="bold"),
        ],
        alignment=ft.MainAxisAlignment.CENTER, 
        expand=False, 
        )

        # Upcoming transactions table
        self.transaction_table = ft.Column(spacing=10, 
                      alignment=ft.alignment.top_center,
                      controls=[])

        page_content = ft.ResponsiveRow(
        [   # left column
            ft.Column(col=7, controls=[
               # top left container (PieChart)
                ft.Container(
                    expand=5,
                    content=self.build_pie_chart(),
                    margin=10,
                    padding=10,
                    alignment=ft.alignment.center,
                    bgcolor=self.colors.BLACK,
                    width=None,
                    # height=500,
                    border_radius=10,
                ),
                # bottom left container (Transaction Table)
                ft.Container(
                    expand=2,
                    content=self.transaction_table,
                    margin=10,
                    padding=10,
                    alignment=ft.alignment.top_center,
                    bgcolor=self.colors.BLACK,
                    width=None,
                    # height=200,
                    border_radius=10,
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True
            ),  # right column
            ft.Column(col=5, controls=[
               # right container (Slider Panel)
                ft.Container(
                    content= self.slider_panel.build(),
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
                    icon=ft.Icons.SAVE,
                    bgcolor=self.colors.BLACK,
                    color=self.colors.TEXT_COLOR,
                    style=ft.ButtonStyle(padding=20,
                                         icon_size=30,
                                         icon_color=self.colors.TEXT_COLOR,
                                         text_style=ft.TextStyle(
                                             size=25,
                                             )
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
                # ----------------- PAGE CONTENT GOES BELOW -----------------
                page_content,              
                # ----------------- PAGE CONTENT GOES ABOVE -----------------
            ],
            expand=True,  # Make content expand to take the remaining space
        )

        self.controls = [
            ft.Row(
                [
                    NavRail.rail, # navigation bar
                    ft.VerticalDivider(width=1), # divider between navbar and page content
                    content,
                ],
                expand=True,
            )                    
        ]

    def did_mount(self):
        self.draw_transaction_table()
        self.page.update()

    def get_accounts(self):
        self.cursor.execute("SELECT budget_accounts_id, account_name, total_allocated_amount, current_amount FROM budget_accounts WHERE budget_accounts.user_id = ?", (self.userID,))
        accounts = self.cursor.fetchall()
        return [{'budget_accounts_id': account[0], 
                 'account_name': account[1], 
                 'total_allocated_amount': account[2], 
                 'current_amount': account[3]
                } for account in accounts]
    
    def get_transactions(self):
        query = "SELECT v.vendor_name, t.description, t.transaction_date, t.amount FROM transactions t JOIN vendors v ON t.vendor_id = v.vendor_id WHERE t.user_id = ? AND t.transaction_date > CURRENT_TIMESTAMP"
        self.cursor.execute(query, (self.userID,))  # needs the comma to be considered a tuple :'c
        transactions = self.cursor.fetchall()
        print(transactions)
        return [{'vendor_name': transaction[0], 'description': transaction[1], 'transaction_date': transaction[2], 'amount': transaction[3]} for transaction in transactions]

    def get_total_budget(self):
        # Implement this method to get the user's total budget from the database
        self.cursor.execute("SELECT total_budgeted_amount FROM budgets WHERE user_id = ?", (self.userID,))
        result = self.cursor.fetchone()
        return result[0] if result else 5000  # Default value if no budget set
    
    def save_budget(self, e):
        # Save the updated budget allocations to database
        for account in self.slider_panel.accounts:
            original_data = account['original_data']
            self.cursor.execute(
                "UPDATE budget_accounts SET total_allocated_amount = ? WHERE budget_accounts_id = ?",
                (account['allocated'], original_data['budget_accounts_id'])
            )
        self.db.commit_db()

        # Create and show snackbar
        snackbar = ft.SnackBar(
            content=ft.Text("Budget saved successfully!"),
            action="OK",
            action_color=self.colors.GREEN_BUTTON,
            duration=3000
        )
        self.page.snack_bar = snackbar
        snackbar.open = True
        self.page.update()

    def draw_slider_table(self):
        accounts = self.get_accounts()

    def draw_transaction_table(self):
        self.transaction_table.controls.clear()
        self.transaction_table.controls.append(ft.Text("Upcoming Transactions", 
                                        color=self.colors.TEXT_COLOR,
                                        weight="bold",
                                        size=20))
        
        transactions = self.get_transactions()

        # if no upcoming transactions
        if len(transactions) == 0:
            self.transaction_table.controls.append(ft.Text("No upcoming transactions", 
                              italic=True, 
                              color=self.colors.TEXT_COLOR,
                              size=15,))
        else:# otherwise add column titles
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
            # Converting returned string type into timestamp
            timestamp_str = transaction['transaction_date']
            timestamp = datetime.datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
            date = timestamp.date()

            amount = transaction['amount']

            self.transaction_table.controls.append(ft.Row([
                ft.Text(vendor_name, width=150, color=self.colors.TEXT_COLOR, text_align="center", size=16),
                ft.Text(description, width=150, color=self.colors.TEXT_COLOR, text_align="center", size=16),
                ft.Text(date, width=150, color=self.colors.TEXT_COLOR, text_align="center", size=16),
                ft.Text(f"${amount:.2f}", width=150, color=self.colors.TEXT_COLOR, text_align="center", size=16),
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=10))  # Add spacing between columns

    def create_pie_chart(self):
        accounts = self.get_accounts()
        if not accounts:
            return ft.Text("No budget accounts found", color=self.colors.TEXT_COLOR)

        total_allocated = sum(account['total_allocated_amount'] for account in accounts)
        if total_allocated == 0:
            return ft.Text("Budget not allocated", color=self.colors.TEXT_COLOR)

        # Create pie chart with adjusted label positioning
        sections = []
        colors = [
            self.colors.GREEN_BUTTON,
            self.colors.PIE_CHART_YELLOW,
            self.colors.BLUE_BACKGROUND,
            ft.Colors.ORANGE,
            ft.Colors.PURPLE,
            ft.Colors.TEAL
        ]
        
        for i, account in enumerate(accounts):
            percentage = (account['total_allocated_amount'] / total_allocated) * 100
            if percentage < 5:  # Skip labels for very small slices
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
                        shadow=ft.BoxShadow(blur_radius=2, color=ft.Colors.BLACK)
                    ),
                    color=colors[i % len(colors)],
                    radius=100,
                    title_position=1.3,  # This pushes labels outward
                )
            )

        return ft.PieChart(
            sections=sections,
            sections_space=0,
            center_space_radius=40,
            expand=True,
        )

    def update_pie_chart(self):
        if not self.pie_chart:
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

        for i, section in enumerate(self.pie_chart.sections):
            if i < len(accounts):
                account = accounts[i]
                percentage = (account['total_allocated_amount'] / total_allocated) * 100
                section.value = percentage
                section.title = f"{account['account_name']}\n{percentage:.1f}%"
                section.color = colors[i % len(colors)]
            else:
                section.value = 0
                section.title = ""

        self.page.update()

    def build_pie_chart(self):
        return self.create_pie_chart() or ft.Container() # Fallback empty container
    
class BudgetSliderPanel:
    def __init__(self, dashboard, total_budget, accounts, colors):
        self.dashboard = dashboard
        self.total_budget = total_budget
        self.accounts = accounts
        self.colors = colors
        self.sliders = {}
        self.account_labels = {}
        self.remaining_label = ft.Text(
            f"Remaining Budget: ${self.calculate_remaining():.2f}",
            size=16,
            color=self.colors.TEXT_COLOR
        )
        
    def calculate_remaining(self):
        total_allocated = sum(acc['allocated'] for acc in self.accounts)
        return self.total_budget - total_allocated
        
    def create_slider_change_handler(self, account):
        def handler(e):
            change = e.control.value - account['allocated']
            remaining = self.calculate_remaining()
            
            if change > remaining:
                e.control.value = account['allocated'] + remaining
                account['allocated'] = e.control.value
            else:
                account['allocated'] = e.control.value
            
            # Update the corresponding account in the dashboard's budget_accounts
            for acc in self.dashboard.budget_accounts:
                if acc['account_name'] == account['name']:
                    acc['total_allocated_amount'] = account['allocated']
                    break
            
            # Update UI elements
            self.account_labels[account['name']].value = f"{account['name']}: ${account['allocated']:.2f}"
            self.remaining_label.value = f"Remaining Budget: ${self.calculate_remaining():.2f}"
            self.update_slider_limits()
            self.dashboard.update_pie_chart()
            e.page.update()
        return handler
    
    def update_slider_limits(self):
        remaining = self.calculate_remaining()
        for account in self.accounts:
            slider = self.sliders[account['name']]
            slider.max = account['allocated'] + remaining
            if slider.value > slider.max:
                slider.value = slider.max
                account['allocated'] = slider.max
    
    def build(self):
        header = ft.Column([
            ft.Text("Budget Allocation", 
                   size=20, 
                   weight=ft.FontWeight.BOLD,
                   color=self.colors.TEXT_COLOR),
            self.remaining_label,
            ft.Divider(color=self.colors.TEXT_COLOR)
        ])
        
        scroll_content = ft.Column(spacing=5)
        
        for account in self.accounts:
            remaining = self.calculate_remaining()
            slider = ft.Slider(
                min=0,
                max=account['allocated'] + remaining,
                value=account['allocated'],
                divisions=20,
                label="{value}",
                active_color=self.colors.GREEN_BUTTON,
                inactive_color=self.colors.BLUE_BACKGROUND,
                on_change=self.create_slider_change_handler(account)
            )
            self.sliders[account['name']] = slider
            
            account_label = ft.Text(
                f"{account['name']}: ${account['allocated']:.2f}", 
                size=16,
                color=self.colors.TEXT_COLOR
            )
            self.account_labels[account['name']] = account_label
            
            scroll_content.controls.extend([
                account_label,
                slider,
                ft.Divider(height=10, color=ft.Colors.TRANSPARENT)
            ])
        
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
