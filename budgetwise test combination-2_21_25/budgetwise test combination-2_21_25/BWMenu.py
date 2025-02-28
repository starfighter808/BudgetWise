import flet as ft

class MenuBar(ft.Column):
    def __init__(self, change_scene_callback):
        super().__init__(
            controls=[
                ft.ElevatedButton(
                    content=ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.DASHBOARD),
                            ft.Text("Dashboard")
                        ],
                        spacing=5
                    ),
                    on_click=lambda e: change_scene_callback(1)
                ),
                ft.ElevatedButton(
                    content=ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.ACCOUNT_BALANCE),
                            ft.Text("Accounts")
                        ],
                        spacing=5
                    ),
                    on_click=lambda e: change_scene_callback(2)
                ),
                ft.ElevatedButton(
                    content=ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.HISTORY),
                            ft.Text("History")
                        ],
                        spacing=5
                    ),
                    on_click=lambda e: change_scene_callback(3)
                ),
                ft.ElevatedButton(
                    content=ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.SWAP_HORIZ),
                            ft.Text("Transactions")
                        ],
                        spacing=5
                    ),
                    on_click=lambda e: change_scene_callback(4)
                ),
                ft.ElevatedButton(
                    content=ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.NOTIFICATIONS),
                            ft.Text("Notifications")
                        ],
                        spacing=5
                    ),
                    on_click=lambda e: change_scene_callback(5)
                ),
                ft.ElevatedButton(
                    content=ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.ACCOUNT_BOX),
                            ft.Text("Preferences")
                        ],
                        spacing=5
                    ),
                    on_click=lambda e: change_scene_callback(6)
                ),
                ft.ElevatedButton(
                    content=ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.SETTINGS),
                            ft.Text("Settings")
                        ],
                        spacing=5
                    ),
                    on_click=lambda e: change_scene_callback(7)
                )
            ],
            width=150,
            height=960,  # adjust as needed
            visible=False
        )