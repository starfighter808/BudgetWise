Classes:
* User
* Audit Logs
* Reports

User:

createUserAccount(username, password):
	username
	password_hash
	created_at		// this might be handled automatically

validateUser():			// use before login
	// checks if user login information is correct

login():
	username
	password_hash

updatePassword():
	password_hash
	updated_at		// this might be handled automatically

getUserID():
	user_id

setTheme():
	theme

setNotificationsEnabled():
	notifications_enabled

* editPreferences():		// not MVP
	default_chart_type	
	language		
	
* checkIfUsernameExists():	// used during account creation
	// this function should compare the input username against
	// the database to ensure it is unique

* checkIfValidInput():		// used for account creation/login
	// this function exists to protect against SQL attacks
	// might not be needed; depends on how SQLite works
	

Audit Log:			// not sure if this will get used

createAuditLog():
	log_id			// handled automatically
	user_id
	action_type
	transaction_id
	related_table
	record_id
	timestamp		// might be handled automatically

getAuditLog():
	log_id
	action_type
	related_table
	timestamp

setActionType():
	action_type

Report:

createReport():
	report_id		// handled automatically
	user_id
	report_type
	report_date		// might be handled automatically
	report_data		// json type might not be supported by SQLite
	report_frequency

getReport(user_id):		// pulls all reports for specified user_id
	report_id
	report_type
	report_date
	report_data
	report_frequency

displayReports():		// displays list of reports for user to choose

updateReportType():
	report_type

updateReportFrequency():
	report_frequency
