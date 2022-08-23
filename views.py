import datetime
import math
import os
import random
import secrets
import smtplib
import string
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from urllib import request

import mysql.connector
import base64
from django.contrib.auth import authenticate, login, user_logged_in
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, response
from django.shortcuts import render
from django.template import loader
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect

from .models import Members

print("Hello !, admin")

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="database_password",
    database="database_name"
)


mydb1 = mysql.connector.connect(
    host="localhost",
    user="root",
    password="database_password",
    database="database_name"
)


def firstreg(request):
    template = loader.get_template('first.html')
    return HttpResponse(template.render())


def first(request):
    global reg
    if request.method == "POST":
        reg = filter_data(request,request.POST['reg'])
        sec = filter_data(request,request.POST['sec'])
        pswd = request.POST['pswd']
        reg = reg.upper()
        print("Reg:", reg, "Sec:", sec, "Pswd:", pswd)
        mycursor = mydb.cursor()
        sql = "insert into testing(reg, sec) values(%s,%s)"
        values = (reg, sec)
        mycursor.execute(sql, values)
        mydb.commit()
        s = search(reg, pswd)
        if s == 2:  # all ok
            return HttpResponseRedirect(reverse('course'))
        elif s == 1:  # wrong password
            return HttpResponse('wrong password entered !!! . Try again')
        elif s == 0:  # no account
            return HttpResponseRedirect(reverse('createacnt'))
        else:
            return HttpResponseRedirect(reverse('firstreg'))
    return HttpResponseRedirect(reverse('firstreg'))


def course(request):
    try:
        t = check_status(request)
        template = loader.get_template('course.html')
        cookie = HttpResponse(template.render({}, request))
        print(t, "chk-stat")
        if t == 2:
            return cookie
        elif t == 0:
            global reg
            regnum = reg
            reg = "00"
            print(regnum)
            reg_check = check_with_reg(request, regnum)
            if reg_check == 1:
                date = datetime.datetime.now()
                cookie_value = makecookie()
                ip = get_ip(request)
                my_cursor = mydb.cursor()
                sql = "insert into cookie(regno, cookievalue, ip, datetime) values(%s,%s,%s,%s)"
                values = (regnum, cookie_value, ip, date)
                my_cursor.execute(sql, values)
                mydb.commit()
                print("user logged in,done with db")
                print(cookie, ip)
                cursor = mydb1.cursor()
                sql = "insert into assigned_cookies(reg, cookies, datetime) values(%s,%s,%s)"
                values = (regnum, cookie_value, date)
                cursor.execute(sql, values)
                mydb1.commit()
                print("ok")
                cookie.set_cookie("userid", cookie_value, max_age=None)
                return cookie
            elif reg_check == 3:
                return HttpResponse('More than one user is active with same reg.no')
            elif reg_check == 0:
                return HttpResponseRedirect(reverse('firstreg'))
            else:
                cookie.set_cookie("userid", reg_check, max_age=None)
                return cookie
        elif t == 1:
            return HttpResponse('More than one user at the same time is not allowed')
    except :
        return HttpResponseRedirect(reverse('firstreg'))


def check_status(request):
    try:
        c_value = filter_data(request,request.COOKIES['userid'])
        ip = get_ip(request)
        mycursor = mydb.cursor()
        sql = "select * from cookie where cookievalue=%s"
        value=(c_value,)
        mycursor.execute(sql,value)
        myresult = mycursor.fetchall()
        if len(myresult) != 0:
            i = myresult[0]
            if i[2] == c_value and i[3] == ip:
                print("Check status ok")
                print(c_value, ip)
                return 2
            elif i[2] == c_value and i[3] != ip:
                print("Multiple users at the same time")
                return 1
        else:
            return 0
    except:
        print("chck-stat exception")
        return 0


def check_with_reg(request,reg_no):
    try:
        if reg_no=="00":
            return 0
        ip=get_ip(request)
        mycursor = mydb.cursor()
        sql = "select * from cookie where regno=%s"
        value = (reg_no,)
        mycursor.execute(sql, value)
        myresult = mycursor.fetchall()
        if len(myresult) != 0:
            i = myresult[0]
            if i[1] == reg_no and ip == i[3]:
                print("Already logged in")
                return i[2]
            elif i[1] == reg_no and ip != i[3]:
                print("more than one user")
                return 3
        else:
            print("Not logged in c-w-r")
            return 1
    except:
        return 0


