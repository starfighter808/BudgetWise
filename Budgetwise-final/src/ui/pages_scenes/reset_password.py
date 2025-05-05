import flet as ft

class ResetPassword(ft.View):
    def __init__(self, page: ft.Page, user_data, colors):
        super().__init__(route="/reset_password", bgcolor= colors.BLUE_BACKGROUND)

        self.page = page
        self.user_data = user_data
        self.colors = colors

        # Input fields
        self.password = ft.TextField(
            label="New Password",
            label_style=ft.TextStyle(color=self.colors.BORDERBOX_COLOR), 
            text_style=ft.TextStyle(color=self.colors.TEXT_COLOR),
            hint_text="Enter your Password",
            hint_style=ft.TextStyle(color=self.colors.BLUE_BACKGROUND),
            focused_border_color=self.colors.BORDERBOX_COLOR, 
            password=True,
            can_reveal_password=True,
            width=400,
            on_change=self.toggle_continue_button
        )

        self.confirm_password = ft.TextField(
            label="Confirm Password",
            label_style=ft.TextStyle(color=self.colors.BORDERBOX_COLOR), 
            text_style=ft.TextStyle(color=self.colors.TEXT_COLOR),
            hint_text="Confirm your Password",
            hint_style=ft.TextStyle(color=self.colors.BLUE_BACKGROUND),
            focused_border_color=self.colors.BORDERBOX_COLOR, 
            password=True,
            can_reveal_password=True,
            width=400,
            on_change=self.toggle_continue_button
        )

        self.error_text = ft.Text("", color=self.colors.ERROR_RED)

        # Continue Button (Now Always Enabled)
        self.continue_button = ft.ElevatedButton(
            "Reset Password",
            on_click=self.reset_password,
            width=400,
            style=ft.ButtonStyle(
                color={ft.ControlState.DEFAULT: self.colors.TEXT_COLOR},
                bgcolor={ft.ControlState.DEFAULT: self.colors.GREEN_BUTTON},
                shape={ft.ControlState.DEFAULT: ft.RoundedRectangleBorder(radius=8)},
            ),
        )

        # Layout
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
                                # Left Column (Input Fields)
                                ft.Column(
                                    controls=[
                                        ft.Text(
                                            "Reset Password",
                                            text_align=ft.TextAlign.CENTER,
                                            size=24,
                                            weight=ft.FontWeight.BOLD,
                                            color=self.colors.TEXT_COLOR,
                                        ),
                                        self.password,
                                        self.confirm_password,
                                        self.error_text,
                                        self.continue_button,
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    expand=True,
                                ),
                                # Right Column (Branding)
                                ft.Column(
                                    controls=[
                                        ft.Icon(name=ft.Icons.LOCK_RESET, color=self.colors.GREEN_BUTTON, size=200),
                                        ft.Text("BudgetWise", size=24, weight=ft.FontWeight.BOLD, color=self.colors.TEXT_COLOR),
                                        ft.Text("The Future of Budgeting", size=12, weight=ft.FontWeight.NORMAL, color=self.colors.TEXT_COLOR),
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
    
    def toggle_continue_button(self, e=None):
        """ Enable or disable the continue button based on input validity (optional now) """
        password = self.password.value.strip()
        confirm_password = self.confirm_password.value.strip()

        # Ensure passwords match and meet security criteria
        # This is just for user feedback if you still want to show an error message:
        if password and confirm_password and password == confirm_password:
            self.error_text.value = ""
        else:
            self.error_text.value = "Passwords must match!"
        
        self.page.update()

    def reset_password(self, e):
        """Handles resetting the password."""
        new_password = self.password.value.strip()
        confirm_password = self.confirm_password.value.strip()
        username = self.user_data.username  # Get stored username

        # Validate password strength
        if not self.user_data.is_valid_password(new_password):
            self.error_text.value = "Password must be at least 8 characters long and contain an uppercase letter, lowercase letter, and a number."
            self.page.update()
            return

        # Ensure passwords match
        if new_password != confirm_password:
            self.error_text.value = "Passwords do not match!"
            self.page.update()
            return

        # Attempt password update
        if self.user_data.update_user_password(username, new_password):
            print(f"Password reset successful for user: {username}")
            self.confirm_password.value = ""
            self.page.go("/reset_password_success")
        else:
            self.error_text.value = "Failed to reset password. Please try again."
            self.page.update()
