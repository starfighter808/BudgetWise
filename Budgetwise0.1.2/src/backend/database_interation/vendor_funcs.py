import sqlcipher3

class Vendor:
    """
    Class to manage vendor-related database operations for a user.
    """

    def __init__(self, db_instance):
        """
        Initializes the Vendor object with an active database connection.
        
        Args:
            db (Database): An instance of the Database class (singleton).
        """
        self.db = db_instance

    def create_vendor(self, user_id, name):
        """
        Inserts a new vendor into the database.

        Args:
            user_id (int): The user ID who owns this vendor.
            name (str): The name of the vendor.
        """
        try:
            query = """INSERT INTO vendors (user_id, vendor_name)
                       VALUES (?, ?)"""
            self.db.cursor().execute(query, (user_id, name))
            self.db.commit_db()
        except sqlcipher3.Error as e:
            print(f"[create_vendor] SQLCipher Error: {e}")

    def get_vendors_by_user_id(self, user_id):
        """
        Retrieves all vendor IDs and names for a specific user.

        Args:
            user_id (int): The user ID.

        Returns:
            list of tuples: A list of (vendor_id, vendor_name) tuples.
        """
        try:
            query = "SELECT vendor_id, vendor_name FROM vendors WHERE user_id = ?"
            return self.db.cursor().execute(query, (user_id,)).fetchall()
        except sqlcipher3.Error as e:
            print(f"[get_vendors_by_user_id] SQLCipher Error: {e}")
            return []

    def update_vendor(self, vendor_id, name):
        """
        Updates vendor details.

        Args:
            vendor_id (int): The vendor ID to update.
            name (str): New name.
        """
        try:
            query = """UPDATE vendors 
                       SET vendor_name = ?
                       WHERE vendor_id = ?"""
            self.db.cursor().execute(query, (name, vendor_id))
            self.db.commit_db()
        except sqlcipher3.Error as e:
            print(f"[update_vendor] SQLCipher Error: {e}")

    def delete_vendor(self, vendor_id):
        """
        Deletes a vendor.

        Args:
            vendor_id (int): Vendor to delete.
        """
        try:
            query = "DELETE FROM vendors WHERE vendor_id = ?"
            self.db.cursor().execute(query, (vendor_id,))
            self.db.commit_db()
        except sqlcipher3.Error as e:
            print(f"[delete_vendor] SQLCipher Error: {e}")

    def get_vendor_name(self, vendor_id):
        """
        Retrieves the name of a vendor.

        Args:
            vendor_id (int): Vendor ID.

        Returns:
            str: Vendor name or None.
        """
        try:
            query = "SELECT vendor_name FROM vendors WHERE vendor_id = ?"
            result = self.db.cursor().execute(query, (vendor_id,)).fetchone()
            return result[0] if result else None
        except sqlcipher3.Error as e:
            print(f"[get_vendor_name] SQLCipher Error: {e}")
            return None

    def get_vendor_details(self, vendor_id):
        """
        Retrieves full details of a vendor (name, etc.).

        Args:
            vendor_id (int): Vendor ID.

        Returns:
            tuple: (vendor_id, vendor_name) or None if not found.
        """
        try:
            query = "SELECT vendor_id, vendor_name FROM vendors WHERE vendor_id = ?"
            result = self.db.cursor().execute(query, (vendor_id,)).fetchone()
            return result if result else None
        except sqlcipher3.Error as e:
            print(f"[get_vendor_details] SQLCipher Error: {e}")
            return None

    def get_all_vendors(self, user_id):
            try:
                # Debugging: Ensure the connection is valid
                if self.db is None:
                    return []

                query = "SELECT vendor_id, vendor_name FROM vendors where user_id = ?"
                cursor = self.db.cursor()
                
                # Debugging: Check if cursor is created successfully
                if cursor is None:
                    return []

                vendors = cursor.execute(query, (user_id,)).fetchall()

                # Debugging: Output the fetched vendors
                return vendors
                
            except sqlcipher3.Error as e:
                print(f"[get_all_vendors] SQLCipher Error: {e}")
                return []

