import flet as ft
import atexit
from Database import Database
from BWScenes import WelcomeScene
from BWDash import DashboardScene
from BWAccounts import AccountScene
from BWTransactions import TransactionScene
from BWForms import LoginScene, SignInScene, SecurityQuestionsForm, AccountCreationForm, BudgetCreationForm, TransactionsForm
from DataManager import DataManager
from installation import Installation
from BWHistory import HistoryScene
from BWMenu import MenuBar    
import os
from user import User
from pathlib import Path