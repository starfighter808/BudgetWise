import flet as ft

class Dashboard(ft.View):
    def __init__(self, page: ft.Page, user_repo, NavRail):
        super().__init__(route="/dashboard", bgcolor="#5C9DFF")
    
        self.controls.append(ft.Text("Dashbaord"))

        title_row = ft.Row( # This is the title of the page
        [
            ft.Text("Dashboard", size=30, weight="bold")
        ],
        alignment=ft.MainAxisAlignment.CENTER, 
        expand=False, 
        )

        content = ft.Column(
            [
                title_row,

                # ----------------- PAGE CONTENT GOES BELOW -----------------

                ft.Text("Page Content", size=15, text_align=ft.TextAlign.CENTER),

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