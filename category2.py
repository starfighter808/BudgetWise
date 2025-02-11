import sqlite3 as s3
import string as str
from database import Database #This line imports the Database class to give us access to Database functions


#An important note to make when reviewing this code is to recognize that database variables have under_scores and local python variables do not
class Category:

    #inherit connection object from the database class
    def __init__(self, conn: Database):
        self.conn = conn

    #this function creates a category in the category table
    def createCategory(userID, catName, catDesc):
        try:
            #this query creates an entry in the category table
            query = """INSERT INTO categories (user_id,  category_name, category_description, category_usage_ranking) VALUES (?, ?, ?, ?)"""
            self.conn.execute(query, (userID, catName, catDesc, 3)) # this line is done this way to prevent SQL injection attacks and predefines category_usage_ranking as 3 (out of five?)
        # if sqlite3 throws, print error to screen.
        except s3.Error as e:
            print(f"An error occurred in createCategory: {e}")
  
# this function accepts a userid to locate all categories in the database pertaining to one user and returns the list of category ID's.
    def getCategoriesByUserID(userID): 
        try:
        # this query should return all categories that belong to a specific user id
            query = """SELECT category_id FROM categories WHERE user_id = ?"""
            return self.conn.fetchall(query, (userID))  # this line is done this way to prevent SQL injection attacks
        # if sqlite3 throws, print error to screen.
        except s3.Error as e:
            print(f"An error occurred in getCategoryByUserID: {e}")
  

#def getCategoryByUsername():
#more definition required

#this function accepts all attributes of something in the categories table in order to update it's entry in the database
    def updateCategories(catID, catName, catDesc, catUR):
        try:
        # this query should update a single category's attributes in the cateogry table
            query = """UPDATE categories SET category_name = ?, category_description = ?, category_usage_ranking = ? WHERE category_id = ?"""
            self.conn.execute(query, (catName, catDesc, catUR, catID))
        # if sqlite3 throws, print error to screen.
        except s3.Error as e:
            print(f"An error occurred in updateCategories: {e}")
    
    def deleteCategory(catID): 
        try:
        # this query should delete categories from the category table
            query = """DELETE FROM categories WHERE category_id = ?"""
            self.conn.execute(query, (catID))  # this line is done this way to prevent SQL injection attacks
        # if sqlite3 throws, print error to screen.
        except s3.Error as e:
            print(f"An error occurred in deleteCategory: {e}")

    def getCategoryDescription(catID):
        try:
        # this query will return the description related to the specific category_id
            query = """SELECT category_description FROM categories WHERE category_id = ?"""
            return self.conn.fetchone(query, (catID))  # this line is done this way to prevent SQL injection attacks
    # if sqlite3 throws, print error to screen.
        except s3.Error as e:
            print(f"An error occurred in getCategoryDescription: {e}")

    def setCategoryDescription(catDesc, catID):  
        try:
            query = """UPDATE categories SET category_description = ? WHERE category_id = ?"""
            self.conn.execute(query, (catDesc, catID))  # this line is done this way to prevent SQL injection attacks
    # if sqlite3 throws, print error to screen.
        except s3.Error as e:
                print(f"An error occurred in setCategoryDescription: {e}")

    def getCategoryUsageRanking(catID):
        try:
        # this query will return the description related to the specific categoryID
            query = """SELECT category_usage_ranking FROM categories WHERE category_id = ?"""
            return self.conn.fetchone(query, (catID))  # this line is done this way to prevent SQL injection attacks
        # if sqlite3 throws, print error to screen.
        except s3.Error as e:
            print(f"An error occurred in getCategoryUsageRanking: {e}")

    def setCategoryUsageRanking(catUR, catID):
        try:
        # this query should set the category_usage_ranking of a specific category with the same category_id
            query = """UPDATE categories SET category_usage_ranking = ? WHERE category_id = ?"""
            self.conn.execute(query, (catUR, catID))  # this line is done this way to prevent SQL injection attacks
        # if sqlite3 throws, print error to screen.
        except s3.Error as e:
            print(f"An error occurred in setCategoryUsageRanking: {e}")

    def setCategoryName(catID, catName):
        try:
        # this query should set the category_name of a specific category with the same category_id
            query = """UPDATE categories SET category_name = ? WHERE category_id = ?"""
            self.conn.execute(query,(catName, catID))  # this line is done this way to prevent SQL injection attacks    
        # if sqlite3 throws, print error to screen.
        except s3.Error as e:
            print(f"An error occurred in setCategoryName: {e}")

    def getCategoryName(catID):
        try:
        # this query will return the category_name related to the specific category_id
            query = """SELECT category_name FROM categories WHERE category_id = ?"""
            return self.conn.fetchone(query, (catID))  # this line is done this way to prevent SQL injection attacks
        # if sqlite3 throws, print error to screen.
        except s3.Error as e:
            print(f"An error occurred in getCategoryName: {e}")

  



