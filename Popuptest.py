import flet as ft
import atexit
from Database import database
from BWScenes import WelcomeScene, DashboardScene
from BWForms import LoginScene, SignInScene, SecurityQuestionsDialog
from BWMenu import MenuBar        
        
    

def main(page: ft.Page):
    page.title = "Welcome to BudgetWise"
    page.window_width = 1280
    page.window_height = 960

    menu_visible = False

    def toggle_menu(e):
        nonlocal menu_visible
        menu_visible = not menu_visible
        scenes[1].toggle_menu()
        page.update()

    def change_scene(scene_index):
        if 0 <= scene_index < len(scenes):
            scene_content.content = scenes[scene_index].get_content()
            toggle_button.disabled = scene_index == 0  # Disable toggle button for scene 0
            page.update()
        else:
            print(f"Error: Scene index {scene_index} is out of range.")

    login_form = LoginScene(change_scene_callback=change_scene)
    signin_form = SignInScene()

    def show_login_form():
        print("Showing login form")
        login_form.open = True
        signin_form.open = False
        page.update()

    def show_signin_form():
        print("Showing sign-in form")
        signin_form.open = True
        login_form.open = False
        page.update()

    scenes = [
        WelcomeScene(change_scene_callback=change_scene, show_login_form=show_login_form, show_signin_form=show_signin_form),
        DashboardScene(change_scene_callback=change_scene, p_width=page.window_width, p_height=page.window_height),
    ]

    menu = MenuBar(change_scene_callback=change_scene)

    toggle_button = ft.ElevatedButton("Toggle Menu", on_click=toggle_menu, disabled=True)  # Initially disabled
    scene_content = ft.Container(content=scenes[0].get_content(), expand=True)

    page.overlay.append(login_form)
    page.overlay.append(signin_form)
    page.overlay.append(signin_form.security_questions_dialog)  # Add security questions dialog to overlay

    page.add(
        ft.Row([toggle_button]),
        ft.Stack(
            controls=[
                scene_content,
                menu,
            ],
            expand=True
        )
    )

    page.update()

ft.app(main)

