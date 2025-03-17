import flet as ft

class CreateBudget(ft.View):
    def __init__(self, page: ft.Page, user_data):
        super().__init__(route="/create_budget", bgcolor="#5C9DFF")

        self.page = page
        self.user_data = user_data 

        self.budget_name = ft.TextField(label="Budget Name")
        self.budget_amount = ft.TextField(label="Budget Amount", keyboard_type=ft.KeyboardType.NUMBER)

        def save_budget_info(e):
            """Validate and save budget info before proceeding."""
            budget_name = self.budget_name.value.strip()
            budget_amount = self.budget_amount.value.strip()

            if not budget_name:
                self.budget_name.error_text = "Budget name cannot be empty"
                self.budget_name.update()
                return

            if not budget_amount.isdigit():
                self.budget_amount.error_text = "Budget amount must be a number"
                self.budget_amount.update()
                return

            # Store in temp_info dictionary
            self.user_data.temp_info["budget_name"] = budget_name
            self.user_data.temp_info["budget_amount"] = int(budget_amount)  

            print("Updated temp_info:", self.user_data.temp_info) 

            self.page.go("/dashboard")  # TODO: ensure this says '/final_step'

        self.controls = [
            ft.Row(
                controls=[
                    ft.Container(
                        width=800,
                        height=410,
                        bgcolor="#40444B",
                        border_radius=10,
                        padding=20,
                        alignment=ft.alignment.center_right,
                        content=ft.Row(
                            controls=[
                                # First column
                                ft.Column(
                                    controls=[
                                        ft.Text(
                                            "Create Budget",
                                            text_align=ft.TextAlign.CENTER,
                                            size=24,
                                            weight=ft.FontWeight.BOLD,
                                            color=ft.Colors.WHITE
                                        ),
                                        self.budget_name,
                                        self.budget_amount,
                                        ft.ElevatedButton(
                                            "Continue",
                                            on_click=save_budget_info, 
                                            width=400,
                                            style=ft.ButtonStyle(
                                                color={
                                                    ft.ControlState.HOVERED: ft.Colors.WHITE,
                                                    ft.ControlState.FOCUSED: ft.Colors.GREEN_200,
                                                    ft.ControlState.DEFAULT: ft.Colors.WHITE,
                                                },
                                                bgcolor={
                                                    ft.ControlState.FOCUSED: ft.Colors.GREEN,
                                                    "": ft.Colors.GREEN,
                                                },
                                                padding={ft.ControlState.HOVERED: 20},
                                                overlay_color=ft.Colors.TRANSPARENT,
                                                elevation={"pressed": 0, "": 2},
                                                animation_duration=300,
                                                side={
                                                    ft.ControlState.DEFAULT: ft.BorderSide(1, ft.Colors.GREEN),
                                                    ft.ControlState.HOVERED: ft.BorderSide(2, ft.Colors.GREEN),
                                                },
                                                shape={
                                                    ft.ControlState.HOVERED: ft.RoundedRectangleBorder(radius=20),
                                                    ft.ControlState.DEFAULT: ft.RoundedRectangleBorder(radius=8),
                                                },
                                            )
                                        ),
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    expand=True,
                                ),
                                # Second column
                                ft.Column(
                                    controls=[
                                        ft.Icon(name=ft.Icons.CALCULATE, color=ft.Colors.GREEN, size=200),
                                        ft.Text("BudgetWise", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                                        ft.Text("Create your monthly budget", size=12, weight=ft.FontWeight.NORMAL, color=ft.Colors.WHITE),
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    expand=True,
                                )   
                            ],
                            expand=True,
                        ),
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True,
            ),
        ]
