import flet as ft
import datetime

class Dashboard(ft.View):
    def __init__(self, page: ft.Page, user_repo, NavRail):
        super().__init__(route="/dashboard", bgcolor="#5C9DFF")
    
        self.page = page
        self.controls.append(ft.Text("Dashbaord"))

        # Database
        self.db = user_repo.db
        self.cursor = user_repo.db.cursor()

        # page is initialized before userID is stored, so we must set a default condition
        if self.page.session.get("userID") != None:
            print("Dashboard successfully retrieved userID")
            self.userID = self.page.session.get("userID")
        else:
            self.userID = 1
        

        title_row = ft.Row( # This is the title of the page
        [
            ft.Text("Dashboard", size=30, weight="bold"),
        ],
        alignment=ft.MainAxisAlignment.CENTER, 
        expand=False, 
        )

        # SliderPanel
        self.budget_accounts_content = ft.Column(controls=[ft.Text("Budget Accounts", 
                                      size=20, 
                                      weight="bold",
                                      color=ft.Colors.WHITE,
                                      style=ft.TextStyle(ft.alignment.top_center)),
                              ft.Text("Bills"),
                              ft.Slider(value=0.3),
                              ft.Text("Groceries", size=16),
                              ft.Slider(value=0.3),
                              ft.Text("Investments", size=16),
                              ft.Slider(value=0.3),
                              ft.Text("Savings", size=16),
                              ft.Slider(value=0.3),
                              ])
        # self.budget_accounts_table = ft.Column(spacing=10, alignment=ft.MainAxisAlignment.CENTER)

        # # Wrap the table in a ListView for scrolling
        # self.scrollable_table = ft.ListView(
        #     controls=[self.budget_accounts_table],
        #     expand=True,
        #     spacing=10,
        #     padding=10,
        # )

        # self.slider_panel = ft.Column(alignment=ft.alignment.top_center,
        #                               controls=[ft.Text("Budget Accounts", 
        #                                                 size=20, 
        #                                                 color=ft.Colors.WHITE,
        #                                                 style=ft.TextStyle(ft.alignment.top_center)), 
        #                                         self.scrollable_table],)

        # PieChart

        # UpcomingTransactions
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
                    content=self.pie_chart(),
                    margin=10,
                    padding=10,
                    alignment=ft.alignment.center,
                    bgcolor=ft.Colors.BLACK,
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
                    bgcolor=ft.Colors.BLACK,
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
                    content= self.budget_accounts_content,
                    # ft.Text("Budget Accounts", size=20, color=ft.Colors.WHITE), 
                            #  self.scrollable_table],
                    margin=10,
                    padding=10,
                    alignment=ft.alignment.top_center,
                    bgcolor=ft.Colors.BLACK,
                    width=None,
                    height=None,
                    border_radius=10,
                    expand=True
                ),
                ft.ElevatedButton(
                    "Save",
                    tooltip="Save current budget account settings",
                    icon=ft.Icons.SAVE,
                    bgcolor=ft.Colors.BLACK,
                    color=ft.Colors.WHITE,
                    style=ft.ButtonStyle(padding=20,
                                         icon_size=30,
                                         icon_color=ft.Colors.WHITE,
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
        self.cursor.execute("SELECT budget_accounts_id, account_name, balance FROM budget_accounts WHERE budget_accounts.the_user = ?", self.userID)
        accounts = self.cursor.fetchall()
        return [{'budget_accounts_id': account[0], 'account_name': account[1], 'balance': account[2]} for account in accounts]
    
    def get_transactions(self):
        query = "SELECT v.vendor_name, t.description, t.transaction_date, t.amount FROM transactions t JOIN vendor v ON t.vendor_id = v.vendor_id WHERE t.the_user = ? AND t.transaction_date > CURRENT_TIMESTAMP"
        self.cursor.execute(query, (self.userID,))  # needs the comma to be considered a tuple :'c
        transactions = self.cursor.fetchall()
        print(transactions)
        return [{'vendor_name': transaction[0], 'description': transaction[1], 'transaction_date': transaction[2], 'amount': transaction[3]} for transaction in transactions]

    # TODO: Implement this in a way where a user can have multiple budgets
    def get_budget(self):
        self.cursor.execute("SELECT budget_accounts_id, account_name, balance FROM budget_accounts WHERE budget_accounts.the_user = ?", self.userID)
        accounts = self.cursor.fetchall()
        return [{'budget_accounts_id': account[0], 'account_name': account[1], 'balance': account[2]} for account in accounts]

    def draw_slider_table(self):
        accounts = self.get_accounts()

    def draw_transaction_table(self):
        self.transaction_table.controls.clear()
        self.transaction_table.controls.append(ft.Text("Upcoming Transactions", 
                                        color=ft.Colors.WHITE,
                                        weight="bold",
                                        size=20))
        
        transactions = self.get_transactions()

        # if no upcoming transactions
        if len(transactions) == 0:
            self.transaction_table.controls.append(ft.Text("No upcoming transactions", 
                              italic=True, 
                              color=ft.Colors.WHITE,
                              size=15,))
        else:# otherwise add column titles
            self.transaction_table.controls.append(
                ft.Row([
                    ft.Text("Vendor", weight="bold", width=150, color=ft.Colors.WHITE, text_align="center", size=15),
                    ft.Text("Transaction", weight="bold", width=150, color=ft.Colors.WHITE, text_align="center", size=15),
                    ft.Text("Date", weight="bold", width=150, color=ft.Colors.WHITE, text_align="center", size=15),
                    ft.Text("Amount", weight="bold", width=150, color=ft.Colors.WHITE, text_align="center", size=15),
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
                ft.Text(vendor_name, width=150, color=ft.Colors.WHITE, text_align="center", size=16),
                ft.Text(description, width=150, color=ft.Colors.WHITE, text_align="center", size=16),
                ft.Text(date, width=150, color=ft.Colors.WHITE, text_align="center", size=16),
                ft.Text(f"${amount:.2f}", width=150, color=ft.Colors.WHITE, text_align="center", size=16),
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=10))  # Add spacing between columns

    # TODO: Needs work badly. Literally ripped from flet documentation
    def pie_chart(self):
        normal_radius = 100
        hover_radius = 120
        normal_title_style = ft.TextStyle(
            size=16, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD
        )
        hover_title_style = ft.TextStyle(
            size=22,
            color=ft.Colors.WHITE,
            weight=ft.FontWeight.BOLD,
            shadow=ft.BoxShadow(blur_radius=2, color=ft.Colors.BLACK54),
        )

        def on_chart_event(e: ft.PieChartEvent):
            for idx, section in enumerate(chart.sections):
                if idx == e.section_index:
                    section.radius = hover_radius
                    section.title_style = hover_title_style
                else:
                    section.radius = normal_radius
                    section.title_style = normal_title_style
            chart.update()

        chart = ft.PieChart(
            sections=[
                ft.PieChartSection(
                    40,
                    title="40%",
                    title_style=normal_title_style,
                    color=ft.Colors.BLUE,
                    radius=normal_radius,
                ),
                ft.PieChartSection(
                    30,
                    title="30%",
                    title_style=normal_title_style,
                    color=ft.Colors.YELLOW,
                    radius=normal_radius,
                ),
                ft.PieChartSection(
                    15,
                    title="15%",
                    title_style=normal_title_style,
                    color=ft.Colors.PURPLE,
                    radius=normal_radius,
                ),
                ft.PieChartSection(
                    15,
                    title="15%",
                    title_style=normal_title_style,
                    color=ft.Colors.GREEN,
                    radius=normal_radius,
                ),
            ],
            sections_space=0,
            center_space_radius=80,
            on_chart_event=on_chart_event,
            expand=True,
        )

        return chart