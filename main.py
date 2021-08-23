import sys, os, sqlite3
from prettytable import PrettyTable
#os.system('cls' if os.name == 'nt' else 'clear')


def updateID():
	try:
		sqlite_conn = sqlite3.connect('base.db')
		cursor = sqlite_conn.cursor()

		cursor.execute("SELECT * FROM base;")
		all_data = cursor.fetchall()
	except sqlite3.Error as error: print("Error connecting to base")

	num = int(1)
	for i in all_data:
		cursor.execute(f'UPDATE base SET id_num = ? WHERE id_num = ?', (num, int(i[0])))
		sqlite_conn.commit()
		num += 1

	cursor.close()
	del all_data


def deleteDB():
	text = input("Are you sure you want to delete all database data? ? (y/n) --> ").rstrip()

	if text == "y":
		try:
			sqlite_conn = sqlite3.connect('base.db')
			cursor = sqlite_conn.cursor()

			cursor.execute("SELECT * FROM base;")
			all_data = cursor.fetchall()
		except sqlite3.Error as error: print("Error connecting to base")

		x = int(1)
		for i in all_data:
			cursor.execute("""DELETE FROM base WHERE id_num=?""", (x,))
			sqlite_conn.commit()
			x += 1

		cursor.close()
		del all_data
		print("Deletion completed successfully !")

	else:
		print("Deleting all data from the database canceled !\n")
		start()


def deleteData():
	try:
		sqlite_conn = sqlite3.connect('base.db')
		cursor = sqlite_conn.cursor()
	except sqlite3.Error as error: print("Error connecting to base")

	text = int(input("Write a row ID --> "))

	cursor.execute("""DELETE FROM base WHERE id_num=?""", (text,))
	sqlite_conn.commit()
	cursor.close()

	updateID()
	showData()


def cleanCLI():
	os.system('cls' if os.name == 'nt' else 'clear')


def add():
	app_name = input("Write a app name --> ").rstrip()
	email = input("Write a email --> ").rstrip()
	ph_num = input("Write a phone number --> ").rstrip()
	user = input("Write a user name --> ").rstrip()
	url = input("Write a URL --> ").rstrip()
	passw = input("Write a password --> ").rstrip()

	try:
		sqlite_conn = sqlite3.connect('base.db')
		cursor = sqlite_conn.cursor()
	except sqlite3.Error as error: print("Error connecting to base")

	cursor.execute("""CREATE TABLE IF NOT EXISTS base(
		id_num INTEGER,
  	app_name TEXT,
  	email TEXT,
  	ph_num TEXT,
  	user TEXT,
  	url TEXT,
  	passw TEXT);
	""")

	updateID()

	cursor.execute("SELECT * FROM base;")
	all_data = cursor.fetchall()
	id_num = len(all_data) + 1

	data = [(id_num, app_name, email, ph_num, user, url, passw)]
	cursor.executemany("INSERT INTO base VALUES(?, ?, ?, ?, ?, ?, ?);", data)
	
	sqlite_conn.commit()
	cursor.close()


def getData():
	try:
		sqlite_conn = sqlite3.connect('base.db')
		cursor = sqlite_conn.cursor()
	except sqlite3.Error as error: print("Error connecting to base")

	text = int(input("Write a row ID --> "))

	cursor.execute("""SELECT * FROM base WHERE id_num = ?""", (text,))
	data = cursor.fetchall()
	cursor.close()

	myTable = PrettyTable(["Paragraph", "Value"], header=False)
	myTable.align["Paragraph"] = "r"
	myTable.align["Value"] = "r"
	
	myTable.add_row(["App Name", data[0][1]])
	myTable.add_row(["Email", data[0][2]])
	myTable.add_row(["Phone Number", data[0][3]])
	myTable.add_row(["User", data[0][4]])
	myTable.add_row(["URL", data[0][5]])
	myTable.add_row(["Password", data[0][6]])

	print("\n")
	print(myTable.get_string(title="INFO"), "\n")
	del data


