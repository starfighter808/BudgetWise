# Normal Python library imports
import flet as ft
from argon2 import PasswordHasher
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
# user data class
from src.backend.database_interation.user_data import UserData
# components
from src.ui.components.navigation_rail import NavRail



def view_handler(page: ft.Page, db_instance):
    user_repo = UserData(db_instance)  
    password_hasher = PasswordHasher() 
    nav_rail = NavRail(page) 


    return {
        "/login": Login(page, user_repo, password_hasher),
        "/sign_up": SignUp(page, user_repo, password_hasher),
        "/security_questions": SecurityQuestions(page, user_repo, password_hasher), 
        "/create_budget": CreateBudget(page, user_repo),  
        "/dashboard": Dashboard(page, user_repo, nav_rail),
        "/username_verification": UsernameVerification(page, user_repo),
        "/forgot_password_questions": ForgotPasswordQuestions(page, user_repo, password_hasher),
        "/reset_password": ResetPassword(page, user_repo, password_hasher),
        "/reset_password_success": ResetPasswordSuccess(page),
        "/add_budget_accounts": AddBudgetAccounts(page, user_repo),
        "/accounts": Accounts(page, user_repo, nav_rail),
        "/transactions": Transactions(page, user_repo, nav_rail),
        "/history": History(page, user_repo, nav_rail),
    }
