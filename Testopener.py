import os
from Database import database

BudgetDb = database('Budgetwise')

if BudgetDb.check_connection:
    print("We are connected")
else:
    print("Problem")

BudgetDb.close_db

if BudgetDb.check_connection != True:
    print("No longer connected")
else:
    print("Problem 2")

BudgetDb.open_db

if BudgetDb.check_connection:
    print("We are connected")
else:
    print("Problem 3")

BudgetDb.close_db

print("Test Complete")



