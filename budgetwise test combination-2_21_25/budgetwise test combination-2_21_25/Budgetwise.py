import flet as ft
import atexit
from Database import Database
from BWScenes import WelcomeScene
from BWDash import DashboardScene
from BWAccounts import AccountScene
from BWForms import LoginScene, SignInScene, SecurityQuestionsForm, AccountCreationForm, BudgetCreationForm
from DataManager import DataManager
from installation import Installation
from BWMenu import MenuBar  
from user import User
from pathlib import Path

def main(page: ft.Page):
    """
    Main entry point for the application. Initializes the necessary components, 
    sets up scenes, handles form visibility, and manages the overall app flow.

    Arguments:
        page (ft.Page): The Flet page object used to manage UI elements and user interactions.
    """
    installer = Installation()  # Create an Installation object to handle app setup tasks
    app_folder = Path(installer.get_app_folder())  # Get the app's folder path
    db_path = app_folder / installer.db_filename  # Determine the path for the database file
    
    # Check if the database exists. If not, create it.
    if not db_path.exists():
        print("Database not found. Creating a new encrypted Database...")
        installer.create_encrypted_database(db_path)  # Create the encrypted database
        print("Success: Encrypted Database created and key stored securely.")
    else:
        print("Database already exists. Starting application...")

    # Function to handle clean exit of the app
    def on_exit():
        """
        This function is called when the app is closing. It clears all UI elements 
        to prevent leftover elements on the screen.
        """
        print("App is attempting to close")
        page.overlay.clear()  # Remove all forms from the overlay
        page.controls.clear()  # Clear the main page's controls

    # DO NOT TOUCH THIS CODE. APP BREAKS.
    # Initialize core classes to ensure no duplicate class initialization
    BudgetDb = Database.get_instance(installer)  # Initialize the Database instance
    user_class_initialized = User(BudgetDb)  # Initialize the User class with the Database instance

    # Register the exit handler
    atexit.register(on_exit)

    # Check the database connection status
    if BudgetDb.check_connection:
        print("We are connected")
    else:
        print("Not Connected")
    
    #____________________________________________________________________
    # Set up page properties like title and window size
    page.title = "Welcome to BudgetWise"
    page.window_width = 1440  # Set the window width
    page.window_height = 1080  # Set the window height

    # Function to show different forms based on the given form parameter
    def show_form(form):
        """
        Shows the selected form and hides all other forms by updating their `open` property.
        
        Arguments:
            form (str): The form to be displayed (either login, signup, etc.).
        """
        # Control which form is visible by setting the 'open' property for each form
        login_form.open = form == login_form
        signin_form.open = form == signin_form
        security_questions_form.open = form == security_questions_form
        account_creation_form.open = form == account_creation_form
        page.update()  # Update the page to reflect changes

    # Function to toggle the visibility of the side menu
    def toggle_menu(e):
        """
        Toggles the visibility of the side menu.
        
        Arguments:
            e: The event passed when the button is clicked.
        """
        menu.visible = not menu.visible  # Toggle the visibility
        menu.width = 200 if menu.visible else 0  # Set the menu width based on visibility
        page.update()  # Update the page to reflect changes

    # Function to change the active scene
    def change_scene(scene_index):
        """
        Changes the current scene based on the provided index.
        
        Arguments:
            scene_index (int): The index of the scene to display from the 'scenes' list.
        """
        if 0 <= scene_index < len(scenes):  # Ensure the index is valid
            new_scene = scenes[scene_index]
            # If the scene has a refresh_ui method, call it to update the UI
            if hasattr(new_scene, "refresh_ui"):  
                new_scene.refresh_ui()
            scene_content.content = new_scene.get_content()  # Update the content of the scene
            toggle_button.disabled = scene_index == 0  # Disable the toggle button on the welcome scene
            page.update()  # Update the page to reflect the new scene

    # Define functions to show each form when needed
    def show_login_form():
        """
        Displays the login form.
        """
        print("Showing login form")
        show_form(login_form)

    def show_signin_form():
        """
        Displays the sign-in form.
        """
        print("Showing sign-in form")
        show_form(signin_form)

    def show_security_questions_form():
        """
        Displays the security questions form.
        """
        print("Showing security questions form")
        show_form(security_questions_form)

    def show_account_creation_form():
        """
        Displays the account creation form.
        """
        print("Showing account creation form")
        show_form(account_creation_form)

    def show_budget_creation_form():
        """
        Displays the budget creation form.
        """
        print("Showing budget creation form")
        budget_creation_form.on_close = scenes[1].on_budget_form_closed  # Set the on-close handler
        show_form(budget_creation_form)

    # Initialize all forms with necessary arguments
    login_form = LoginScene(change_scene_callback=change_scene, user_instance=user_class_initialized)
    signin_form = SignInScene(change_scene_callback=change_scene, show_security_questions_form=show_security_questions_form, user_instance=user_class_initialized)
    security_questions_form = SecurityQuestionsForm(change_scene_callback=change_scene, show_account_creation_form=show_account_creation_form, user_instance=user_class_initialized)
    account_creation_form = AccountCreationForm(change_scene_callback=change_scene)
    data_storage = DataManager()  # Initialize the data manager to handle data operations
    budget_creation_form = BudgetCreationForm(change_scene_callback=change_scene, data_manager=data_storage)

    # Set up scenes for the application
    scenes = [
        WelcomeScene(change_scene_callback=change_scene, show_login_form=show_login_form, show_signin_form=show_signin_form),
        DashboardScene(
            change_scene_callback=change_scene,
            p_width=page.window_width,
            p_height=page.window_height,
            show_budget_creation_form=show_budget_creation_form,
            budget_creation_form=budget_creation_form,  # Pass the budget creation form to the dashboard
            data_manager=data_storage
        ),
        AccountScene(
            change_scene_callback=change_scene,
            p_width=page.window_width,
            p_height=page.window_height,
            show_budget_creation_form=show_budget_creation_form,
            budget_creation_form=budget_creation_form,
            data_manager=data_storage
        )
    ]

    # Set up the side menu with a toggle button
    menu = MenuBar(change_scene_callback=change_scene)
    menu.visible = False  # Start with the menu hidden
    menu.width = 0  # Set the initial width to 0 (hidden)

    # The toggle button to open/close the side menu
    toggle_button = ft.ElevatedButton("Toggle Menu", on_click=toggle_menu, disabled=True)  # Initially disabled

    # Container for the scene content (main content area)
    scene_content = ft.Container(content=scenes[0].get_content(), expand=True)

    # Add forms to the overlay (forms are initially hidden)
    page.overlay.extend([login_form, signin_form, security_questions_form, account_creation_form, budget_creation_form])

    # Ensure all forms are closed initially
    login_form.open = False
    print("login form closed")
    signin_form.open = False
    print("signin form closed")
    security_questions_form.open = False
    print("security question form closed")
    account_creation_form.open = False
    print("account creation form closed")
    budget_creation_form.open = False
    print("budget creation form closed")

    # Create the main container that holds the side menu and the main content
    main_container = ft.Row(
        controls=[
            menu,  # Menu bar
            scene_content  # Main content area that changes based on the active scene
        ],
        spacing=0,
        expand=True
    )

    # Add the toggle button and the main container to the page
    page.add(
        ft.Row([toggle_button]),
        main_container
    )

    # Update the page to reflect all the changes made above
    page.update()

# Start the Flet application with the main function
ft.app(main)
