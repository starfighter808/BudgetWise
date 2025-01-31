import flet as ft
import atexit
from Database import database
from BWScenes import WelcomeScene, LoginScene
        
        
    

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
            scene_content.content = scenes[scene_index].get_content().content
            page.update()
        else:
            print(f"Error: Scene index {scene_index} is out of range.")

    scenes = [
        WelcomeScene(change_scene_callback=change_scene),
        LoginScene()
    ]

    menu = ft.Column(
    controls=[
        ft.ElevatedButton(
            content=ft.Row(
                controls=[
                    ft.Icon(ft.Icons.DASHBOARD),
                    ft.Text("Dashboard")
                ],
                spacing=5
            ),
            on_click=lambda e: change_scene(3)
        ),
        ft.ElevatedButton(
            content=ft.Row(
                controls=[
                    ft.Icon(ft.Icons.ACCOUNT_BALANCE),
                    ft.Text("Accounts")
                ],
                spacing=5
            ),
            on_click=lambda e: change_scene(4)
        ),
        ft.ElevatedButton(
            content=ft.Row(
                controls=[
                    ft.Icon(ft.Icons.HISTORY),
                    ft.Text("History")
                ],
                spacing=5
            ),
            on_click=lambda e: change_scene(5)
        ),
        ft.ElevatedButton(
            content=ft.Row(
                controls=[
                    ft.Icon(ft.Icons.SWAP_HORIZ),
                    ft.Text("Transactions")
                ],
                spacing=5
            ),
            on_click=lambda e: change_scene(6)
        ),
        ft.ElevatedButton(
            content=ft.Row(
                controls=[
                    ft.Icon(ft.Icons.NOTIFICATIONS),
                    ft.Text("Notifications")
                ],
                spacing=5
            ),
            on_click=lambda e: change_scene(7)
        ),
        ft.ElevatedButton(
            content=ft.Row(
                controls=[
                    ft.Icon(ft.Icons.ACCOUNT_BOX),
                    ft.Text("Preferences")
                ],
                spacing=5
            ),
            on_click=lambda e: change_scene(8)
        ),
        ft.ElevatedButton(
            content=ft.Row(
                controls=[
                    ft.Icon(ft.Icons.SETTINGS),
                    ft.Text("Settings")
                ],
                spacing=5
            ),
            on_click=lambda e: change_scene(9)
        )
    ],
    width=150,
    height=page.window_height,
    visible=False
)

    toggle_button = ft.ElevatedButton("Toggle Menu", on_click=toggle_menu)
    scene_content = ft.Container(content=scenes[0].get_content().content, expand=True)

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
