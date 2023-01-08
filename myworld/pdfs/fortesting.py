import mysql.connector

mydb1 = mysql.connector.connect(
    host="localhost",
    user="root",
    password="database@9440672439",
    database="library"
)


regno="211FA04563"
mycursor = mydb1.cursor()
sql = "select content from html_content where regno=%s"
value = (regno,)
mycursor.execute(sql, value)
myresult = mycursor.fetchall()
print(myresult)
if len(myresult) != 0:
        f=open('templates/ownProfile.html','w')
        f.write(myresult[0][0])
        f.close()
f=open('templates/ownProfile.html','r')
print(f.read())
f.close()
