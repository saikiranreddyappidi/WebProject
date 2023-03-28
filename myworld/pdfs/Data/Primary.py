import random
import secrets
import string

import mysql.connector

mydb = mysql.connector.connect(
	host="localhost",
	user="root",
	password="database@9440672439",
	database="library"
)

"""
1. We then create a class called DB. This class contains the methods to connect to the database and perform the CRUD
operations.
2. We then create a method called get_reg. This method takes in the cookie value as a parameter, and it returns the
registration number corresponding to the cookie value.
3. We then create a method called search. This method takes in the registration number and the password as parameters,
and returns the student information if the password is correct. If the password is incorrect, it returns 1. If the
registration number is not found in the database, it returns 0. If there is an exception, it also returns 0. """
class DB:
	def get_reg(self, c_value):
		mycursor = mydb.cursor()
		sql = "select reg from assigned_cookies where cookies=%s"
		value = (c_value,)
		mycursor.execute(sql, value)
		myresult = mycursor.fetchall()
		print(myresult)
		return myresult
	
	def search(self, reg, password):
		try:
			mycursor = mydb.cursor()
			sql = "select * from student_info where reg_no=%s"
			val = (reg,)
			mycursor.execute(sql, val)
			myresult = mycursor.fetchall()
			if len(myresult) != 0:
				i = myresult[0]
				if i[1] == reg and password == i[3]:
					print("login successful")
					return 2
				elif i[1] == reg and password != i[3]:
					print("wrong password")
					return 1
			else:
				return 0
		except:
			print('search exception')
			return 0

"""The cookies class creates the cookie that will be sent and set on the client side for unique identification of the user."""
class Cookies:
	def makecookie(self):
		sum = 0
		n = random.randint(20, 30)
		for _ in range(2):
			sum += random.randint(1990000, 59977779)
		al = str(''.join(random.choices(string.ascii_letters + string.digits, k=n)))
		sc = str(''.join(secrets.choice(string.ascii_letters + string.digits) for i in range(n)))
		cookie = al + str(sum) + sc
		return cookie
	

"""
1. First we have a class user
2. Inside the class we have a function called profile
3. This function will return a list of dictionaries which consists of the following:
	3.1. regno - registration number of the student
	3.2. name - name of the student
	3.3. photo - link to the student's photo
4. The photo link is None if the student doesn't have a photo uploaded 
"""
class user:
	def profile(self):
		mycursor = mydb.cursor()
		sql = "select reg_no,name,photo_link from student_info"
		mycursor.execute(sql)
		myresult = mycursor.fetchall()
		individual = []
		for i in myresult:
			if i[2]=='':
				x = {'regno': i[0], 'name': i[1], 'photo': None}
			else:
				x = {'regno': i[0], 'name': i[1], 'photo': i[2]}
			individual.append(x)
		return individual

# user= user()
# print(user().profile(),sep='\n')