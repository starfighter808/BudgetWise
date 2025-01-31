from installation import Installation

def main():
    installer = Installation()

    #Comment out the install sesciont once it is installed successfully


    # install dependencies and database
    installer.check_os()
    installer.check_python()
    installer.check_library_status()
    installer.create_encrypted_database()


    # Edit the Database/ work with it
    #installer.edit_db



if __name__ == "main":
    main()
