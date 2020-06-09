import sys

from flask import Flask, render_template, request, redirect, Response
from flask_mysqldb import MySQL
import random, json

app = Flask(__name__)

# Parameters for Godaddy MYSQL
# app.config['MYSQL_HOST'] = '198.12.249.203'
# app.config['MYSQL_USER'] = 'group5_sebastian'
# app.config['MYSQL_PASSWORD'] = 'Cammie23324$'
# app.config['MYSQL_DB'] = 'group5_remoteTest'


# Parameters for LocalHost connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root1234'
app.config['MYSQL_DB'] = 'MyDB'

# #Parameters for pythonanywhere connection
# app.config['MYSQL_HOST'] = 'contactology.mysql.pythonanywhere-services.com'
# app.config['MYSQL_USER'] = 'contactology'
# app.config['MYSQL_PASSWORD'] = 'root1234'
# app.config['MYSQL_DB'] = 'contactology$MyDB'

# Start connection with MySQL
mysql = MySQL(app)

# This is the first thing that main calls, it just renders our index.html file. (Scroll all the way down for main.)
@app.route('/')
def output():
	# serve index template
	return render_template('index.html')


# Ajax syntax for receiving post call from javascript
@app.route('/login', methods = ['POST'])
def test():
	# Here we are just checking if the request is POST
	if request.method == "POST":
		# We are getting the JSON sent from javascript, JSON is the only thing we can use to communicate
		# between JS and Python
		data = request.get_json(force = True)
		data = json.loads(data)
		# We are creating two new variables, username and userpass, and assigning them to the name and pass
		# variables from the JSON we just retrieved
		username = data['name']
		userpass = data['pass']

		# We are opening a connection curson for the api call to MySQL
		cur = mysql.connection.cursor()

		# The code in the parenthesis is how we ask MySQL to return the data, we pass it the data
		result = cur.execute("SELECT * FROM Users WHERE username = %s AND userpass = %s",(username ,userpass))

		# We are checking if the result is less than 1, this means they don't match or they dont exist.
		if (result < 1):
			return "Username password dont match."

		else:
			return "Username password match."

		# We are commiting and closing the connection to MySQL
		mysql.connection.commit()
		cur.close()

		#Thats it! A fuction that check to see if an account exists and/or the login information is correct.


@app.route('/register', methods = ['POST'])
def test2():
	if request.method == "POST":
		data = request.get_json(force = True)
		data = json.loads(data)
		username = data['name']
		userpass = data['pass']
		firstname = data['firstname']
		lastname = data['lastname']
		cur = mysql.connection.cursor()
		result = cur.execute("SELECT * FROM Users WHERE username = %s",(username,))

		if (result < 1):
			cur.execute("INSERT INTO Users(username, userpass,firstname,lastname) VALUES (%s, %s,%s,%s)", (username, userpass,firstname,lastname))
			mysql.connection.commit()
			cur.close()
			print "created"
			return "Account created."


		else:
			mysql.connection.commit()
			cur.close()
			print "not created."
			return "Found."




@app.route('/getUserid', methods = ['POST'])
def test3():
	if request.method == "POST":
		data = request.get_json(force = True)
		username = data['name']
		cur = mysql.connection.cursor()
		result = cur.execute("SELECT Userid FROM Users WHERE username = %s",(username ,))
		getall = cur.fetchone();
		mysql.connection.commit()
		cur.close()
		return str(getall[0])

@app.route('/getContacts', methods = ['POST'])
def test4():
	if request.method == "POST":
		data = request.get_json(force = True)
		userid = data['Userid']
		cur = mysql.connection.cursor()
		result = cur.execute("SELECT * FROM Contacts WHERE Userid = %s ORDER BY Name",(userid ,))
		getall = cur.fetchall();
		mysql.connection.commit()
		cur.close()
		return json.dumps(getall)

@app.route('/createCont', methods = ['POST'])
def test5():
	if request.method == "POST":
		data = request.get_json(force = True)
		data = json.loads(data)
		Name = data['Name']
		Address = data['Address']
		Email = data['Email']
		Number = data['Number']
		Userid = data['Userid']
		Date = data['Date']
		cur = mysql.connection.cursor()
		cur.execute("INSERT INTO Contacts(Name, Address, Email, Numb, Userid,Date) VALUES (%s, %s, %s, %s, %s,%s)", (Name, Address,Email,Number,Userid,Date))
		mysql.connection.commit()
		cur.close()
		return "Success"

@app.route('/deleteCont', methods = ['POST'])
def test6():
	if request.method == "POST":
		data = request.get_json(force = True)
		data = json.loads(data)
		Contactid = data['Contactid']
		cur = mysql.connection.cursor()
		cur.execute("DELETE FROM Contacts WHERE Contactid = %s", (Contactid,))
		mysql.connection.commit()
		cur.close()
		return "Success"

@app.route('/searchCont', methods = ['POST'])
def test7():
	if request.method == "POST":
		data = request.get_json(force = True)
		# data = json.loads(data)
		Name = data['Name']
		Userid = data['Userid']
		cur = mysql.connection.cursor()
		result = cur.execute("SELECT * FROM Contacts WHERE Userid = %s And Name LIKE %s",(Userid ,("%"+Name+"%")))
		getall = cur.fetchall();
		mysql.connection.commit()
		cur.close()
		return json.dumps(getall)

@app.route('/updateCont', methods = ['POST'])
def test8():
	if request.method == "POST":
		data = request.get_json(force = True)
		data = json.loads(data)
		newName = data['Name']
		newNumber = data['Number']
		newEmail = data['Email']
		newAddr = data['Address']
		Contactid = data['Contactid']
		cur = mysql.connection.cursor()
		cur.execute("UPDATE Contacts Set Name = %s, Numb = %s, Address = %s, Email = %s WHERE (Contactid = %s)",(newName,newNumber, newAddr, newEmail, Contactid))
		mysql.connection.commit()
		print (cur.rowcount)
		cur.close()
		return 'success'

# This just runs the app, like main in C.
if __name__ == '__main__':
	# run!
	app.run(threaded= True,debug = True)