def cse(request):
    template = loader.get_template('cse.html')
    mycursor = mydb1.cursor()
    sql = "select * from links_provided where branch='cse'"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    # print("result form db:",myresult)
    list_members = []
    k = 0
    for i in myresult:
        # print(i,type(i))
        k = k + 1
        mymembers = {}
        mymembers['id'] = k
        mymembers['facultyname'] = i[7]
        mymembers['filename'] = i[2]
        mymembers['link'] = i[3]
        mymembers['file_type'] = i[5]
        list_members.append(mymembers)
    context = {'mymembers': list_members}
    check = check_status(request)
    if check == 2:
        return HttpResponse(template.render(context, request))
    elif check == 1:
        return HttpResponse("Already one user is active at the same time")
    else:
        return HttpResponseRedirect(reverse('firstreg'))


def user_logout(request):
    returned_cookie = request.COOKIES['userid']
    mycursor = mydb.cursor()
    sql = "delete from cookie where cookievalue=%s"
    values = (returned_cookie,)
    mycursor.execute(sql, values)
    mydb.commit()
    print("logged out")
    return HttpResponseRedirect(reverse('firstreg'))


def userprofile(request):
    try:
        template = loader.get_template('userprofile.html')
        t = check_status(request)
        if t == 2:
            c_value = filter_data(request, request.COOKIES['userid'])
            mycursor = mydb.cursor()
            sql = "select * from cookie where cookievalue=%s"
            value = (c_value,)
            mycursor.execute(sql, value)
            myresult = mycursor.fetchall()
            reg_no = myresult[0][1]
            mycursor = mydb1.cursor()
            sql = "select * from student_info where Reg_no=%s"
            value = (reg_no,)
            mycursor.execute(sql, value)
            myresult = mycursor.fetchall()
            list_members = []
            for i in myresult:
                mymembers = {}
                mymembers['reg_no'] = i[1]
                mymembers['name'] = i[2]
                mymembers['mail'] = i[4]
                mymembers['link'] = i[8]
                list_members.append(mymembers)
            context = {'mymembers': list_members}
            return HttpResponse(template.render(context, request))
        else:
            return HttpResponseRedirect(reverse('course'))
    except:
        return HttpResponseRedirect(reverse('firstreg'))


def userinp(request):
    template = loader.get_template('userfiles.html')
    return HttpResponse(template.render())


def userfileinp(request):
    file_name=filter_data(request,request.POST['filename'])
    subject = request.POST['sub']
    link=request.POST['link']
    t=check_status(request)
    if t==2:
        regis = return_reg(request)
        if regis !='0':
            date=datetime.datetime.now()
            sec=18
            cursor = mydb1.cursor()
            sql = "insert into userlinks(reg, sec, filename, link, datetime,subject) values(%s,%s,%s,%s,%s,%s)"
            values = (regis, sec, file_name, link, date,subject)
            cursor.execute(sql, values)
            mydb1.commit()
            return HttpResponseRedirect(reverse('course'))
        else:
            return HttpResponse('Something went wrong when writng to database')    
 

def return_reg(request):
    c_value = filter_data(request,request.COOKIES['userid'])
    ip = get_ip(request)
    mycursor = mydb.cursor()
    sql = "select * from cookie where cookievalue=%s"
    value=(c_value,)
    mycursor.execute(sql,value)
    myresult = mycursor.fetchall()
    if len(myresult) != 0:
        i=myresult[0]
        if i[2] == c_value and i[3] == ip:
            print("Check status ok--returning reg")
            return i[1]
    else:
        return 0


def createacnt(request):
    template = loader.get_template('createacnt.html')
    return HttpResponse(template.render())


def creating(request):
    try:
        name = filter_data(request,request.POST['name'])
        reg = filter_data(request,request.POST['reg'])
        pswd = request.POST['pswd']
        email = filter_data(request,request.POST['mail'])
        link = request.POST['link']
        reg = reg.upper()
        print("input")
        mycursor = mydb1.cursor()
        sql = "select * from student_info"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        k = 0
        print("db")
        for i in myresult:
            print(i,k)
            k += 1
            if i[1] == reg and i[4] == email:
                return HttpResponse("Already account exits on this Registration.no and E-mail !!!")
            elif i[1] == reg:
                return HttpResponse("Already account exists on this Registration.No !!!")
            elif i[4] == email:
                return HttpResponse("Already account exists on this E-mail.Use different one !!!")
            elif k == len(myresult):
                print("creating")
                sql = "insert into student_info(reg_no,name,password,email,photo_link) values(%s,%s,%s,%s,%s)"
                values = (reg, name, pswd, email,link)
                mycursor.execute(sql, values)
                mydb1.commit()
                print("new account created")
                return HttpResponseRedirect(reverse('firstreg'))
    except:
        return HttpResponseRedirect(reverse('firstreg'))


