import flet as ft
import atexit
from routing import view_handler
from src.backend.database_creation.installation import Installation
from src.backend.database_interation.database import Database
from pathlib import Path
import time

def main(page: ft.Page):

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
        """This function is called when the app is closing."""
        print("App is attempting to close")
        page.overlay.clear()  # Remove all forms from the overlay
        page.controls.clear()  # Clear the main page's controls

    # Register the exit handler, queues up the on_exit funtion to run when closed
        # However you have to make sure to trigger it, this just queues it not calls it, must call for it to work
    atexit.register(on_exit) 

    # Initialize core classes
    db_instance = Database.get_instance(installer)


    """ UI SETUP   """
    page.title = "BudgetWise"
    page.padding = 0
    page.window.resizable = True  # Allow window resizing
    page.window.width = 1280  # Default width
    page.window.height = 800  # Default height
    page.window.center()  # Move window to center
    page.window.prevent_close = True  # Prevent immediate close

    views = view_handler(page, db_instance)

    def route_change(e):
        page.views.clear()
        new_view = views.get(page.route)  # Get the new view
        if new_view:
            page.views.append(new_view)
            page.update()
        else:
            print(f"Error: No view found for route {page.route}")  # Debugging

    def handle_window_event(e: ft.WindowEvent):
        if e.data == "close":  
            print("Closing app and cleaning up...")

            # Close database properly
            if db_instance.check_connection():
                db_instance.close_db()  # Ensure DB is properly closed

            # Optional: Small delay (only if needed)
            time.sleep(0.01)  

            print("Database closed. Exiting...")
            page.window.prevent_close = False
            page.window.close()  # close window
            #if mememory leaks or un closed connections use page. wiondow.destory(), however, takes 2 seconds to close when done



    # Set event handlers
    page.on_route_change = route_change
    page.window.on_event = handle_window_event  # Detect window close attempts

    # TODO: Change back to "/login"
    page.go("/login") 

ft.app(target=main)
