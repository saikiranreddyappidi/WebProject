#main python file to run the website
#This is generally called views file
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from .models import Members
import mysql.connector
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import smtplib
import os
import math
import random
from django.contrib.auth import authenticate, login,user_logged_in
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_protect


print("Hello !, admin")

mydb=mysql.connector.connect(
    host="localhost",
    user="root",
    password="database_password",
    database="database_name"
)

mydb1=mysql.connector.connect(
    host="localhost",
    user="root",
    password="database_password",
    database="database_name"
)



def firstreg(request):
    template = loader.get_template('first.html')
    return HttpResponse(template.render())

def wrongmessage(request):
    template = loader.get_template('first.html')
    message=["wrong pswd"]
    context={'message':message}
    return HttpResponse(template.render(context, request))

def first(request):
    global reg
    global sec
    global pswd
    try:
        reg = request.GET['reg']
        sec = request.GET['sec']
        pswd = request.GET['pswd']
        reg = reg.upper()
        details = Members(reg=reg, sec=sec)
        details.save()
        print("Reg:", reg, "Sec:", sec, "Pswd:", pswd)
        mycursor = mydb.cursor()
        sql = "insert into testing(reg, sec) values(%s,%s)"
        values = (reg, sec)
        mycursor.execute(sql, values)
        mydb.commit()
        user = authenticate(username=reg, password=pswd)
        print("hey")
        if user is not None:
            print("hi")
            login(request, user)
        else:
            print("hello")
        get_ip(request)
        s = search(reg, pswd)
        if s == 2:  # all ok
            return HttpResponseRedirect(reverse('course'))
        elif s == 1:  # wrong password
            return HttpResponse('wrong password entered !!! . Try again')
        elif s == 0:  # no account
            return HttpResponseRedirect(reverse('createacnt'))

    except:
        return HttpResponseRedirect(reverse('firstreg'))


def createacnt(request):
    template=loader.get_template('createacnt.html')
    return HttpResponse(template.render())

def creating(request):
    try:
        name = request.GET['name']
        reg = request.GET['reg']
        pswd = request.GET['pswd']
        email = request.GET['mail']
        reg = reg.upper()
        mycursor = mydb1.cursor()
        sql = "select * from student_info"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        k = 0
        for i in myresult:
            k = k + 1
            if i[1] == reg and i[4] == email:
                return HttpResponse("Already account exits on this Registration.No and E-mail !!!")
            elif i[1] == reg:
                return HttpResponse("Already account exists on this Registration.No !!!")
            elif i[4] == email:
                return HttpResponse("Already account exists on this E-mail.Use different one !!!")
            else:
                sql = "insert into student_info(reg_no,name,password,email) values(%s,%s,%s,%s)"
                values = (reg, name, pswd, email)
                mycursor.execute(sql, values)
                mydb1.commit()
                print("new account created")
                return HttpResponseRedirect(reverse('firstreg'))
    except:
        return HttpResponseRedirect(reverse('firstreg'))


def faculty(request):
    template=loader.get_template('facultyaccess.html')
    return HttpResponse(template.render({}, request))

def facultyaccess(request):
    if request.method == "POST":
        try:
            facultyid = request.POST['facultyid']
            facultypswd = request.POST['facultypswd']
            print(facultyid, facultypswd)
            mycursor = mydb1.cursor()
            sql = "select * from faculty"
            mycursor.execute(sql)
            myresult = mycursor.fetchall()
            k = 0
            for i in myresult:
                print(i)
                k = k + 1
                if i[2] == facultyid:
                    global f_id
                    f_id = facultyid
                    if i[3] == facultypswd:
                        print("faculty login success")
                        fac_ip = get_ip(request)
                        mycursor = mydb.cursor()
                        log_in = 1
                        sql = "insert into active_users(faculty_id,log_in_or_out,login_ip) values (%s,%s,%s)"
                        values = (facultyid, log_in, fac_ip)
                        mycursor.execute(sql, values)
                        mydb.commit()
                        return HttpResponseRedirect("pdf_links")
                    else:
                        return HttpResponse("Wrong password !!!")
                elif k == len(myresult):
                    return HttpResponse("No account found !!!")
        except :
            return HttpResponseRedirect("faculty")
    else:
        return HttpResponseRedirect("faculty")

def pdf_links(request):
    try:
        template = loader.get_template('pdf_links.html')
        mycursor = mydb1.cursor()
        sql = "select * from links_provided where faculty_id=%s"
        values = (f_id)
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
    except:
        return HttpResponseRedirect(reverse("faculty"))

def delete(request,filename):
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

def add(request):
    template=loader.get_template('addlink.html')
    return HttpResponse(template.render({}, request))

def addlink(request):
    try:
        filename_to_upload = request.POST['filename']
        file_type = request.POST['file_type']
        link_to_upload = request.POST['dlink']
        branch = request.POST['branch']
        print(file_type,branch)
        ip_fac = get_ip(request)
        mycursor = mydb1.cursor()
        sql = "select * from links_provided"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        for i in myresult:
            if i[2] == filename_to_upload:
                return HttpResponse("File name already exits!!!\nTry with other name.")
        fac_ip = get_ip(request)
        mycursors = mydb.cursor()
        sqls = "select faculty_id from active_users where login_ip=%s"
        values = (fac_ip)
        mycursors.execute(sqls, (values,))
        myresult = mycursors.fetchall()
        print(myresult[0][0])
        sql = "insert into links_provided (faculty_id,file_name,drive_links,branch,file_type) values (%s,%s,%s,%s,%s)"
        value = (myresult[0][0], filename_to_upload, link_to_upload, branch, file_type)
        mycursor.execute(sql, value)
        mydb1.commit()
        return HttpResponseRedirect(reverse('pdf_links'))
    except:
        return HttpResponseRedirect(reverse('faculty'))