def faculty(request):
    template = loader.get_template('facultyaccess.html')
    return HttpResponse(template.render({}, request))


def facultyaccess(request):
    if request.method == "POST":
        try:
            facultyid = filter_data(request,request.POST['facultyid'])
            facultypswd = request.POST['facultypswd']
            print(facultyid, facultypswd)
            mycursor = mydb1.cursor()
            sql = "select * from faculty"
            mycursor.execute(sql)
            myresult = mycursor.fetchall()
            k = 0
            for i in myresult:
                k = k + 1
                if i[2] == facultyid:
                    if i[3] == facultypswd:
                        print("faculty login verified")
                        t = dup_fac(request,facultyid)
                        print(facultyid)
                        if t == 0:
                            fac_ip = get_ip(request)
                            cookie_value = makecookie()
                            cookie=HttpResponseRedirect("pdf_links")
                            cookie.set_cookie("sessionid", cookie_value, max_age=None)
                            mycursor = mydb.cursor()
                            sql = "insert into active_users(faculty_id,cookie,login_ip) values (%s,%s,%s)"
                            values = (facultyid, cookie_value, fac_ip)
                            mycursor.execute(sql, values)
                            mydb.commit()
                            print("f-a-c ok,login success")
                            return cookie
                        else:
                            return HttpResponse('Already one active user with this id on ip'+str(t))
                    else:
                        return HttpResponse("Wrong password !!!")
                elif k == len(myresult):
                    return HttpResponse("No account found !!!")
        except:
            return HttpResponseRedirect(reverse('faculty'))
    else:
        return HttpResponseRedirect(reverse("faculty"))


def pdf_links(request):
    try:
        print('pdf-link')
        t=faculty_auth(request,1)
        if t!=0:
            template = loader.get_template('pdf_links.html')
            mycursor = mydb1.cursor()
            sql = "select * from links_provided where faculty_id=%s"
            values = (t)
            mycursor.execute(sql, (values,))
            myresult = mycursor.fetchall()
            # print("result form db:",myresult)
            list_members = []
            k = 0
            for i in myresult:
                # print(i,type(i))
                k = k + 1
                mymembers = {}
                mymembers['id'] = k
                mymembers['filename'] = i[2]
                mymembers['link'] = i[3]
                mymembers['branch'] = i[4]
                mymembers['file_type'] = i[5]
                list_members.append(mymembers)
            # print("list :" ,list_members,type(list_members))
            context = {'mymembers': list_members}
            # print("context:",context,type(context))
            return HttpResponse(template.render(context, request))
        else:
            return HttpResponseRedirect(reverse('faculty'))    
    except:
        return HttpResponseRedirect(reverse("faculty"))


def delete(request, filename):
    t=faculty_auth(request,0)
    if t==2:
        try:
            print(filename)
            mycursor = mydb1.cursor()
            sql = "delete from links_provided where file_name=%s"
            value = (filename)
            mycursor.execute(sql, (value,))
            mydb1.commit()
            return HttpResponseRedirect(reverse('pdf_links'))
        except:
            return HttpResponseRedirect(reverse('faculty'))
    else:
        return HttpResponseRedirect(reverse('faculty'))


def add(request):
    template = loader.get_template('addlink.html')
    return HttpResponse(template.render({}, request))


