import flet as ft

class NavRail(ft.Container):
    def __init__(self, page: ft.Page):
        self.page = page
        self.rail = ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            # extended=True,
            min_width=100,
            min_extended_width=400,
            # leading=ft.FloatingActionButton(icon=ft.Icons.CREATE, text="Add"),
            group_alignment=-0.9,
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.Icons.DASHBOARD_OUTLINED, 
                    selected_icon=ft.Icons.DASHBOARD, 
                    label="Dashboard",
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icon(ft.Icons.ACCOUNT_BALANCE_WALLET_OUTLINED),
                    selected_icon=ft.Icon(ft.Icons.ACCOUNT_BALANCE_WALLET),
                    label="Accounts",
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.ACCOUNT_BALANCE_OUTLINED,
                    selected_icon=ft.Icon(ft.Icons.ACCOUNT_BALANCE),
                    label_content=ft.Text("Transactions"),
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.ACCESS_TIME_FILLED_OUTLINED,
                    selected_icon=ft.Icon(ft.Icons.ACCESS_TIME_FILLED),
                    label_content=ft.Text("History"),
                ),
            ],
            on_change=self.on_change,
            # For testing
            # on_change=lambda e: print("Selected destination:", e.control.selected_index),
        )
    
    def on_change(self, e):
        # Call page.go() to navigate to the corresponding page
        if e.control.selected_index == 0:
            self.page.go("/dashboard")
        elif e.control.selected_index == 1:
            self.page.go("/accounts")
        elif e.control.selected_index == 2:
            self.page.go("/transactions")
        elif e.control.selected_index == 3:
            self.page.go("/history")