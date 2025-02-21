**Important**:
**All required libraries must be installed for the code to work. This is not an executable (.exe) file.**

You will need:

**Flet**

    pip install flet
    
You may need the latest version:

    pip install --upgrade flet

**sqlcipher3-wheels**

    pip install sqlcipher3-wheels

**keyring**

    pip install keyring

**argon2**

     pip install argon2-cffi

The BudgetWise test combination folder is the first attempt at gathering all the code together and implementing it as a unified system. To run the code, simply execute the BudgetWise.py program.

When you run BudgetWise.py, it will:

    Create the database if it does not exist.
    Encrypt the database.
    Launch the Flet scenes.
    Allow for user sign-ups and logins.

Additionally, there is a folder called check_database, which contains a program named tamper_with_database.py. This program allows you to verify whether data has been properly written to the database in command line form.

As of February 18, 2025, the code has not been tested on macOS or Linux. It has been tested and confirmed to work on Windows 10. However, the functionality of vendor2.py and transactions2.py has not been verified. The rest of the code is working as expected. Moving forward, I believe all development should be built on top of this code as a base.

I also have a backup version stored in my branch.
