# this code is assuming there is a connection to the database already, if this is not true please reconfigure
import sqlite3 as s3
import string as str


# i am going to assume we open a connection using some kind of connection name like 'conn'
# if this is incorrect feel free to ctrl + f and change my instances of conn.object() to something else

#######################################
# IMPLIED CODE LINE
# conn = s3.connect('budgetwise.db')
#######################################


# An important note to make when reviewing this code is to recognize that database variables have under_scores and local python variables do not


# this function accepts two string inputs to create a vendor in the database
def createVendor(vName, vDesc):
    try:
        # establish cursor object
        cursor = conn.cursor()

        # aquire cached data from user class (in progress)
        # userID = getUserID()

        cursor.execute(
            """
               INSERT INTO vendor (user_id,vendor_name,vendor_description,vendor_usage_ranking) VALUES (?, ?, ?, ?)
               """,
            (userID, vName, vDesc, 3)  # this line is done this way to prevent SQL injection attacks and predefines vendor_usage_ranking as 3 (out of five?)
        )
        conn.commit()

    # if sqlite3 throws, print error to screen.
    except s3.Error as e:
        print(f"An error occurred in createVendor: {e}")
        conn.rollback()

    # regardless of what happens above we want to close the cursor
    finally:
        if cursor:
            cursor.close()


# this function accepts a userid to locate all vendors in the database pertaining to one user and returns the list of vendors as tuples.
# Tuple format (???)
def getVendorsByUserID(userID):
    try:
        # establish cursor object
        cursor = conn.cursor()

        # this query should return all vendors in the database that belong to a specific user_id
        cursor.execute(
            """
               SELECT vendor_id FROM vendor WHERE user_id = ?
               """,
            (userID)  # this line is done this way to prevent SQL injection attacks
        )
        vendorID = cursor.fetchall()
        return vendorID

    # if sqlite3 throws, print error to screen.
    except s3.Error as e:
        print(f"An error occurred in getVendorByUserID: {e}")
        conn.rollback()

    # regardless of what happens above we want to close the cursor
    finally:
        if cursor:
            cursor.close()


# def getVendorByUsername():
# more description required


def updateVendor(vendorID, vName, vDesc, vendorUR):
    try:
        # establish cursor object
        cursor = conn.cursor()

        # this query should return all vendors in the database that belong to a specific user_id
        cursor.execute(
            """
               UPDATE vendor SET vendor_name = ?, vendor_description = ?, vendor_usage_ranking = ? WHERE vendor_id = ?
               """,
            (vName, vDesc, vendorUR, vendorID)
        )
        conn.commit()

    # if sqlite3 throws, print error to screen.
    except s3.Error as e:
        print(f"An error occurred in updateVendor: {e}")
        conn.rollback()

    # regardless of what happens above we want to close the cursor
    finally:
        if cursor:
            cursor.close()


def deleteVendor(vendorID):
    try:
        # establish cursor object
        cursor = conn.cursor()

        # this query should delete vendors from the vendor table
        cursor.execute(
            """
               DELETE FROM vendor WHERE vendor_id = ?
               """,
            (vendorID)  # this line is done this way to prevent SQL injection attacks
        )
        conn.commit()

    # if sqlite3 throws, print error to screen.
    except s3.Error as e:
        print(f"An error occurred in deleteVendor: {e}")
        conn.rollback()

    # regardless of what happens above we want to close the cursor
    finally:
        if cursor:
            cursor.close()


def getVendorDescription(vendorID):
    try:
        # establish cursor object
        cursor = conn.cursor()

        # this query will return the description related to the specific vendorID
        cursor.execute(
            """
                SELECT vendor_description FROM vendor WHERE vendor_id = ?
               """,
            (vendorID)  # this line is done this way to prevent SQL injection attacks
        )
        vDesc = cursor.fetchone()
        return vDesc
    # if sqlite3 throws, print error to screen.
    except s3.Error as e:
        print(f"An error occurred in getVendorDescription: {e}")
        conn.rollback()

    # regardless of what happens above we want to close the cursor
    finally:
        if cursor:
            cursor.close()


def setVendorDescription(vendorID, vDesc):
    try:
        # establish cursor object
        cursor = conn.cursor()

        # this query should change a vendor's description based on their vendor_id
        cursor.execute(
            """
               UPDATE vendor SET vendor_description = ? WHERE vendor_id = ?
               """,
            (vDesc, vendorID)  # this line is done this way to prevent SQL injection attacks
        )
        conn.commit()

    # if sqlite3 throws, print error to screen.
    except s3.Error as e:
        print(f"An error occurred in setVendorDescription: {e}")
        conn.rollback()

    # regardless of what happens above we want to close the cursor
    finally:
        if cursor:
            cursor.close()


def getVendorUsageRanking(vendorID):
    try:
        # establish cursor object
        cursor = conn.cursor()

        # this query will return the vendor_usage_ranking related to the specific vendor_id
        cursor.execute(
            """
                SELECT vendor_usage_ranking FROM vendor WHERE vendor_id = ?
               """,
            (vendorID)  # this line is done this way to prevent SQL injection attacks
        )
        vendorUR = cursor.fetchone()
        return vendorUR
    # if sqlite3 throws, print error to screen.
    except s3.Error as e:
        print(f"An error occurred in getVendorUsageRanking: {e}")
        conn.rollback()

    # regardless of what happens above we want to close the cursor
    finally:
        if cursor:
            cursor.close()


def setVendorUsageRanking(vendorID, vendorUR):
    try:
        # establish cursor object
        cursor = conn.cursor()

        # this query should change the vendor_usage_ranking that belong to a specific user_id
        cursor.execute(
            """
               UPDATE vendor SET vendor_usage_ranking = ? WHERE vendor_id = ?
               """,
            (vendorUR, vendorID)  # this line is done this way to prevent SQL injection attacks
        )
        conn.commit()

    # if sqlite3 throws, print error to screen.
    except s3.Error as e:
        print(f"An error occurred in setVendorUsageRanking: {e}")
        conn.rollback()

    # regardless of what happens above we want to close the cursor
    finally:
        if cursor:
            cursor.close()


def setVendorName(vendorID, vName):
    try:
        # establish cursor object
        cursor = conn.cursor()

        # this query should change a vendor's name in the databse accoring to their vendor_id
        cursor.execute(
            """
               UPDATE vendor SET vendor_name = ? WHERE vendor_id = ?
               """,
            (vName, vendorID)  # this line is done this way to prevent SQL injection attacks
        )
        conn.commit()

    # if sqlite3 throws, print error to screen.
    except s3.Error as e:
        print(f"An error occurred in setVendorName: {e}")
        conn.rollback()

    # regardless of what happens above we want to close the cursor
    finally:
        if cursor:
            cursor.close()

def getVendorName(vendorID):
    try:
        # establish cursor object
        cursor = conn.cursor()

        # this query will return the vendor_name related to the specific vendorID
        cursor.execute(
            """
                SELECT vendor_name FROM vendor WHERE vendor_id = ?
               """,
            (vendorID)  # this line is done this way to prevent SQL injection attacks
        )
        vName = cursor.fetchone()
        return vName
    # if sqlite3 throws, print error to screen.
    except s3.Error as e:
        print(f"An error occurred in getVendorName: {e}")
        conn.rollback()

    # regardless of what happens above we want to close the cursor
    finally:
        if cursor:
            cursor.close()




