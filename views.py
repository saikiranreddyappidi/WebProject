from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from .models import Members
import mysql.connector

mydb=mysql.connector.connect(
    host="localhost",
    user="root",
    password="database@9440672439",
    database="regist"
)

mydb1=mysql.connector.connect(
    host="localhost",
    user="root",
    password="database@9440672439",
    database="library"
)



def firstreg(request):
    template=loader.get_template('first.html')
    return HttpResponse(template.render())

def createacnt(request):
    template=loader.get_template('createacnt.html')
    return HttpResponse(template.render())

def creating(request):
    name=request.GET['name']
    reg = request.GET['reg']
    pswd=request.GET['pswd']
    mycursor = mydb1.cursor()
    sql = "insert into student_info(reg_no,name,password) values(%s,%s,%s)"
    values = (reg, name, pswd)
    mycursor.execute(sql, values)
    mydb1.commit()
    print("created")
    return HttpResponseRedirect(reverse('firstreg'))

def first(request):
    global reg
    global sec
    global pswd
    reg = request.GET['reg']
    sec = request.GET['sec']
    pswd = request.GET['pswd']
    details=Members(reg=reg, sec=sec)
    details.save()
    print("Reg:",reg,"Sec:",sec,"Pswd:",pswd)
    mycursor = mydb.cursor()
    sql = "insert into testing(reg, sec) values(%s,%s)"
    values = (reg,sec)
    mycursor.execute(sql, values)
    mydb.commit()
    s=search(reg,pswd)
    if s==2:#all ok
        return HttpResponseRedirect(reverse('course'))
    elif s==1:#wrong password
        return HttpResponseRedirect(reverse('firstreg'))
    elif s==0:#no account
        return HttpResponseRedirect(reverse('createacnt'))

def course(request):
    template=loader.get_template('course.html')
    return HttpResponse(template.render({}, request))

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

def cse(request):
    template = loader.get_template('cse.html')
    return HttpResponse(template.render({}, request))

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


