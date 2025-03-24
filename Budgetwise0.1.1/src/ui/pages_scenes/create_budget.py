import flet as ft
from datetime import datetime

class CreateBudget(ft.View):
    def __init__(self, page: ft.Page, user_data, colors):
        super().__init__(route="/create_budget", bgcolor= colors.BLUE_BACKGROUND)

        self.page = page
        self.user_data = user_data
        self.colors = colors

        # UI Components
        self.budget_name = ft.TextField(label="Budget Name")
        self.budget_amount = ft.TextField(label="Budget Amount", keyboard_type=ft.KeyboardType.NUMBER)

        # Button handler: Save budget info and navigate to the next page
        self.save_button = ft.ElevatedButton(
            "Continue",
            on_click=self.save_budget_info,
            width=400,
            style=ft.ButtonStyle(
                color={
                    ft.ControlState.HOVERED: self.colors.TEXT_COLOR,
                    ft.ControlState.FOCUSED: self.colors.GREEN_BUTTON ,
                    ft.ControlState.DEFAULT: self.colors.TEXT_COLOR,
                },
                bgcolor={
                    ft.ControlState.FOCUSED: self.colors.GREEN_BUTTON,
                    "": self.colors.GREEN_BUTTON,
                },
                padding={ft.ControlState.HOVERED: 20},
                overlay_color= self.colors.TRANSPARENT,
                elevation={"pressed": 0, "": 2},
                animation_duration=300,
                side={
                    ft.ControlState.DEFAULT: ft.BorderSide(1, self.colors.GREEN_BUTTON),
                    ft.ControlState.HOVERED: ft.BorderSide(2, self.colors.GREEN_BUTTON),
                },
                shape={
                    ft.ControlState.HOVERED: ft.RoundedRectangleBorder(radius=20),
                    ft.ControlState.DEFAULT: ft.RoundedRectangleBorder(radius=8),
                },
            )
        )

        self.controls = [
            ft.Row(
                controls=[
                    ft.Container(
                        width=800,
                        height=410,
                        bgcolor=self.colors.GREY_BACKGROUND,
                        border_radius=10,
                        padding=20,
                        alignment=ft.alignment.center_right,
                        content=ft.Row(
                            controls=[
                                # Left column for form
                                ft.Column(
                                    controls=[
                                        ft.Text(
                                            "Create Budget",
                                            text_align=ft.TextAlign.CENTER,
                                            size=24,
                                            weight=ft.FontWeight.BOLD,
                                            color=self.colors.TEXT_COLOR
                                        ),
                                        self.budget_name,
                                        self.budget_amount,
                                        self.save_button,
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    expand=True,
                                ),
                                # Right column for logo and description
                                ft.Column(
                                    controls=[
                                        ft.Icon(name=ft.Icons.CALCULATE, color=self.colors.GREEN_BUTTON, size=200),
                                        ft.Text("BudgetWise", size=24, weight=ft.FontWeight.BOLD, color=self.colors.TEXT_COLOR),
                                        ft.Text("Create your monthly budget", size=12, weight=ft.FontWeight.NORMAL, color=self.colors.TEXT_COLOR),
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    expand=True,
                                ),
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

    def save_budget_info(self, e):
        """Validate and save budget info before proceeding."""
        # Get the budget values from the UI fields
        budget_name = self.budget_name.value.strip()
        budget_amount = self.budget_amount.value.strip()

        # Validate the budget name
        if not budget_name:
            self.budget_name.error_text = "Budget name cannot be empty"
            self.budget_name.update()
            return

        # Validate the budget amount
        if not budget_amount.isdigit():
            self.budget_amount.error_text = "Budget amount must be a valid number"
            self.budget_amount.update()
            return
        
        # Validate the deciaml places make sure it is 2 at most
        
        # Convert amount to integer after validation
        budget_amount = float(budget_amount)


        # Call or create token with userid, budget name, budget amount?
        # or add these values to a user token?

        # Store the information temporarily
        
        # Need the user id from the username maybe use token system during sign up?
        self.user_data.budget_name = budget_name
        self.user_data.budget_amount = budget_amount

        # Insert the budget information into the database through user_data
        self.user_data.create_budget(budget_name, budget_amount) # Need userid to work properly

        # Navigate to the next page (dashboard)
        self.page.go("/add_budget_accounts")  # Adjust the route if necessary
