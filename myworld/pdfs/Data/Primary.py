import random
import secrets
import string

import mysql.connector

mydb = mysql.connector.connect(
	host="localhost",
	user="root",
	password="database",
	database="library"
)


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