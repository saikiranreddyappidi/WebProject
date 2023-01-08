import datetime
import random
import secrets
import socket
import string
import pyrebase

import mysql.connector
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, RequestContext
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect

print("Hello !, admin")
hostname = socket.gethostname()
print("Running server at: ", socket.gethostbyname(hostname))
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="database@9440672439",
    database="world"
)


def test(request):
    template = loader.get_template('database.html')
    return HttpResponse(template.render({}, request))


def loginform(request):
    template = loader.get_template('login.html')
    cookie = HttpResponse(template.render({}, request))
    cookie.set_cookie("cltunqe", makecookie(request), max_age=None)
    # cookie.set_cookie("prsntstat", "sersidequryforpubliicorall", max_age=None)
    return cookie


def newlogin(request):
    if request.method == "POST":
        reg = request.POST['reg']
        pswd = request.POST['pswd']
        reg = reg.upper()
        print(reg,pswd)
        mycursor = mydb.cursor()
        sql = "select password from details where regno=%s"
        values = (reg,)
        mycursor.execute(sql, values)
        myresult = mycursor.fetchall()
        ip = get_ip(request)
        if myresult[0][0] is None:
            mycursor = mydb.cursor()
            sql = "update details set password=%s,datetime=%s where regno=%s"
            values = (pswd, datetime.datetime.now(), reg)
            mycursor.execute(sql, values)
            mydb.commit()
        elif myresult[0][0] == pswd:
            pass
        else:
            return HttpResponseRedirect(reverse('loginform'))
        mycursor = mydb.cursor()
        cookie = request.COOKIES['cltunqe']
        sql = "insert into active_users(regno, cookie, ip, date_time) values(%s,%s,%s,%s)"
        values = (reg, cookie, ip, datetime.datetime.now())
        mycursor.execute(sql, values)
        mydb.commit()
        sql = "insert into land_page(user,currentpage) values(%s,%s)"
        values = (cookie,"sersidequryforpubliicorall")
        mycursor.execute(sql, values)
        mydb.commit()
        return HttpResponseRedirect(reverse('index'))
    else:
        return HttpResponseRedirect(reverse('loginform'))
    
    
def index(request):
    reg = status(request)
    if reg != 0:
        template = loader.get_template('parent.html')
        target_user = present_page(request)
        # for active users
        mycursor_world = mydb.cursor()
        sql = "select regno,date_time,cookie from active_users where regno!=%s order by date_time"
        value=(reg,)
        mycursor_world.execute(sql,value)
        myresult_world = mycursor_world.fetchall()
        active_list = []
        temp=[]
        for i in myresult_world:
            if i[0] not in temp:
                mymembers = {}
                mymembers['reg'] = i[0]
                mymembers['time'] = i[1]
                mymembers['id'] = i[2]
                active_list.append(mymembers)
            temp.append(i[0])
        reciver=[{'to_user':str(target_user).upper()}]
        context = {'active_users':active_list,'receiver':reciver}
        # print(context)
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponseRedirect(reverse('loginform'))
    

def iframe(request):
    try:
        template = loader.get_template('child-iframe.html')
        reg = status(request)
        if reg != 0:
            receiver_reg = present_page(request)
            if receiver_reg == "public":
                mycursor_lib = mydb.cursor()
                sql = "select * from messages where reciver='public'"
                mycursor_lib.execute(sql)
                myresult = mycursor_lib.fetchall()
                public = [{"decision": True}]
            else:
                mycursor_lib = mydb.cursor()
                sql = "select * from messages where (sender=%s and reciver=%s) or (sender=%s and reciver=%s)"
                value = (receiver_reg, reg, reg, receiver_reg)
                mycursor_lib.execute(sql, value)
                myresult = mycursor_lib.fetchall()
                public = [{"decision": False}]
            content = []
            for i in myresult:
                mymembers = {}
                if reg == i[1]:
                    mymembers['me'] = True
                else:
                    mymembers['me'] = False
                mymembers['reg'] = i[1]
                mymembers['data'] = i[3]
                mymembers['time'] = i[4]
                content.append(mymembers)
            context = {'content': content, 'public': public}
            return HttpResponse(template.render(context, request))
        else:
            return HttpResponse("<h3>Sorry, Something went wrong!!!</h3>")
    except:
        return HttpResponse('Something went wrong!!!')
    

def change_present_page(request, identity):
    current = request.COOKIES['cltunqe']
    mycursor = mydb.cursor()
    sql = "update land_page set currentpage=%s where user=%s"
    values = (identity, current)
    mycursor.execute(sql, values)
    mydb.commit()
    return HttpResponseRedirect(reverse('index'))
    

def tweet(request):
    if request.method == "POST":
        data = request.POST['msg']
        print(data)
        client_reg = status(request)
        receiver_reg = present_page(request)
        mycursor = mydb.cursor()
        sql = "insert into messages(sender, reciver, data, datetime) values (%s,%s,%s,%s)"
        values = (client_reg, receiver_reg, data, datetime.datetime.now())
        mycursor.execute(sql, values)
        mydb.commit()
    return HttpResponseRedirect(reverse('index'))
    
    
# it returns present page of the user
def present_page(request):
    cookie = request.COOKIES['cltunqe']
    mycursor = mydb.cursor()
    sql="select currentpage from land_page where user=%s"
    values = (cookie,)
    mycursor.execute(sql, values)
    myresult = mycursor.fetchall()
    sql = "select regno from active_users where cookie=%s"
    values = (myresult[0][0],)
    mycursor.execute(sql, values)
    myresult = mycursor.fetchall()
    if len(myresult) == 0:
        return 0
    else:
        return myresult[0][0]


def logout(request):
    reg=status(request)
    mycursor = mydb.cursor()
    sql = "delete from active_users where regno=%s"
    values = (reg,)
    mycursor.execute(sql, values)
    mydb.commit()
    return HttpResponseRedirect(reverse('loginform'))


def status(request):
    cookie=request.COOKIES['cltunqe']
    mycursor = mydb.cursor()
    sql = "select regno from active_users where cookie=%s"
    values = (cookie,)
    mycursor.execute(sql, values)
    myresult = mycursor.fetchall()
    if len(myresult) == 0:
        return 0
    else:
        return myresult[0][0]


def get_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        print("returning FORWARDED_FOR")
        ip = x_forwarded_for.split(',')[-1].strip()
    elif request.META.get('HTTP_X_REAL_IP'):
        print("returning REAL_IP")
        ip = request.META.get('HTTP_X_REAL_IP')
    else:
        print("returning REMOTE_ADDR")
        ip = request.META.get('REMOTE_ADDR')
    print(ip)
    return ip


def makecookie(self):
    sum = 0
    n = random.randint(30, 50)
    for _ in range(2):
        sum += random.randint(1990000, 59977779)
    al = str(''.join(random.choices(string.ascii_letters + string.digits, k=n)))
    sc = str(''.join(secrets.choice(string.ascii_letters + string.digits) for i in range(n)))
    cookie = al + str(sum) + sc
    return cookie
