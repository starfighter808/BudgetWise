# this code is assuming there is a connection to the database already, if this is not true please reconfigure
import sqlite3 as s3
import string as str
from database import Database #This line imports the Database class to give us access to Database functions


# An important note to make when reviewing this code is to recognize that database variables have under_scores and local python variables do not
class Vendor:
    
    #inherit connection object from the database class
    def __init__(self, conn: Database):
        self.conn = conn

    # this function accepts two string inputs to create a vendor in the database
    def createVendor(userID, vName, vDesc):
        try:
            query = """INSERT INTO vendor (user_id,vendor_name,vendor_description,vendor_usage_ranking) VALUES (?, ?, ?, ?)"""
            self.conn.execute(query,(userID, vName, vDesc, 3))  # this line is done this way to prevent SQL injection attacks and predefines vendor_usage_ranking as 3 (out of five?)
            # if sqlite3 throws, print error to screen.
        except s3.Error as e:
            print(f"An error occurred in createVendor: {e}")

    # this function accepts a userid to locate all vendors in the database pertaining to one user and returns the list of vendor_id's.
    def getVendorsByUserID(userID):
        try:
            query = """SELECT vendor_id FROM vendor WHERE user_id = ?"""
            self.conn.fetchall(query, (userID))  # this line is done this way to prevent SQL injection attacks
        # if sqlite3 throws, print error to screen.
        except s3.Error as e:
            print(f"An error occurred in getVendorByUserID: {e}")
    
    # def getVendorByUsername():
    # more description required

    def updateVendor(vendorID, vName, vDesc, vendorUR):
        try:
            query = """UPDATE vendor SET vendor_name = ?, vendor_description = ?, vendor_usage_ranking = ? WHERE vendor_id = ?"""
            self.conn.execute(query, (vName, vDesc, vendorUR, vendorID))
        # if sqlite3 throws, print error to screen.
        except s3.Error as e:
            print(f"An error occurred in updateVendor: {e}")

    def deleteVendor(vendorID):
        try:
            query = """DELETE FROM vendor WHERE vendor_id = ?"""
            self.conn.execute(query,(vendorID))  # this line is done this way to prevent SQL injection attacks
        # if sqlite3 throws, print error to screen.
        except s3.Error as e:
            print(f"An error occurred in deleteVendor: {e}")

    def getVendorDescription(vendorID):
        try:
            query = """SELECT vendor_description FROM vendor WHERE vendor_id = ?"""
            return self.conn.fetchone(query,(vendorID))  # this line is done this way to prevent SQL injection attacks
        # if sqlite3 throws, print error to screen.
        except s3.Error as e:
            print(f"An error occurred in getVendorDescription: {e}")

    def setVendorDescription(vendorID, vDesc):
        try:
            query = """UPDATE vendor SET vendor_description = ? WHERE vendor_id = ?"""
            self.conn.execute(query, (vDesc, vendorID))  # this line is done this way to prevent SQL injection attacks
        # if sqlite3 throws, print error to screen.
        except s3.Error as e:
            print(f"An error occurred in setVendorDescription: {e}")

    def getVendorUsageRanking(vendorID):
        try:
            query = """SELECT vendor_usage_ranking FROM vendor WHERE vendor_id = ?"""
            self.conn.fetchone(query, (vendorID))  # this line is done this way to prevent SQL injection attacks
        # if sqlite3 throws, print error to screen.
        except s3.Error as e:
            print(f"An error occurred in getVendorUsageRanking: {e}")

    def setVendorUsageRanking(vendorID, vendorUR):
        try:
            query = """UPDATE vendor SET vendor_usage_ranking = ? WHERE vendor_id = ?"""
            self.conn.execute(query, (vendorUR, vendorID))  # this line is done this way to prevent SQL injection attacks
        # if sqlite3 throws, print error to screen.
        except s3.Error as e:
            print(f"An error occurred in setVendorUsageRanking: {e}")

    def setVendorName(vendorID, vName):
        try:
            # this query should change a vendor's name in the databse accoring to their vendor_id
            query = """UPDATE vendor SET vendor_name = ? WHERE vendor_id = ?"""
            self.conn.execute(query, (vName, vendorID))  # this line is done this way to prevent SQL injection attacks
        # if sqlite3 throws, print error to screen.
        except s3.Error as e:
            print(f"An error occurred in setVendorName: {e}")

    def getVendorName(vendorID):
        try:
            # this query will return the vendor_name related to the specific vendorID
            query = """SELECT vendor_name FROM vendor WHERE vendor_id = ?"""
            self.conn.fetchone(query,(vendorID))  # this line is done this way to prevent SQL injection attacks
        # if sqlite3 throws, print error to screen.
        except s3.Error as e:
            print(f"An error occurred in getVendorName: {e}")
