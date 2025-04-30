# Normal Python library imports
import flet as ft

# Colors
from src.ui.components.colors import Colors

# Login
from src.ui.pages_scenes.login import Login

# Sign up/account set up pages
from src.ui.pages_scenes.sign_up import SignUp
from src.ui.pages_scenes.security_questions import SecurityQuestions
from src.ui.pages_scenes.create_budget import CreateBudget
from src.ui.pages_scenes.add_budget_accounts import AddBudgetAccounts

# Forgot password/reset passwor pages
from src.ui.pages_scenes.username_verification import UsernameVerification
from src.ui.pages_scenes.forgot_password_questions import ForgotPasswordQuestions
from src.ui.pages_scenes.reset_password_success import ResetPasswordSuccess
from src.ui.pages_scenes.reset_password import ResetPassword

# Main pages
from src.ui.pages_scenes.dashboard import Dashboard
from src.ui.pages_scenes.accounts import Accounts
from src.ui.pages_scenes.transactions import Transactions
from src.ui.pages_scenes.history import History
from src.ui.pages_scenes.reports import Reports
from src.ui.pages_scenes.accounts_popup import MakeEdits


# user data class
from src.backend.database_interation.user_data import UserData # <------LOOK HERE
from src.backend.database_interation.trans_class import TransClass
from src.backend.database_interation.vendor_funcs import Vendor

# components
from src.ui.components.navigation_rail import NavRail


def view_handler(page: ft.Page, db_instance):
    user_data = UserData(db_instance) 
    colors = Colors() 
    nav_rail = NavRail(page, user_data) 
    vend_funcs = Vendor(db_instance)
    trans_funcs = TransClass(user_data)

    return {
        "/login": Login(page, user_data, colors),
        "/sign_up": SignUp(page, user_data, colors),
        "/security_questions": SecurityQuestions(page, user_data, colors), 
        "/create_budget": CreateBudget(page, user_data, colors),  
        "/dashboard": Dashboard(page, user_data, nav_rail, colors),
        "/username_verification": UsernameVerification(page, user_data, colors), 
        "/forgot_password_questions": ForgotPasswordQuestions(page, user_data, colors), 
        "/reset_password": ResetPassword(page, user_data, colors),
        "/reset_password_success": ResetPasswordSuccess(page, colors),
        "/add_budget_accounts": AddBudgetAccounts(page, user_data, colors),
        "/accounts": Accounts(page, user_data, nav_rail, colors),
        "/transactions": Transactions(page, user_data, nav_rail, colors, trans_funcs, vend_funcs),
        "/history": History(page, user_data, nav_rail, colors),
    }
