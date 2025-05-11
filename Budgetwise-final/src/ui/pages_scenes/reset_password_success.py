import flet as ft

class ResetPasswordSuccess(ft.View):
    def __init__(self, page: ft.Page, colors):
        super().__init__(route="/reset_password_success", bgcolor= colors.BLUE_BACKGROUND)
        self.page = page

        self.colors = colors

        # Success message
        success_message = ft.Text(
            "Password Reset Successfully!",
            text_align=ft.TextAlign.CENTER,
            size=24,
            weight=ft.FontWeight.BOLD,
            color=self.colors.TEXT_COLOR,
        )

        instruction_message = ft.Text(
            "Click the button below to return to the login page.",
            text_align=ft.TextAlign.CENTER,
            size=16,
            color=self.colors.TEXT_COLOR,
        )

        # Continue Button
        continue_button = ft.ElevatedButton(
            "Continue to Login",
            on_click=lambda e: self.page.go("/login"),
            width=250,
            style=ft.ButtonStyle(
                color={ft.ControlState.DEFAULT: self.colors.TEXT_COLOR},
                bgcolor={ft.ControlState.DEFAULT: self.colors.GREEN_BUTTON},
                overlay_color=self.colors.TRANSPARENT,
                elevation={"pressed": 0, "": 2},
                shape={ft.ControlState.DEFAULT: ft.RoundedRectangleBorder(radius=8)},
            ),
        )

        # Layout
        self.controls = [
            ft.Row(
                controls=[ 
                    ft.Container(
                        width=800,
                        height=350,
                        bgcolor=self.colors.GREY_BACKGROUND,
                        border_radius=10,
                        padding=20,
                        alignment=ft.alignment.center,
                        content=ft.Column(
                            controls=[
                                ft.Icon(name=ft.Icons.VERIFIED_USER, color=self.colors.GREEN_BUTTON, size=100),
                                success_message,
                                instruction_message,
                                continue_button,
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=20,
                        ),
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True,
            ),
        ]
