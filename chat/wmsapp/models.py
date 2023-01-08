import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="database@9440672439",
    database="world"
)

mycursor_lib = mydb.cursor()
receiver_reg="211FA04563"
sender_reg="211FA04562"
sql = "select * from messages where (sender=%s and reciver=%s) or (sender=%s and reciver=%s)"
value = (receiver_reg,sender_reg,sender_reg,receiver_reg)
mycursor_lib.execute(sql,value)
myresult = mycursor_lib.fetchall()
for i in myresult:
	print(i)