def addlink(request):
    t = faculty_auth(request, 1)
    if t != 0:
        filename_to_upload = filter_data(request,request.POST['filename'])
        file_type = filter_data(request,request.POST['file_type'])
        link_to_upload = request.POST['dlink']
        branch = filter_data(request,request.POST['branch'])
        print(file_type, branch)
        mycursor = mydb1.cursor()
        sql = "select * from links_provided where file_name=%s"
        value=(filename_to_upload,)
        mycursor.execute(sql,value)
        myresult = mycursor.fetchall()
        if len(myresult) != 0:
            return HttpResponse("File name already exits!!!\nTry with other name.")
        mycursor1 = mydb1.cursor()
        sql1 = "select * from faculty where faculty_id=%s"
        value1 = (t,)
        mycursor1.execute(sql1, value1)
        myresult1 = mycursor1.fetchall()
        fac_name = myresult1[0][1]
        date = datetime.datetime.now()
        sql = "insert into links_provided (faculty_id, file_name, drive_links, branch, file_type, datetime, facultyname) values (%s, %s, %s, %s, %s, %s, %s)"
        value = (t, filename_to_upload, link_to_upload, branch, file_type,date,fac_name)
        mycursor.execute(sql, value)
        mydb1.commit()
        return HttpResponseRedirect(reverse('pdf_links'))
    else:
        return HttpResponseRedirect(reverse('faculty'))


def fac_logout(request):
    returned_cookie = request.COOKIES['sessionid']
    mycursor = mydb.cursor()
    sql = "delete from active_users where cookie=%s"
    values = (returned_cookie,)
    mycursor.execute(sql, values)
    mydb.commit()
    print("logged out")
    return HttpResponseRedirect(reverse('firstreg'))


def faculty_auth(request,enable):
    try:
        c_value = request.COOKIES['sessionid']
        print(c_value)
        ip = get_ip(request)
        mycursor = mydb.cursor()
        sql = "select * from active_users where cookie=%s"
        value=(c_value,)
        mycursor.execute(sql,value)
        myresult = mycursor.fetchall()
        if len(myresult) != 0:
            i=myresult[0]
            print(i)
            if enable == 1:
                return i[1]
            else:
                return 2
        else:
            print("not logged in a-c-u")
            return 0
    except:
        return 0


def dup_fac(request,fac_id):
    try:
        ip = get_ip(request)
        mycursor = mydb.cursor()
        sql = "select * from active_users where faculty_id=%s"
        value=(fac_id,)
        mycursor.execute(sql,value)
        myresult = mycursor.fetchall()
        print('d-f')
        if len(myresult) != 0:
            i=myresult[0]
            print(i)
            if i[1] == fac_id:
                print("One active user")
                return ip
        else:
            print("not logged in a-c-u")
            return 0
    except:
        return 0


def mail_checking(request):
    template = loader.get_template('mail_checking.html')
    return HttpResponse(template.render({}, request))


def comparing_mail(request):
    mail = filter_data(request,request.POST['mail'])
    reg = filter_data(request,request.POST['reg'])
    reg = reg.upper()
    print("Entered mail :", mail, "Reg.no", reg)
    my_cursor = mydb.cursor()
    sql = "delete from active_otps where reg=%s"
    value = (reg)
    my_cursor.execute(sql, (value,))
    mydb.commit()
    mycursor = mydb1.cursor()
    sql = "select * from student_info where reg_no=%s"
    val=(reg)
    mycursor.execute(sql, (val,))
    myresult = mycursor.fetchall()
    if len(myresult) != 0:
        i=myresult[0]
        if mail == i[4]:
            print("correct mail entered")
            otp = str(sendingotp(i[4], i[2], i[3]))
            print("sent otp:", otp)
            date=datetime.datetime.now()
            cookie_value = makecookie()
            mycursor = mydb.cursor()
            ip = get_ip(request)
            sql = "insert into active_otps (reg,otp,ip,datetime,cookie) values (%s,%s,%s,%s,%s)"
            values = (reg, otp, ip, date, cookie_value)
            mycursor.execute(sql, values)
            mydb.commit()
            my_cursor = mydb1.cursor()
            sql = "insert into assigned_otp (reg,otp,ip,datetime,cookie) values (%s,%s,%s,%s,%s)"
            values = (reg, otp, ip, date, cookie_value)
            my_cursor.execute(sql, values)
            mydb1.commit()
            cookie = HttpResponseRedirect(reverse('updating_password'))
            cookie.set_cookie("tcookie", cookie_value, max_age=None)
            return cookie
        elif mail != i[4]:
            print("wrong mail entered")
            return HttpResponse('wrong mail entered !!!')
    else:
        return HttpResponse('No account found with this registration')
    return HttpResponseRedirect(reverse('firstreg'))


def updating_password(request):
    template = loader.get_template('updating_password.html')
    return HttpResponse(template.render({}, request))