def editData():
	try:
		sqlite_conn = sqlite3.connect('base.db')
		cursor = sqlite_conn.cursor()
	except sqlite3.Error as error: print("Error connecting to base")

	showData()

	text = int(input("Write the row ID you want to edit --> "))
	cleanCLI()

	cursor.execute("""SELECT * FROM base WHERE id_num = ?""", (text,))
	data = cursor.fetchall()

	myTable = PrettyTable(["ID", "Paragraph", "Value"])
	myTable.align["ID"] = "r"
	myTable.align["Paragraph"] = "r"
	myTable.align["Value"] = "r"
	myTable.add_row(["1", "App Name", data[0][1]])
	myTable.add_row(["2", "Email", data[0][2]])
	myTable.add_row(["3", "Phone Number", data[0][3]])
	myTable.add_row(["4", "User", data[0][4]])
	myTable.add_row(["5", "URL", data[0][5]])
	myTable.add_row(["6", "Password", data[0][6]])

	print(myTable.get_string(title="ID List"), "\n")
	del data
	cursor.close()

	itemINT = int(input("Enter the ID of the item you want to edit. Example: 2 --> "))

	itemPRG = str("")
	if itemINT == 1: itemPRG = "app_name"
	elif itemINT == 2: itemPRG = "email"
	elif itemINT == 3: itemPRG = "ph_num"
	elif itemINT == 4: itemPRG = "user"
	elif itemINT == 5: itemPRG = "url"
	elif itemINT == 6: itemPRG = "passw"
	else:
		print("Wrong ID")
		return

	newValue = str(input(f"Enter a new value for the {itemPRG} item --> ")).rstrip()

	try:
		sqlite_conn = sqlite3.connect('base.db')
		cursor = sqlite_conn.cursor()

		cursor.execute(f'UPDATE base SET {itemPRG} = ? WHERE id_num = ?', (newValue, text))
		sqlite_conn.commit()
		cursor.close()

		print(f"{itemPRG} clause edited successfully !\n")

	except sqlite3.Error as error: 
		print("Error connecting to base\n")
		return


def showData():
	try:
		sqlite_conn = sqlite3.connect('base.db')
		cursor = sqlite_conn.cursor()

		cursor.execute("SELECT * FROM base;")
		all_data = cursor.fetchall()
	except sqlite3.Error as error: 
		print("Error connecting to base\n")
		return

	cursor.close()

	myTable = PrettyTable(["ID", "App Name", "Email", "Phone Number", "User", "URL", "Password"])
	myTable.align["ID"] = "l"
	myTable.align["App Name"] = "r"
	myTable.align["Email"] = "r"
	myTable.align["Phone Number"] = "r"
	myTable.align["User"] = "r"
	myTable.align["URL"] = "r"
	myTable.align["Password"] = "r"
	
	for i in all_data: myTable.add_row([i[0], i[1], i[2], i[3], i[4], i[5], i[6]])
	print("\n")
	print(myTable.get_string(title="Password Manager"), "\n")
	del all_data


def start():
	text = str(input("Write a command. Example: #help --> ")).rstrip()

	if text == "#exit": sys.exit()
	elif text == "#add": add()
	elif text == "#get": getData()
	elif text == "#edit": editData()
	elif text == "#delete": deleteData()
	elif text == "#delete_database": deleteDB()
	elif text == "#clean": cleanCLI()
	elif text == "#show": showData()
	elif text == "#help":
		print("\nCommands:")
		print("  #help - Shows a list of commands")
		print("  #add - Add a element in a data base")
		print("  #get - Get data from database")
		print("  #edit - Editing cells")
		print("  #show - View data")
		print("  #delete - Deletes data from the database")
		print("  #delete_database - Deleting all data from the database")
		print("  #clean - Cleaning the console")
		print("  #exit - Exit the programm\n")
		
	start()

start()