import flet as ft
import atexit
from Database import database
from BWScenes import WelcomeScene
from BWDash import DashboardScene
from BWAccounts import AccountScene
from BWForms import LoginScene, SignInScene, SecurityQuestionsForm, AccountCreationForm, BudgetCreationForm
from DataManager import DataManager
from installation import Installation
from BWHistory import HistoryScene
from BWMenu import MenuBar    
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
    
    if BudgetDb.check_connection:
        print("We are connected")
    else:
        print("Not Connected")
    
    #____________________________________________________________________

    page.title = "Welcome to BudgetWise"
    page.window_width = 1440
    page.window_height = 1080

    def show_form(form):
        login_form.open = form == login_form
        signin_form.open = form == signin_form
        security_questions_form.open = form == security_questions_form
        account_creation_form.open = form == account_creation_form
        page.update()

    def toggle_menu(e):
        menu.visible = not menu.visible
        menu.width = 200 if menu.visible else 0  # Adjust the width of the menu
        page.update()

    def change_scene(scene_index):
        if 0 <= scene_index < len(scenes):
            new_scene = scenes[scene_index]
            scene_content.content = new_scene.get_content()  # ✅ Switch the scene first
            page.update()  # ✅ Ensure the new scene is fully added before further updates
            
            if hasattr(new_scene, "refresh_ui"):
                new_scene.refresh_ui()  # ✅ Refresh the UI elements after it's added to the page
            
            toggle_button.disabled = scene_index == 0  # ✅ Ensure it's enabled for Scene 1+
            toggle_button.update()  # ✅ Force the UI update for the button

    # Define show functions
    def show_login_form():
        print("Showing login form")
        show_form(login_form)

    def show_signin_form():
        print("Showing sign-in form")
        show_form(signin_form)

    def show_security_questions_form():
        print("Showing security questions form")
        show_form(security_questions_form)

    def show_account_creation_form():
        print("Showing account creation form")
        show_form(account_creation_form)
    
    def show_budget_creation_form():
        print("Showing budget creation form")
        budget_creation_form.on_close = scenes[1].on_budget_form_closed  # ✅ Ensure it refreshes the dashboard
        show_form(budget_creation_form)

    # Initialize all forms with necessary arguments
    login_form = LoginScene(change_scene_callback=change_scene)
    signin_form = SignInScene(change_scene_callback=change_scene, show_security_questions_form=show_security_questions_form)
    security_questions_form = SecurityQuestionsForm(change_scene_callback=change_scene, show_account_creation_form=show_account_creation_form)
    account_creation_form = AccountCreationForm(change_scene_callback=change_scene)
    data_storage = DataManager()
    budget_creation_form = BudgetCreationForm(
        change_scene_callback=change_scene,
        data_manager=data_storage
    )

    # Set up scenes
    scenes = [
        WelcomeScene(change_scene_callback=change_scene, show_login_form=show_login_form, show_signin_form=show_signin_form),
        DashboardScene(
            change_scene_callback=change_scene,
            p_width=page.window_width,
            p_height=page.window_height,
            show_budget_creation_form=show_budget_creation_form,
            budget_creation_form=budget_creation_form,  # Pass the budget creation form to the dashboard scene
            data_manager = data_storage
        ),
        AccountScene(
            change_scene_callback = change_scene, 
            p_width = page.window_width, 
            p_height = page.window_height,
            show_budget_creation_form=show_account_creation_form,
            budget_creation_form=budget_creation_form, 
            data_manager = data_storage
        ),
        HistoryScene(
            change_scene_callback = change_scene, 
            p_width = page.window_width, 
            p_height = page.window_height,
            data_manager = data_storage
        )
    ]

    menu = MenuBar(change_scene_callback=change_scene)
    menu.visible = False  # Start with the menu hidden
    menu.width = 0  # Start with the menu width set to 0

    toggle_button = ft.ElevatedButton("Toggle Menu", on_click=toggle_menu, disabled=True)  # Initially disabled
    scene_content = ft.Container(content=scenes[0].get_content(), expand=True)

    # Add forms to the overlay, keeping them closed initially
    page.overlay.extend([login_form, signin_form, security_questions_form, account_creation_form, budget_creation_form])

    # Ensure all forms are closed initially
    login_form.open = False
    signin_form.open = False
    security_questions_form.open = False
    account_creation_form.open = False
    budget_creation_form.open = False

    # Create a container that includes the menu bar and the main content
    main_container = ft.Row(
        controls=[
            menu,  # Menu bar
            scene_content  # Main content
        ],
        spacing=0,
        expand=True
    )

    page.add(
        ft.Row([toggle_button]),
        main_container
    )

    page.update()

ft.app(main)