def importing_password(request):
    enotp = filter_data(request,request.POST['otp'])
    pswd = request.POST['pswd']
    repswd = request.POST['repswd']
    mycursor = mydb.cursor()
    web_cookie=request.COOKIES['tcookie']
    sql = "select * from active_otps where cookie=%s"
    value=(web_cookie,)
    mycursor.execute(sql,value)
    myresult = mycursor.fetchall()
    if len(myresult) != 0:
        i=myresult[0]
        reg_form_db = i[1]
        otp_from_db = i[2]
        if enotp == otp_from_db:
            print("OTP confirmation success")
            print(pswd,repswd)
            if pswd != repswd:
                print("password confirmation failed")
                return HttpResponse("Password confirmation failed !!!")
            else:
                mycursor = mydb1.cursor()
                sql = "update student_info set PassWord=%s where reg_no=%s"
                values = (pswd,reg_form_db)
                mycursor.execute(sql, values)
                mydb1.commit()
                print("password updated")
                my_cursor = mydb.cursor()
                sql = "delete from active_otps where reg=%s"
                value = (reg_form_db)
                my_cursor.execute(sql, (value,))
                mydb.commit()
                return HttpResponseRedirect(reverse('firstreg'))
        else:
            print("OTP confirmation failed")
            return HttpResponse("wrong OTP entered !!!")
    else:
        return HttpResponse('A problem occured.Try again later !!!')

def newadmin(request):
    template = loader.get_template('newadmin.html')
    return HttpResponse(template.render({}, request))


def search(reg, password):
    mycursor = mydb1.cursor()
    sql = "select * from student_info where reg_no=%s"
    val=(reg)
    mycursor.execute(sql,(val,))
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


def sendingotp(mail, name, psawd):
    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.ehlo()
    smtp.starttls()
    smtp.login('yourmail@gmail.com', 'app_password')
    msg = MIMEMultipart()
    subject = "Reset Password Verification code"
    msg['Subject'] = subject
    l = len(mail)
    nl = len(name)
    pl = len(psawd)
    l = int(l * l + math.sin(math.sqrt(l)) + math.ceil(math.sqrt(l)) + math.pi)
    nl = int(l * l + math.cos(math.sqrt(nl)) + math.ceil(math.sqrt(nl)) + math.pi)
    pl = int(l * l + math.tan(math.sqrt(pl)) + math.floor(math.sqrt(pl)) + math.pi)
    hotp = l + nl + pl + min(l, nl, pl) + random.randint(l, nl)
    text1 = "Hi " + name + "," + "\n" + "\n" + "We received your request for changing the password of your pdfs account." + "\n" + "\n" + "Your otp code is: " + str(
        hotp)+"This otp will expires after 5 minutes" + "\n" + "\n"
    text2 = "If you didn't request this code, you can safely ignore this email. Someone else might have typed your email address by mistake." + "\n" + "\n"
    text3 = "Thanks," + "\n" + '\n' + "The pdfs account team"
    text = text1 + text2 + text3
    msg.attach(MIMEText(text))
    to = [str(mail)]
    smtp.sendmail(from_addr="yourmail@gmail.com", to_addrs=to, msg=msg.as_string())
    smtp.quit()
    print("Mail sent")
    return hotp


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


def makecookie():
    sum = 0
    n = random.randint(20, 30)
    for _ in range(2):
        sum += random.randint(1990000, 59977779)
    al = str(''.join(random.choices(string.ascii_letters + string.digits, k=n)))
    sc = str(''.join(secrets.choice(string.ascii_letters + string.digits) for i in range(n)))
    cookie = al + str(sum) + sc
    return cookie


def btech(request):
    template = loader.get_template('btech.html')
    return HttpResponse(template.render({}, request))

def fileip(request):
    name = request.POST['filename']
    fileinp = request.FILES['file']
    cursor = mydb.cursor()
    file = open(fileinp, 'rb').read()
    file = base64.b64encode(file)
    args = (name, file)
    query = 'INSERT INTO files(file_name,document) VALUES(%s, %s)'
    cursor.execute(query, args)
    mydb.commit()
    return HttpResponse('ok')


def filter_data(request,word):
    arr = ['`', '!', '#', '$', '%', '^', '&', '*', '(', ')', '+', '=', '/', '<', '>', '/', '?', '~', 'script', '"',
           "'", ';', ':',',']
    for i in word:
        if i in arr:
            word = word.replace(i, "_")
    return word
