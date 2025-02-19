import flet as ft
import atexit
from Database import database
from BWScenes import WelcomeScene, DashboardScene
from BWForms import LoginScene, SignInScene, SecurityQuestionsDialog
from BWMenu import MenuBar
from installation import Installation
import os
from login import Login

def main(page: ft.Page):

    installer = Installation()
    app_folder = installer.get_app_folder()
    db_path = os.path.join(app_folder, installer.db_filename)
    
    # Check if the database already exists. If not, create it.
    if not os.path.exists(db_path):
        print("Database not found. Creating a new encrypted database...")
        installer.create_encrypted_database()
        print("Success: Encrypted database created and key stored securely.")
    else:
        print("Database already exists. Starting application...")

    # DO NOT TOUCH THIS CODE. APP BREAKS
    BudgetDb = database()

    def on_exit():
        print("App is attempting to close")

        # Ensure the database connection is closed in the same thread
        if BudgetDb.check_connection():
            BudgetDb.close_db()

        if BudgetDb.check_connection() != True:
            print("Database disconnected")
        else:
            print("Error")
        return True


    # Register the on_exit function to be called on exit
    atexit.register(on_exit)
    
    if BudgetDb.check_connection():
        print("We are connected")
    else:
        print("Not Connected")
    
    # ____________________________________________________________________

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
