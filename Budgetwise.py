import flet as ft
import atexit
from Database import database
from BWScenes import WelcomeScene
from BWForms import LoginScene, SignInScene, SecurityQuestionsDialog
from BWMenu import MenuBar        
        
    

def main(page: ft.Page):
    BudgetDb = database('Budgetwise')

    def on_exit():
    
        print("App is attempting to close")
        BudgetDb.close_db
    
        if BudgetDb.check_connection != True:
            print("Database disconnected")
        else:
            print("Error")
        
        return True

    # Register the on_exit function to be called on exit
    atexit.register(on_exit)
    
    if BudgetDb.check_connection:
        print("We are connected")
    else:
        print("Not Connected")

    page.title = "Welcome to BudgetWise"
    page.window_width = 1280
    page.window_height = 960

    menu_visible = False

    def toggle_menu(e):
        nonlocal menu_visible
        menu_visible = not menu_visible
        menu.visible = menu_visible
        page.update()

    def change_scene(scene_index):
        if 0 <= scene_index < len(scenes):
            scene_content.content = scenes[scene_index].get_content()
            page.update()
        else:
            print(f"Error: Scene index {scene_index} is out of range.")

    login_form = LoginScene()
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
    ]

    menu = MenuBar(change_scene_callback=change_scene)

    toggle_button = ft.ElevatedButton("Toggle Menu", on_click=toggle_menu)
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