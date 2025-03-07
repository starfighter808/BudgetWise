import flet as ft

class Dashboard(ft.View):
    def __init__(self, page: ft.Page, user_repo):
        super().__init__(route="/dashboard", bgcolor="#5C9DFF")
    
        self.controls.append(ft.Text("Dashbaord"))
    