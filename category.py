import sqlite3 as s3
import string as str


#i am going to assume we open a connection using some kind of connection name like 'conn'
#if this is incorrect feel free to ctrl + f and change my instances of conn.object() to something else

#######################################
#IMPLIED CODE LINE
# conn = s3.connect('budgetwise.db')
#######################################


#An important note to make when reviewing this code is to recognize that database variables have under_scores and local python variables do not

#this function creates a category in the category table
def createCategory(catName, catDesc):
    try:
        # establish cursor object
        cursor = conn.cursor()

        # aquire cached data from user class (in progress)
        # userID = getUserID()

        cursor.execute(
            """
               INSERT INTO categories (user_id ,category_name ,category_description ,category_usage_ranking) VALUES (?, ?, ?, ?)
               """,
            (userID, catName, catDesc, 3)  # this line is done this way to prevent SQL injection attacks and predefines category_usage_ranking as 3 (out of five?)
        )
        conn.commit()

    # if sqlite3 throws, print error to screen.
    except s3.Error as e:
        print(f"An error occurred in createCategory: {e}")
        conn.rollback()

    # regardless of what happens above we want to close the cursor
    finally:
        if cursor:
            cursor.close()
  
# this function accepts a userid to locate all categories in the database pertaining to one user and returns the list of category ID's.
def getCategoriesByUserID(userID): 

    try:
        # establish cursor object
        cursor = conn.cursor()

        # this query should return all categories that belong to a specific user id
        cursor.execute(
            """
               SELECT category_id FROM categories WHERE user_id = ?
               """,
            (userID)  # this line is done this way to prevent SQL injection attacks
        )
        categoryIDs = cursor.fetchall()
        return categoryIDs

    # if sqlite3 throws, print error to screen.
    except s3.Error as e:
        print(f"An error occurred in getCategoryByUserID: {e}")
        conn.rollback()

    # regardless of what happens above we want to close the cursor
    finally:
        if cursor:
            cursor.close()
  

#def getCategoryByUsername():
#more definition required

#this function accepts all attributes of something in the categories table in order to update it's entry in the database
def updateCategories(catID, catName, catDesc, catUR):
    try:
        # establish cursor object
        cursor = conn.cursor()

        # this query should update a single category's attributes in the cateogry table
        cursor.execute(
            """
               UPDATE categories SET category_name = ?, category_description = ?, category_usage_ranking = ? WHERE category_id = ?
               """,
            (catName, catDesc, catUR, catID)
        )
        conn.commit()

    # if sqlite3 throws, print error to screen.
    except s3.Error as e:
        print(f"An error occurred in updateCategories: {e}")
        conn.rollback()

    # regardless of what happens above we want to close the cursor
    finally:
        if cursor:
            cursor.close()
  

def deleteCategory(catID): 
    try:
        # establish cursor object
        cursor = conn.cursor()

        # this query should delete categories from the category table
        cursor.execute(
            """
               DELETE FROM categories WHERE category_id = ?
               """,
            (catID)  # this line is done this way to prevent SQL injection attacks
        )
        conn.commit()

    # if sqlite3 throws, print error to screen.
    except s3.Error as e:
        print(f"An error occurred in deleteCategory: {e}")
        conn.rollback()

    # regardless of what happens above we want to close the cursor
    finally:
        if cursor:
            cursor.close()

  

def getCategoryDescription(catID):
    try:
        # establish cursor object
        cursor = conn.cursor()

        # this query will return the description related to the specific category_id
        cursor.execute(
            """
                SELECT category_description FROM categories WHERE category_id = ?
               """,
            (catID)  # this line is done this way to prevent SQL injection attacks
        )
        catDesc = cursor.fetchone()
        return catDesc
    # if sqlite3 throws, print error to screen.
    except s3.Error as e:
        print(f"An error occurred in getCategoryDescription: {e}")
        conn.rollback()

    # regardless of what happens above we want to close the cursor
    finally:
        if cursor:
            cursor.close()
  

def setCategoryDescription(catDesc, catID):  
    try:
        # establish cursor object
        cursor = conn.cursor()

        # this query should set the category_description related to the specific categoryID
        cursor.execute(
            """
               UPDATE categories SET category_description = ? WHERE category_id = ?
               """,
            (catDesc, catID)  # this line is done this way to prevent SQL injection attacks
        )
        conn.commit()

    # if sqlite3 throws, print error to screen.
    except s3.Error as e:
        print(f"An error occurred in setCategoryDescription: {e}")
        conn.rollback()

    # regardless of what happens above we want to close the cursor
    finally:
        if cursor:
            cursor.close()

def getCategoryUsageRanking(catID):
    try:
        # establish cursor object
        cursor = conn.cursor()

        # this query will return the description related to the specific categoryID
        cursor.execute(
            """
                SELECT category_usage_ranking FROM categories WHERE category_id = ?
               """,
            (catID)  # this line is done this way to prevent SQL injection attacks
        )
        categoryUR = cursor.fetchone()
        return categoryUR
    # if sqlite3 throws, print error to screen.
    except s3.Error as e:
        print(f"An error occurred in getCategoryUsageRanking: {e}")
        conn.rollback()

    # regardless of what happens above we want to close the cursor
    finally:
        if cursor:
            cursor.close()

  

def setCategoryUsageRanking(catUR, catID):
    try:
        # establish cursor object
        cursor = conn.cursor()

        # this query should return all categories in the database that belong to a specific user_id
        cursor.execute(
            """
               UPDATE categories SET category_usage_ranking = ? WHERE category_id = ?
               """,
            (catUR, catID)  # this line is done this way to prevent SQL injection attacks
        )
        conn.commit()

    # if sqlite3 throws, print error to screen.
    except s3.Error as e:
        print(f"An error occurred in setCategoryUsageRanking: {e}")
        conn.rollback()

    # regardless of what happens above we want to close the cursor
    finally:
        if cursor:
            cursor.close()

def setCategoryName(catID, catName):
    try:
        # establish cursor object
        cursor = conn.cursor()

        # this query should set the category_name of a specific category with the same category_id
        cursor.execute(
            """
               UPDATE categories SET category_name = ? WHERE category_id = ?
               """,
            (catName, catID)  # this line is done this way to prevent SQL injection attacks
        )
        conn.commit()

    # if sqlite3 throws, print error to screen.
    except s3.Error as e:
        print(f"An error occurred in setCategoryName: {e}")
        conn.rollback()

    # regardless of what happens above we want to close the cursor
    finally:
        if cursor:
            cursor.close()

def getCategoryName(catID):
    try:
        # establish cursor object
        cursor = conn.cursor()

        # this query will return the category_name related to the specific category_id
        cursor.execute(
            """
                SELECT category_name FROM categories WHERE category_id = ?
               """,
            (catID)  # this line is done this way to prevent SQL injection attacks
        )
        catName = cursor.fetchone()
        return catName
    # if sqlite3 throws, print error to screen.
    except s3.Error as e:
        print(f"An error occurred in getCategoryName: {e}")
        conn.rollback()

    # regardless of what happens above we want to close the cursor
    finally:
        if cursor:
            cursor.close()

  



