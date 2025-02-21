import flet as ft

class UIUpdater:
    def __init__(self, dashboard_scene):
        self.dashboard_scene = dashboard_scene

    def update_amounts(self, amount):
        self.dashboard_scene.daily_spending += amount
        self.dashboard_scene.period_amount += amount
        self.dashboard_scene.current_balance += amount

        self.dashboard_scene.spending_info.controls[0].value = f"Daily Spending: ${self.dashboard_scene.daily_spending:.2f}"
        self.dashboard_scene.spending_info.controls[1].value = f"Period Amount: ${self.dashboard_scene.period_amount:.2f}"
        self.dashboard_scene.spending_info.controls[2].value = f"Current Balance: ${self.dashboard_scene.current_balance:.2f}"
        self.dashboard_scene.spending_info.update()

    def update_daily_spending(self):
        total_daily_spending = sum(
            control.controls[1].controls[0].value for control in self.dashboard_scene.slider_controls if isinstance(control.controls[1].controls[0], ft.Slider)
        )
        self.dashboard_scene.daily_spending = total_daily_spending
        self.dashboard_scene.spending_info.controls[0].value = f"Daily Spending: ${total_daily_spending:.2f}"
        self.dashboard_scene.spending_info.update()

    def refresh_sliders(self):
        self.dashboard_scene.scrollable_right_container.controls = [
            self.dashboard_scene.spending_info,
            self.dashboard_scene.add_transaction_button,
            ft.Text("Upcoming Payments:"),
            ft.Text("Car Payment - Due: 9/23/23"),
            *self.dashboard_scene.slider_controls
        ]
        self.dashboard_scene.scrollable_right_container.update()
        self.dashboard_scene.scrollable_main_content.update()