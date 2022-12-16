import mysql.connector
import datetime
import time

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="database@9440672439",
    database="regist"
)


def exp_otp(t: int):
    mycursor = mydb.cursor()
    sql = "select * from active_otps"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    for i in myresult:
        time_1 = i[4]
        time_2 = datetime.datetime.now()
        time_2 = str(time_2)
        time_1 = str(time_1)
        time_2 = time_2.split(":")
        time_1 = time_1.split(":")
        mins = int(time_2[-2]) - int(time_1[-2])
        secs = (float(time_2[-1]) - float(time_1[-1]))
        if secs < 0:
            secs = -secs
        remaining = mins + secs/60
        print(i[1], remaining)
        if remaining > 5 or i[6] > 5:
            print("deleted otp", i[1])
            sql = "delete from active_otps where reg=%s"
            values = (i[1],)
            mycursor.execute(sql, values)
            mydb.commit()
    time.sleep(30)
    print(t)
    exp_otp(t+1)


exp_otp(0)