def mail_checking(request):
    template=loader.get_template('mail_checking.html')
    return HttpResponse(template.render({}, request))

def comparing_mail(request):
    global reg
    mail=request.POST['mail']
    reg=request.POST['reg']
    reg=reg.upper()
    print("Entered mail :",mail,"Reg.no",reg)
    #if match
    mycursor = mydb1.cursor()
    sql = "select * from student_info"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    k = 0
    for i in myresult:
        k = k + 1
        if i[1] == reg:
            if i[1] == reg and mail == i[4]:
                global no_of_times
                no_of_times=int(i[6])
                print("correct mail entered")
                global otp
                otp=str(sendingotp(i[4],i[2],i[3]))
                print("sent otp:",otp)
                mycursor = mydb1.cursor()
                global ip
                ip=str(get_ip(request))
                sql = "update student_info set otp=%s,ip=%s where Reg_No=%s"
                values = (otp,ip,reg)
                mycursor.execute(sql, values)
                mydb1.commit()
                return HttpResponseRedirect(reverse('updating_password'))
            elif i[1] == reg and mail != i[4]:
                print("wrong mail entered")
                return HttpResponse('wrong mail entered !!!')
        if k == len(myresult):
            print("no account found")
            return HttpResponseRedirect(reverse('createacnt'))

    return HttpResponseRedirect(reverse('updating_password'))

def updating_password(request):
    template = loader.get_template('updating_password.html')
    return HttpResponse(template.render({}, request))

def importing_password(request):
    enotp=request.POST['otp']
    pswd=request.POST['pswd']
    repswd=request.POST['repswd']
    ip=get_ip(request)
    mycursor = mydb1.cursor()
    sql = "select * from student_info"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    k = 0
    for i in myresult:
        k = k + 1
        if i[7] == ip:
            reg_form_db=i[1]
            otp_from_db=i[5]
            break
    if enotp==otp_from_db:
        print("OTP confirmation success")
        if pswd != repswd:
            print("password confirmation failed")
            return HttpResponse("Password confirmation failed !!!")
        else:
            ip1=get_ip(request)
            fixed_otp="1729"
            fixed_ip="255.255.255.0"
            mycursor = mydb1.cursor()
            sql = "update student_info set PassWord=%s,otp=%s,no_of_times=no_of_times+1,ip=%s where ip=%s and otp=%s"
            values = (pswd,fixed_otp,fixed_ip, ip1,enotp)
            mycursor.execute(sql, values)
            mydb1.commit()
            print("password updated")
            return HttpResponseRedirect(reverse('firstreg'))
    else:
        print("OTP confirmation failed")
        return HttpResponse("wrong OTP entered !!!")



@login_required(login_url="firstreg")
def course(request):
    template=loader.get_template('course.html')
    return HttpResponse(template.render({}, request))


@login_required(login_url="firstreg")
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
        mymembers['facultyname'] = "Sai Kiran"
        mymembers['filename'] = i[2]
        mymembers['link'] = i[3]
        mymembers['file_type'] = i[5]
        list_members.append(mymembers)
    # print("list :" ,list_members,type(list_members))
    context = {'mymembers': list_members}
    # print("context:",context,type(context))
    return HttpResponse(template.render(context, request))

def admin(request):
    template = loader.get_template('admin.html')
    return HttpResponse(template.render({}, request))


def search(reg,password):
    mycursor = mydb1.cursor()
    sql="select * from student_info"
    mycursor.execute(sql)
    myresult=mycursor.fetchall()
    k=0
    for i in myresult:
        k=k+1
        if i[1]==reg:
            if i[1]==reg and password==i[3]:
                print("login successful")
                return 2
            elif i[1]==reg and password!=i[3]:
                print("wrong password")
                return 1
        if k==len(myresult):
            print("no account")
            return 0

def sendingotp(mail,name,psawd):
    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.ehlo()
    smtp.starttls()
    smtp.login('yourmail@gmail.com', 'app_password')
    msg = MIMEMultipart()
    subject = "OTP"
    msg['Subject'] = subject
    l=#
    nl=#
    pl=#
    hotp = l + nl + pl + min(l, nl, pl)+random.randint(l,nl)
    text = "Your otp for your pdfs account is " + str(hotp) + ".\nFill this OTP there and reset your password"
    msg.attach(MIMEText(text))
    to = [str(mail)]
    smtp.sendmail(from_addr="saikiranreddyvfstr@gmail.com", to_addrs=to, msg=msg.as_string())
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



def btech(request):
    template=loader.get_template('btech.html')
    return HttpResponse(template.render({}, request))

def pharma(request):
    template=loader.get_template('pharma.html')
    return HttpResponse(template.render({}, request))

def law(request):
    template=loader.get_template('law.html')
    return HttpResponse(template.render({}, request))

def manage(request):
    template=loader.get_template('management.html')
    return HttpResponse(template.render({}, request))



