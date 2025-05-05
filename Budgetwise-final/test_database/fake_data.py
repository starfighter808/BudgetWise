import os
import keyring
from pathlib import Path
import sys
import platform
import sqlcipher3


app_name = "BudgetWise"
db_filename = "BudgetWise.db"

def get_app_folder():
    """Return the proper application folder depending on the OS and create it if needed."""
        
    os_type = platform.system() 

    if os_type == "Windows":
        app_folder = os.path.join(os.getenv("APPDATA"), app_name)  
    elif os_type == "Darwin":  
        app_folder = os.path.join(os.path.expanduser("~/Library/Application Support"), app_name)  
    elif os_type == "Linux":  
        app_folder = os.path.join(os.path.expanduser("~/.local/share"), app_name) 
        print(app_folder)
    else:
        raise ValueError(f"Unsupported OS: {os_type}")

    os.makedirs(app_folder, exist_ok=True) 
    return app_folder

def fake_data():
    """Allows developers to interact with the encrypted database until they choose to exit."""
    app_folder = get_app_folder()
    Path(app_folder).mkdir(parents=True, exist_ok=True)
    db_path = os.path.join(app_folder, db_filename)

    # Retrieve the database password from keyring
    password = keyring.get_password(app_name, "db_password")
    if password is None:
        print("Error: No password found for the database. Cannot proceed.")
        return

    try:
        conn = sqlcipher3.connect(db_path)
        # Be cautious: if the password contains special characters like a single quote,
        # you might need additional handling or escaping.
        conn.execute(f"PRAGMA key='{password}'")
        conn.execute("PRAGMA foreign_keys = 1")
        cursor = conn.cursor()


        ### ADD TO TOP OF SCRIPT IF NOT WORKING ###
        # DELETE FROM transactions;
        # DELETE FROM budget_accounts;
        # DELETE FROM budgets;
        # DELETE FROM vendors;
        # DELETE FROM users;

        ### Password for all user is also Password1 it is being left as argon2 so it should just work if inserted ###
        print("Connected to the database. Attempting to insert data!")
        sql_script = """
            -- user data
            INSERT OR IGNORE INTO users (
                user_id, username, password_hash,
                alerts_enabled, default_chart, weekly_reports, monthly_reports, yearly_reports,
                security_question1, security_question2, security_question3,
                security_question1_answer, security_question2_answer, security_question3_answer
            ) VALUES
            (1, 'user1', '$argon2id$v=19$m=65536,t=3,p=4$5oIX8NY1s0/iqOrHH6Nlag$iwJFMpQwgY9iZqWErCDfpBJSKnX6rH1/iYkYa1KOmd0', 1, 0, 0, 0, 0,
            'What was the name of your first pet?', 'What was the make and model of your first car?', 'What is the name of your favorite childhood book?',
            '$argon2id$v=19$m=65536,t=3,p=4$JMNDlTyRqXmws2mpxMTFcg$yGhIIkq8LiJMI5LjnOMIvP3HsOqts1qmgBNnBC02Fiw',
            '$argon2id$v=19$m=65536,t=3,p=4$UG/Ew7+GgpO5iEr7ZeWuCw$SO23bV4/wQS9Xln4hKa0r6/CV3ctBjP6ZzJHcBYl11k',
            '$argon2id$v=19$m=65536,t=3,p=4$oc+PaL1B7uxMXbIiTAozIw$Dbtbs5sY50lyAWu9ITfOeLKt8bKDy+Ph8qsfPRsAxg0'),

            (2, 'user2', '$argon2id$v=19$m=65536,t=3,p=4$5oIX8NY1s0/iqOrHH6Nlag$iwJFMpQwgY9iZqWErCDfpBJSKnX6rH1/iYkYa1KOmd0', 1, 0, 0, 0, 0,
            'What was the name of your first pet?', 'What was the make and model of your first car?', 'What is the name of your favorite childhood book?',
            '$argon2id$v=19$m=65536,t=3,p=4$JMNDlTyRqXmws2mpxMTFcg$yGhIIkq8LiJMI5LjnOMIvP3HsOqts1qmgBNnBC02Fiw',
            '$argon2id$v=19$m=65536,t=3,p=4$UG/Ew7+GgpO5iEr7ZeWuCw$SO23bV4/wQS9Xln4hKa0r6/CV3ctBjP6ZzJHcBYl11k',
            '$argon2id$v=19$m=65536,t=3,p=4$oc+PaL1B7uxMXbIiTAozIw$Dbtbs5sY50lyAWu9ITfOeLKt8bKDy+Ph8qsfPRsAxg0'),

            (3, 'user3', '$argon2id$v=19$m=65536,t=3,p=4$5oIX8NY1s0/iqOrHH6Nlag$iwJFMpQwgY9iZqWErCDfpBJSKnX6rH1/iYkYa1KOmd0', 1, 0, 0, 0, 0,
            'What was the name of your first pet?', 'What was the make and model of your first car?', 'What is the name of your favorite childhood book?',
            '$argon2id$v=19$m=65536,t=3,p=4$JMNDlTyRqXmws2mpxMTFcg$yGhIIkq8LiJMI5LjnOMIvP3HsOqts1qmgBNnBC02Fiw',
            '$argon2id$v=19$m=65536,t=3,p=4$UG/Ew7+GgpO5iEr7ZeWuCw$SO23bV4/wQS9Xln4hKa0r6/CV3ctBjP6ZzJHcBYl11k',
            '$argon2id$v=19$m=65536,t=3,p=4$oc+PaL1B7uxMXbIiTAozIw$Dbtbs5sY50lyAWu9ITfOeLKt8bKDy+Ph8qsfPRsAxg0'),

            (4, 'user4', '$argon2id$v=19$m=65536,t=3,p=4$5oIX8NY1s0/iqOrHH6Nlag$iwJFMpQwgY9iZqWErCDfpBJSKnX6rH1/iYkYa1KOmd0', 1, 0, 0, 0, 0,
            'What was the name of your first pet?', 'What was the make and model of your first car?', 'What is the name of your favorite childhood book?',
            '$argon2id$v=19$m=65536,t=3,p=4$JMNDlTyRqXmws2mpxMTFcg$yGhIIkq8LiJMI5LjnOMIvP3HsOqts1qmgBNnBC02Fiw',
            '$argon2id$v=19$m=65536,t=3,p=4$UG/Ew7+GgpO5iEr7ZeWuCw$SO23bV4/wQS9Xln4hKa0r6/CV3ctBjP6ZzJHcBYl11k',
            '$argon2id$v=19$m=65536,t=3,p=4$oc+PaL1B7uxMXbIiTAozIw$Dbtbs5sY50lyAWu9ITfOeLKt8bKDy+Ph8qsfPRsAxg0'),

            (5, 'user5', '$argon2id$v=19$m=65536,t=3,p=4$5oIX8NY1s0/iqOrHH6Nlag$iwJFMpQwgY9iZqWErCDfpBJSKnX6rH1/iYkYa1KOmd0', 1, 0, 0, 0, 0,
            'What was the name of your first pet?', 'What was the make and model of your first car?', 'What is the name of your favorite childhood book?',
            '$argon2id$v=19$m=65536,t=3,p=4$JMNDlTyRqXmws2mpxMTFcg$yGhIIkq8LiJMI5LjnOMIvP3HsOqts1qmgBNnBC02Fiw',
            '$argon2id$v=19$m=65536,t=3,p=4$UG/Ew7+GgpO5iEr7ZeWuCw$SO23bV4/wQS9Xln4hKa0r6/CV3ctBjP6ZzJHcBYl11k',
            '$argon2id$v=19$m=65536,t=3,p=4$oc+PaL1B7uxMXbIiTAozIw$Dbtbs5sY50lyAWu9ITfOeLKt8bKDy+Ph8qsfPRsAxg0');


            -- vendor data

            INSERT OR IGNORE INTO vendors (vendor_id, user_id, vendor_name) VALUES
            (1, 1, 'Amazon'),
            (2, 1, 'Whole Foods Market'),
            (3, 1, 'Netflix'),
            (4, 1, 'PetSmart'),
            (5, 1, 'Chase Bank'),
            (6, 1, 'Fidelity Investments'),

            (7, 2, 'Amazon'),
            (8, 2, 'Whole Foods Market'),
            (9, 2, 'Netflix'),
            (10, 2, 'PetSmart'),
            (11, 2, 'Chase Bank'),
            (12, 2, 'Fidelity Investments'),

            (13, 3, 'Amazon'),
            (14, 3, 'Whole Foods Market'),
            (15, 3, 'Netflix'),
            (16, 3, 'PetSmart'),
            (17, 3, 'Chase Bank'),
            (18, 3, 'Fidelity Investments'),

            (19, 4, 'Amazon'),
            (20, 4, 'Whole Foods Market'),
            (21, 4, 'Netflix'),
            (22, 4, 'PetSmart'),
            (23, 4, 'Chase Bank'),
            (24, 4, 'Fidelity Investments'),

            (25, 5, 'Amazon'),
            (26, 5, 'Whole Foods Market'),
            (27, 5, 'Netflix'),
            (28, 5, 'PetSmart'),
            (29, 5, 'Chase Bank'),
            (30, 5, 'Fidelity Investments');

            -- Budget data
            INSERT OR IGNORE INTO budgets (user_id, budget_name, total_budgeted_amount, leftover_amount, start_date, end_date) VALUES
            (1, 'Budget-Test', 900.0, 900.0, '2025-04-14', '2025-04-30'),
            (2, 'Budget-Test', 900.0, 900.0, '2025-04-14', '2025-04-30'),
            (3, 'Budget-Test', 900.0, 900.0, '2025-04-14', '2025-04-30'),
            (4, 'Budget-Test', 900.0, 900.0, '2025-04-14', '2025-04-30'),
            (5, 'Budget-Test', 900.0, 900.0, '2025-04-14', '2025-04-30');


            -- Budget Accounts data
            INSERT OR IGNORE INTO budget_accounts (
            budget_accounts_id, user_id, budget_id, account_name,
            total_allocated_amount, current_amount, savings_goal,
            created_at, updated_at, notes
            )
            VALUES
            (1, 1, 1, 'Rent', 100.0, 100.0, 0.0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'Rent'),
            (2, 1, 1, 'Food', 100.0, 100.0, 0.0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'Food'),
            (3, 1, 1, 'Entertainment', 20.0, 20.0, 0.0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'Entertainment'),
            (4, 1, 1, 'Pets', 200.0, 200.0, 0.0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'Pets'),
            (5, 1, 1, 'Savings', 380.0, 380.0, 0.0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'Savings'),
            (6, 1, 1, 'Stocks', 100.0, 100.0, 0.0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'Stocks.'),

            (7, 2, 1, 'Rent', 120.0, 120.0, 0.0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'Rent'),
            (8, 2, 1, 'Food', 150.0, 150.0, 0.0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'Food'),
            (9, 2, 1, 'Entertainment', 30.0, 30.0, 0.0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'Entertainment'),
            (10, 2, 1, 'Pets', 180.0, 180.0, 0.0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'Pets'),
            (11, 2, 1, 'Savings', 400.0, 400.0, 0.0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'Savings'),
            (12, 2, 1, 'Stocks', 90.0, 90.0, 0.0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'Stocks.'),

            (13, 3, 1, 'Rent', 130.0, 130.0, 0.0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'Rent'),
            (14, 3, 1, 'Food', 110.0, 110.0, 0.0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'Food'),
            (15, 3, 1, 'Entertainment', 25.0, 25.0, 0.0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'Entertainment'),
            (16, 3, 1, 'Pets', 160.0, 160.0, 0.0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'Pets'),
            (17, 3, 1, 'Savings', 350.0, 350.0, 0.0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'Savings'),
            (18, 3, 1, 'Stocks', 110.0, 110.0, 0.0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'Stocks.'),

            (19, 4, 1, 'Rent', 140.0, 140.0, 0.0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'Rent'),
            (20, 4, 1, 'Food', 130.0, 130.0, 0.0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'Food'),
            (21, 4, 1, 'Entertainment', 22.0, 22.0, 0.0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'Entertainment'),
            (22, 4, 1, 'Pets', 210.0, 210.0, 0.0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'Pets'),
            (23, 4, 1, 'Savings', 370.0, 370.0, 0.0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'Savings'),
            (24, 4, 1, 'Stocks', 95.0, 95.0, 0.0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'Stocks.'),

            (25, 5, 1, 'Rent', 110.0, 110.0, 0.0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'Rent'),
            (26, 5, 1, 'Food', 140.0, 140.0, 0.0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'Food'),
            (27, 5, 1, 'Entertainment', 28.0, 28.0, 0.0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'Entertainment'),
            (28, 5, 1, 'Pets', 190.0, 190.0, 0.0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'Pets'),
            (29, 5, 1, 'Savings', 360.0, 360.0, 0.0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'Savings'),
            (30, 5, 1, 'Stocks', 105.0, 105.0, 0.0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'Stocks.');


            -- transaction data
            INSERT OR IGNORE INTO transactions (
                transaction_id, user_id, budget_accounts_id, vendor_id,
                amount, transaction_date, description, recurring, status
            )
            VALUES
            (1, 1, 1, 1, 50.67, '2025-04-14 13:22:32', 'Rent', 0,0),
            (2, 1, 2, 1, 79.0, '2025-04-14 13:22:32', 'Food', 0,0),
            (3, 1, 3, 1, 10.0, '2025-04-14 13:22:32', 'Netflix', 0,0),
            (4, 1, 4, 1, 140.0, '2025-04-14 13:22:32', 'Pets', 0,0),
            (5, 1, 5, 1, 320.0, '2025-04-14 13:22:32', 'Savings', 1,0),
            (6, 1, 6, 1, 80.0, '2025-04-14 13:22:32', 'Investment', 1,0),

            (7, 2, 7, 1, 50.67, '2025-04-14 13:22:32', 'Rent', 0,0),
            (8, 2, 8, 1, 79.0, '2025-04-14 13:22:32', 'Food', 0,0),
            (9, 2, 9, 1, 10.0, '2025-04-14 13:22:32', 'Netflix', 0,0),
            (10, 2, 10, 1, 140.0, '2025-04-14 13:22:32', 'Pets', 0,0),
            (11, 2, 11, 1, 320.0, '2025-04-14 13:22:32', 'Savings', 1,0),
            (12, 2, 12, 1, 80.0, '2025-04-14 13:22:32', 'Investment', 1,0),

            (13, 3, 13, 1, 50.67, '2025-04-14 13:22:32', 'Rent', 0,0),
            (14, 3, 14, 1, 79.0, '2025-04-14 13:22:32', 'Food', 0,0),
            (15, 3, 15, 1, 10.0, '2025-04-14 13:22:32', 'Netflix', 0,0),
            (16, 3, 16, 1, 140.0, '2025-04-14 13:22:32', 'Pets', 0,0),
            (17, 3, 17, 1, 320.0, '2025-04-14 13:22:32', 'Savings', 1,0),
            (18, 3, 18, 1, 80.0, '2025-04-14 13:22:32', 'Investment', 1,0),

            (19, 4, 19, 1, 50.67, '2025-04-14 13:22:32', 'Rent', 0,0),
            (20, 4, 20, 1, 79.0, '2025-04-14 13:22:32', 'Food', 0,0),
            (21, 4, 21, 1, 10.0, '2025-04-14 13:22:32', 'Netflix', 0,0),
            (22, 4, 22, 1, 140.0, '2025-04-14 13:22:32', 'Pets', 0,0),
            (23, 4, 23, 1, 320.0, '2025-04-14 13:22:32', 'Savings', 1,0),
            (24, 4, 24, 1, 80.0, '2025-04-14 13:22:32', 'Investment', 1,0),

            (25, 5, 25, 1, 50.67, '2025-04-14 13:22:32', 'Rent', 0,0),
            (26, 5, 26, 1, 79.0, '2025-04-14 13:22:32', 'Food', 0,0),
            (27, 5, 27, 1, 10.0, '2025-04-14 13:22:32', 'Netflix', 0,0),
            (28, 5, 28, 1, 140.0, '2025-04-14 13:22:32', 'Pets', 0,0),
            (29, 5, 29, 1, 320.0, '2025-04-14 13:22:32', 'Savings', 1,0),
            (30, 5, 30, 1, 80.0, '2025-04-14 13:22:32', 'Investment', 1,0);

        """
        try:
            # Execute the SQL script to create all tables
            cursor.executescript(sql_script)
            conn.commit()  # Commit the changes to the database
            print("All data added successfully!")  
        except Exception as e:
            # Handle errors during table creation
            print("Error inserting dummy data:", e)
        finally:
            cursor.close()  # Ensure the cursor is closed after execution
    except:
        print("failed to connected and work")

def main():
    fake_data()

if __name__ == "__main__":
    sys.exit(main())
