import flet as ft
import atexit
from Database import database
from BWScenes import WelcomeScene, DashboardScene
from BWForms import LoginScene, SignInScene, SecurityQuestionsForm, AccountCreationForm, BudgetCreationForm
from BWMenu import MenuBar        

def main(page: ft.Page):
    page.title = "Welcome to BudgetWise"
    page.window_width = 1440
    page.window_height = 1080
    p_width = 1440
    p_height = 1080

    def show_form(form):
        login_form.open = form == login_form
        signin_form.open = form == signin_form
        security_questions_form.open = form == security_questions_form
        account_creation_form.open = form == account_creation_form
        budget_creation_form.open = form == budget_creation_form
        page.update()

    def toggle_menu(e):
        menu.visible = not menu.visible
        menu.width = 200 if menu.visible else 0  # Adjust the width of the menu
        page.update()

    def change_scene(scene_index):
        if 0 <= scene_index < len(scenes):
            scene_content.content = scenes[scene_index].get_content()
            toggle_button.disabled = scene_index == 0
            page.update()
        else:
            print(f"Error: Scene index {scene_index} is out of range.")

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
        show_form(budget_creation_form)

    login_form = LoginScene(change_scene_callback=change_scene)
    signin_form = SignInScene(change_scene_callback=change_scene, show_security_questions_form=show_security_questions_form)
    security_questions_form = SecurityQuestionsForm(change_scene_callback=change_scene, show_account_creation_form=show_account_creation_form)
    account_creation_form = AccountCreationForm(change_scene_callback=change_scene)

    budget_creation_form = BudgetCreationForm(
        change_scene_callback=change_scene,
        add_slider_callback=None,  # Temporarily set to None until dashboard_scene is created
        remove_account_callback=None  # Temporarily set to None until dashboard_scene is created
    )

    dashboard_scene = DashboardScene(
        change_scene_callback=change_scene,
        p_width=p_width,
        p_height=p_height,
        show_budget_creation_form=show_budget_creation_form,
        budget_creation_form=budget_creation_form  # Pass the budget creation form to the dashboard scene
    )

    budget_creation_form.add_slider_callback = dashboard_scene.add_slider
    budget_creation_form.remove_account_callback = dashboard_scene.form_manager.remove_account

    scenes = [
        WelcomeScene(change_scene_callback=change_scene, show_login_form=show_login_form, show_signin_form=show_signin_form),
        dashboard_scene
    ]

    menu = MenuBar(change_scene_callback=change_scene)
    menu.visible = False
    menu.width = 0

    toggle_button = ft.ElevatedButton("Toggle Menu", on_click=toggle_menu, disabled=True)
    scene_content = ft.Container(content=scenes[0].get_content(), expand=True)

    page.overlay.extend([login_form, signin_form, security_questions_form, account_creation_form, budget_creation_form])

    login_form.open = False
    signin_form.open = False
    security_questions_form.open = False
    account_creation_form.open = False
    budget_creation_form.open = False

    main_container = ft.Row(
        controls=[
            menu,
            scene_content
        ],
        spacing=0,
        expand=True
    )

    page.add(
        ft.Row([toggle_button]),
        main_container
    )

    page.update()

ft.app(target=main)
