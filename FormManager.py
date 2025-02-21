class FormManager:
    def __init__(self, budget_creation_form, dashboard_scene):
        self.budget_creation_form = budget_creation_form
        self.dashboard_scene = dashboard_scene
        self.ui_updater = dashboard_scene.ui_updater

    def show_form(self, form):
        self.budget_creation_form.open = form == self.budget_creation_form
        self.budget_creation_form.page.update()

    def remove_account(self, account_name):
        print(f"Removing account from budget form: {account_name}")
        self.budget_creation_form.summary_box.controls = [control for control in self.budget_creation_form.summary_box.controls if account_name not in control.value]
        self.budget_creation_form.summary_box.update()
        self.ui_updater.update_amounts(-self.get_amount(account_name))
        self.ui_updater.refresh_sliders()

    def get_amount(self, account_name):
        for control in self.budget_creation_form.summary_box.controls:
            if account_name in control.value:
                amount = float(control.value.split(": $")[1])
                return amount
        return 0

