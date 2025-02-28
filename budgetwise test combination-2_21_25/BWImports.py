import flet as ft
import atexit
from Database import database
from BWScenes import WelcomeScene
from BWDash import DashboardScene
from BWAccounts import AccountScene
from BWTransactions import TransactionScene
from BWForms import LoginScene, SignInScene, SecurityQuestionsForm, AccountCreationForm, BudgetCreationForm
from DataManager import DataManager
from installation import Installation
from BWHistory import HistoryScene
from BWMenu import MenuBar    
import os
from login import Login