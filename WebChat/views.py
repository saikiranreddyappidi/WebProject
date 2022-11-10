import datetime
import random
import secrets
import socket
import string

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
    template = loader.get_template('parent.html')
    return HttpResponse(template.render({}, request))


def iframe(request):
    template = loader.get_template('child-iframe.html')
    return HttpResponse(template.render({}, request))


def loginform(request):
    template = loader.get_template('login.html')
    cookie = HttpResponse(template.render({}, request))
    c_value=makecookie(request)
    cookie.set_cookie("cltunqe", c_value, max_age=None)
    mycursor = mydb.cursor()
    sql = "insert into active_users (cookie) values(%s)"
    values = (c_value,)
    mycursor.execute(sql, values)
    mydb.commit()
    return cookie


def newlogin(request):
    if request.method=="POST":
        reg=request.POST['reg']
        pswd=request.POST['pswd']
        print(reg,pswd)
    else:
        return HttpResponseRedirect(reverse('loginform'))
    mycursor = mydb.cursor()
    sql = "select password from details where regno=%s"
    values = (reg,)
    mycursor.execute(sql, values)
    myresult = mycursor.fetchall()
    print(myresult)
    ip = get_ip(request)
    if myresult[0][0] is None:
        mycursor = mydb.cursor()
        sql = "update details set password=%s,datetime=%s where regno=%s"
        values = (pswd, datetime.datetime.now(),reg)
        mycursor.execute(sql, values)
        mydb.commit()
    elif myresult[0][0]==pswd:
        pass
    else:
        return HttpResponseRedirect(reverse('loginform'))
    mycursor = mydb.cursor()
    cookie = request.COOKIES['cltunqe']
    sql = "update active_users set regno=%s where cookie=%s"
    values = (reg, cookie)
    mycursor.execute(sql, values)
    mydb.commit()
    return HttpResponseRedirect(reverse('index'))
    


def index(request):
    cookie=request.COOKIES['cltunqe']
    mycursor = mydb.cursor()
    sql = "select regno from active_users where cookie=%s"
    values = (cookie,)
    mycursor.execute(sql, values)
    myresult = mycursor.fetchall()
    reg=myresult[0][0]
    if reg != 0:
        template = loader.get_template('parent.html')
        # for public messages
        mycursor_lib = mydb.cursor()
        sql = "select * from messages where reciver='public' order by datetime"
        mycursor_lib.execute(sql)
        myresult = mycursor_lib.fetchall()
        content=[]
        for i in myresult:
            mymembers = {}
            if reg==i[1]:
                mymembers['me']=1
            else:
                mymembers['me']=0
            mymembers['reg'] = i[1]
            mymembers['time'] = i[4]
            mymembers['content'] = i[3]
            content.append(mymembers)
        # for active users
        mycursor_world = mydb.cursor()
        sql = "select * from active_users where regno!=%s order by date_time"
        value=(reg,)
        mycursor_world.execute(sql,value)
        myresult_world = mycursor_world.fetchall()
        active_list = []
        for i in myresult_world:
            mymembers = {}
            mymembers['reg'] = i[1]
            mymembers['time'] = i[4]
            active_list.append(mymembers)
        reciver=[{'user':'Public','link':'all'}]
        context = {'message': content,'active_users':active_list,'receiver':reciver}
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponseRedirect(reverse('loginform'))


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
