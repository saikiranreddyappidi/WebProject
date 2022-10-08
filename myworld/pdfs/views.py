import base64
import datetime
import socket

from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse

from .Data.Primary import *
from .MailServices.mail import Mail

print("Hello !, admin")
hostname = socket.gethostname()
print("Running server at: ", socket.gethostbyname(hostname))
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="database@9440672439",
    database="regist"
)


mydb1 = mysql.connector.connect(
    host="localhost",
    user="root",
    password="database@9440672439",
    database="library"
)


def home(request):
    template = loader.get_template('home.html')
    return HttpResponse(template.render())


def get_reg(c_value):
    print("get_reg")
    mycursor = mydb1.cursor()
    sql = "select reg from assigned_cookies where cookies=%s"
    value = (c_value,)
    mycursor.execute(sql, value)
    myresult = mycursor.fetchall()
    print(myresult)
    return myresult


def firstreg(request):
    ip = get_ip(request)
    template = loader.get_template('first.html')
    cookie = HttpResponse(template.render())
    cook = Cookies()
    cookie_value = cook.makecookie()
    cookie.set_cookie("fwist", cookie_value, max_age=None)
    try:
        c_value = filter_data(request, request.COOKIES['userid'])
        print("cookies--", c_value)
        myresult = get_reg(c_value)
        if len(myresult) and myresult[0][0] != '0':
            return HttpResponseRedirect('already_login_once')
        else:
            mycursor = mydb.cursor()
            sql = "insert into first_visit(cookie,ip,datetime) values(%s, %s, %s)"
            values = (cookie_value, ip, datetime.datetime.now())
            mycursor.execute(sql, values)
            mydb.commit()
            return cookie
    except:
        print('exception occured in firstreg')
        mycursor = mydb.cursor()
        sql = "insert into first_visit(cookie,ip,datetime) values(%s, %s, %s)"
        values = (cookie_value, ip, datetime.datetime.now())
        mycursor.execute(sql, values)
        mydb.commit()
        return cookie


def newlogin(request):
    ip = get_ip(request)
    template = loader.get_template('newlogin.html')
    cookie = HttpResponse(template.render())
    cook = Cookies()
    cookie_value = cook.makecookie()
    cookie.set_cookie("fwist", cookie_value, max_age=None)
    mycursor = mydb.cursor()
    sql = "insert into first_visit(cookie,ip,datetime) values(%s, %s, %s)"
    values = (cookie_value, ip, datetime.datetime.now())
    mycursor.execute(sql, values)
    mydb.commit()
    return cookie


def already_login_once(request):
    try:
        returned_cookie = filter_data(request, request.COOKIES['userid'])
        myresult = get_reg(returned_cookie)
        if len(myresult) > 0:
            reg_no = myresult[0][0]
        else:
            return HttpResponseRedirect(reverse('firstreg'))
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
            mymembers['link'] = i[5]
            list_members.append(mymembers)
        context = {'mymembers': list_members}
        template = loader.get_template('already_login_once.html')
        cookie = HttpResponse(template.render(context, request))
        cook = Cookies()
        cookie_value = cook.makecookie()
        cookie.set_cookie("Alin", cookie_value, max_age=None)
        ip = get_ip(request)
        mycursor = mydb.cursor()
        sql = "insert into alreadylogin(reg,cookie,ip,datetime) values(%s, %s, %s, %s)"
        values = (reg_no, cookie_value, ip, datetime.datetime.now())
        mycursor.execute(sql, values)
        mydb.commit()
        print("already_login_once")
        return cookie
    except:
        return HttpResponseRedirect(reverse('firstreg'))


def alreadylogin(request):
    try:
        c_value = filter_data(request, request.COOKIES['Alin'])
        if request.method == "POST":
            pswd = request.POST['pswd']
            mycursor = mydb.cursor()
            sql = "select reg from alreadylogin where cookie=%s"
            value = (c_value,)
            mycursor.execute(sql, value)
            myresult = mycursor.fetchall()
            mycursor = mydb.cursor()
            sql = "insert into testing(reg,password,datetime) values(%s,%s,%s)"
            values = (myresult[0][0], pswd, datetime.datetime.now())
            mycursor.execute(sql, values)
            mydb.commit()
            user = DB()
            s = user.search(myresult[0][0], pswd)
            if s == 2:  # all ok
                mycursor = mydb.cursor()
                sql = "update alreadylogin set enable=1 where cookie=%s"
                values = (c_value,)
                mycursor.execute(sql, values)
                mydb.commit()
                return HttpResponseRedirect(reverse('redirection'))
            elif s == 1:  # wrong password
                return HttpResponse('Wrong Password !!!')
            elif s == 0:  # no account
                print("no account found from already login")
                template = loader.get_template('somethingwentwrong.html')
                return HttpResponse(template.render())
            else:
                print("else from already-login")
                return HttpResponseRedirect(reverse('newlogin'))
    except:
        print("exception occurred in already-login")
        return HttpResponseRedirect(reverse('newlogin'))


def first(request):
    try:
        c_value = filter_data(request, request.COOKIES['fwist'])
        if request.method == "POST":
            reg = filter_data(request, request.POST['reg'])
            pswd = request.POST['pswd']
            reg = reg.upper()
            print("Reg:", reg, "Pswd:", pswd)
            mycursor = mydb.cursor()
            sql = "insert into testing(reg,password,datetime) values(%s,%s,%s)"
            values = (reg, pswd, datetime.datetime.now())
            mycursor.execute(sql, values)
            mydb.commit()
            user = DB()
            s = user.search(reg, pswd)
            if s == 2:  # all ok
                mycursor = mydb.cursor()
                sql = "update first_visit set reg=%s where cookie=%s"
                values = (reg, c_value)
                mycursor.execute(sql, values)
                mydb.commit()
                print("first-course")
                return HttpResponseRedirect(reverse('redirection'))
            elif s == 1:  # wrong password
                return HttpResponse('Wrong Password')
            elif s == 0:  # no account
                return HttpResponse('No account found !!!')
            else:
                return HttpResponseRedirect(reverse('firstreg'))
    except:
        return HttpResponseRedirect(reverse('firstreg'))


def redirection(request):
    print("redirect")
    try:
        template = loader.get_template('redirect.html')
        cookie = HttpResponse(template.render({}, request))
        regnum = '0'
        try:
            c_value_alin = filter_data(request, request.COOKIES['Alin'])
            mycursor = mydb.cursor()
            sql = "select reg,enable from alreadylogin where cookie=%s"
            value = (c_value_alin,)
            mycursor.execute(sql, value)
            myresult = mycursor.fetchall()
            if myresult[0][1]:
                regnum = str(myresult[0][0])
            print(regnum, "from alin course")
        except:
            print("Exception occured in Alin from redirection")
        if regnum == '0':
            c_value_fwist = filter_data(request, request.COOKIES['fwist'])
            mycursor = mydb.cursor()
            sql = "select reg from first_visit where cookie=%s"
            value = (c_value_fwist,)
            mycursor.execute(sql, value)
            myresult = mycursor.fetchall()
            regnum = str(myresult[0][0])
            print(regnum, "form fwist course")
        print(regnum == '0', regnum, type(regnum))
        if regnum == '0':
            template = loader.get_template('somethingwentwrong.html')
            return HttpResponse(template.render())
        reg_check = check_with_reg(request, regnum)
        if reg_check == 1:  # not logged in
            date = datetime.datetime.now()
            cook = Cookies()
            cookie_value = cook.makecookie()
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
        elif reg_check == 3:  # already one user
            print("reached")
            print(regnum)
            template = loader.get_template('continuation.html')
            cookie = HttpResponse(template.render({}, request))
            date = datetime.datetime.now()
            cook = Cookies()
            cookie_value = cook.makecookie()
            ip = get_ip(request)
            my_cursor = mydb.cursor()
            sql = "insert into temp_cookie(reg, cookievalue, ip, datetime) values(%s,%s,%s,%s)"
            values = (regnum, cookie_value, ip, date)
            my_cursor.execute(sql, values)
            mydb.commit()
            cookie.set_cookie("respo", cookie_value, max_age=None)
            return cookie
        else:
            return HttpResponseRedirect(reverse('firstreg'))
    except:
        print("redirection exception")
        template = loader.get_template('somethingwentwrong.html')
        return HttpResponse(template.render())

def course(request):
    try:
        check = check_status(request)
        if check == 2:
            template = loader.get_template('course.html')
            return HttpResponse(template.render())
        elif check == 1:
            return HttpResponse("Already one user is active at the same time")
        else:
            return HttpResponseRedirect(reverse('firstreg'))
    except:
        print("course exception")
        return HttpResponseRedirect(reverse('firstreg'))


def user_response(request):
    print("forced deletion")
    try:
        c_value = filter_data(request, request.COOKIES['respo'])
        mycursor = mydb.cursor()
        sql = "select reg from temp_cookie where cookievalue=%s"
        value = (c_value,)
        mycursor.execute(sql, value)
        myresult = mycursor.fetchall()
        sql = "delete from cookie where regno=%s"
        values = (myresult[0][0],)
        mycursor.execute(sql, values)
        mydb.commit()  #
        try:
            print("fwist deletion")
            # c_value_fwist = filter_data(request, request.COOKIES['fwist'])
            mycursor = mydb.cursor()
            sql = "delete from first_visit where reg=%s"
            value = (myresult[0][0],)
            mycursor.execute(sql, value)
            mydb.commit()
        except:
            print("exception occured in user response, c_value_fwist")
        print(myresult[0][0], "--logged out through forced deletion")  #
        sql = "delete from temp_cookie where reg=%s"
        values = (myresult[0][0],)
        mycursor.execute(sql, values)
        mydb.commit()
        print("logged out of other sessions", myresult[0][0])
        cook = Cookies()
        cookie_value = cook.makecookie()
        ip = get_ip(request)
        my_cursor = mydb.cursor()
        sql = "insert into cookie(regno, cookievalue, ip, datetime) values(%s,%s,%s,%s)"
        values = (myresult[0][0], cookie_value, ip, datetime.datetime.now())
        my_cursor.execute(sql, values)
        mydb.commit()
        template = loader.get_template('redirect.html')
        cookie = HttpResponse(template.render({}, request))
        cookie.set_cookie("userid", cookie_value, max_age=None)
        return cookie
    except:
        print("user response exception")
        template = loader.get_template('somethingwentwrong.html')
        return HttpResponse(template.render())


def check_status(request):
    try:
        c_value = filter_data(request, request.COOKIES['userid'])
        ip = get_ip(request)
        mycursor = mydb.cursor()
        sql = "select * from cookie where cookievalue=%s"
        value=(c_value,)
        mycursor.execute(sql, value)
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


def check_with_reg(request, reg_no):
    try:
        if reg_no == "00":
            return 0
        mycursor = mydb.cursor()
        sql = "select * from cookie where regno=%s"
        value = (reg_no,)
        mycursor.execute(sql, value)
        myresult = mycursor.fetchall()
        if len(myresult) != 0:
            i = myresult[0]
            if i[1] == reg_no:
                return 3
        else:
            print("Not logged in c-w-r from check-with-reg")
            return 1
    except:
        print("check with reg exception")
        return 0


def cse(request, branch):
    try:
        check = check_status(request)
        if check == 2:
            template = loader.get_template('cse.html')
            mycursor = mydb1.cursor()
            sql = "select * from links_provided where branch=%s"
            print(branch)
            value = (branch,)
            mycursor.execute(sql, value)
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

            mycursor = mydb.cursor()
            sql = "select subject from branch_subject where branch=%s"
            mycursor.execute(sql, value)
            myresult_of_b_s = mycursor.fetchall()
            subjects_list = []
            k = 0
            for data in myresult_of_b_s:
                mycursor_lib = mydb1.cursor()
                sql = "select * from apporved_files where subject=%s and enable=1"
                value = (data[0],)
                mycursor_lib.execute(sql, value)
                myresult = mycursor_lib.fetchall()
                for i in myresult:
                    # print(i,type(i))
                    k = k + 1
                    mycursor = mydb1.cursor()
                    sql = "select photo_link from student_info where Reg_no=%s"
                    value_reg = (i[1],)
                    mycursor.execute(sql, value_reg)
                    myresult_photo_link = mycursor.fetchall()
                    mymembers = {}
                    mymembers['id'] = k
                    mymembers['reg'] = i[1]
                    mymembers['filename'] = i[2]
                    mymembers['file_type'] = i[3]
                    mymembers['link'] = i[4]
                    mymembers['photo_link'] = myresult_photo_link[0][0]
                    subjects_list.append(mymembers)
            sub = {}
            sub['value'] = branch.upper()
            b_name = []
            b_name.append(sub)
            context = {'mymembers': list_members, 'students_files': subjects_list, 'branch_name': b_name}
            return HttpResponse(template.render(context, request))
        elif check == 1:
            return HttpResponse("Already one user is active at the same time")
        else:
            return HttpResponseRedirect(reverse('firstreg'))
    except:
        print("cse exception")
        template = loader.get_template('somethingwentwrong.html')
        return HttpResponse(template.render())


def my_files(request):
    try:
        check = check_status(request)
        if check == 2:
            c_value = filter_data(request, request.COOKIES['userid'])
            mycursor = mydb.cursor()
            sql = "select regno from cookie where cookievalue=%s"
            value = (c_value,)
            mycursor.execute(sql, value)
            myresult = mycursor.fetchall()
            template = loader.get_template('my_files.html')
            mycursor = mydb1.cursor()
            sql = "select * from apporved_files where regno=%s"
            values = (myresult[0][0],)
            mycursor.execute(sql, values)
            myresult = mycursor.fetchall()
            list_members = []
            delete_requested_list = []
            k = 0
            t = 0
            for i in myresult:
                if i[10] == 1:
                    k = k + 1
                    mymembers = {}
                    mymembers['id'] = k
                    mymembers['filename'] = i[2]
                    mymembers['file_type'] = i[3]
                    mymembers['link'] = i[4]
                    mymembers['subject'] = i[5]
                    list_members.append(mymembers)
                else:
                    mycursor = mydb.cursor()
                    sql = "select comments from deletion_requests where filename=%s"
                    values = (i[2],)
                    mycursor.execute(sql, values)
                    myresult = mycursor.fetchall()
                    t = t + 1
                    mymembers = {}
                    mymembers['id'] = t
                    mymembers['filename'] = i[2]
                    mymembers['file_type'] = i[3]
                    mymembers['link'] = i[4]
                    mymembers['subject'] = i[5]
                    mymembers['comment'] = myresult[0][0]
                    delete_requested_list.append(mymembers)
            context = {'mymembers': list_members, 'delete_requested': delete_requested_list}
            return HttpResponse(template.render(context, request))
        else:
            print("myfiles condition exception")
            return HttpResponseRedirect(reverse('firstreg'))
    except:
        print("myfiles exception")
        template = loader.get_template('somethingwentwrong.html')
        return HttpResponse(template.render())


def requested_userprofile(request, regno):
    try:
        if check_status(request) == 2:
            template = loader.get_template('requested_profile.html')
            mycursor = mydb1.cursor()
            sql = "select * from student_info where Reg_no=%s"
            value = (regno,)
            mycursor.execute(sql, value)
            myresult = mycursor.fetchall()
            list_members = []
            for i in myresult:
                mymembers = {}
                mymembers['reg_no'] = i[1]
                mymembers['name'] = i[2]
                mymembers['mail'] = i[4]
                mymembers['link'] = i[5]
                list_members.append(mymembers)
            context = {'mymembers': list_members}
            return HttpResponse(template.render(context, request))
        else:
            return HttpResponseRedirect(reverse('firstreg'))
    except:
        print("requested userprofile exception")
        template = loader.get_template('somethingwentwrong.html')
        return HttpResponse(template.render())


def delete_requests(request, filename):
    if check_status(request) == 2:
        template = loader.get_template('delete_requests.html')
        return HttpResponse(template.render())
    else:
        print("delete-requests condition exception")
        template = loader.get_template('somethingwentwrong.html')
        return HttpResponse(template.render())


def raise_deletion_requests(request,filename):
    if check_status(request) == 2:
        comment=filter_data(request, request.POST['comment'])
        mycursor = mydb.cursor()
        sql = "insert into deletion_requests(filename,comments,datetime) values (%s,%s,%s)"
        values = (filename, comment, datetime.datetime.now())
        mycursor.execute(sql, values)
        mydb.commit()
        mycursor = mydb1.cursor()
        sql = "update apporved_files set enable=0 where file_name=%s"
        values = (filename,)
        mycursor.execute(sql, values)
        mydb1.commit()
        return HttpResponseRedirect(reverse('my_files'))
    else:
        print("raise deletion request exception")
        return HttpResponseRedirect(reverse('firstreg'))


def user_logout(request):
    returned_cookie = filter_data(request, request.COOKIES['userid'])
    mycursor = mydb.cursor()
    sql = "select regno from cookie where cookievalue=%s"
    values = (returned_cookie,)
    mycursor.execute(sql, values)
    myresult = mycursor.fetchall()
    sql = "delete from cookie where cookievalue=%s"
    mycursor.execute(sql, values)
    mydb.commit()
    print(myresult, "from userlogout")
    try:
        print("alin deletion")
        # c_value_alin = filter_data(request, request.COOKIES['Alin'])
        mycursor = mydb.cursor()
        sql = "delete from alreadylogin where reg=%s"
        value = (myresult[0][0],)
        mycursor.execute(sql, value)
        mydb.commit()
    except:
        print("exception occured in user logout, c_value_alin")
    try:
        print("fwist deletion")
        # c_value_fwist = filter_data(request, request.COOKIES['fwist'])
        mycursor = mydb.cursor()
        sql = "delete from first_visit where reg=%s"
        value = (myresult[0][0],)
        mycursor.execute(sql, value)
        mydb.commit()
    except:
        print("exception occured in user logout, c_value_fwist")
    print(myresult[0][0], "--logged out")
    return HttpResponseRedirect(reverse('already_login_once'))


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
                mymembers['link'] = i[5]
                list_members.append(mymembers)
            context = {'mymembers': list_members}
            return HttpResponse(template.render(context, request))
        else:
            return HttpResponseRedirect(reverse('course'))
    except:
        print("user profile exception")
        return HttpResponseRedirect(reverse('firstreg'))


def userinp(request):
    t = check_status(request)
    if t == 2:
        template = loader.get_template('userfiles.html')
        return HttpResponse(template.render())
    else:
        return HttpResponseRedirect(reverse('course'))


def userfileinp(request):
    try:
        file_name = filter_data(request, request.POST['filename'])
        subject = request.POST['sub']
        file_type = request.POST['file_type']
        link = request.POST['link']
        comment = filter_data(request, request.POST['comment'])
        if comment == "Explain something about the file._optional_":
            comment = None
        t = check_status(request)
        if t == 2:
            regis = return_reg(request)
            if regis != '0':
                mycursor = mydb1.cursor()
                sql = "select sec from student_info where reg_no=%s"
                value = (regis,)
                mycursor.execute(sql, value)
                myresult = mycursor.fetchall()
                sec = myresult[0][0]
                date = datetime.datetime.now()
                cursor1 = mydb1.cursor()
                sql = "insert into userlinks(reg, sec, filename, file_type, link, datetime,subject,comment) values(%s,%s,%s,%s,%s,%s,%s,%s)"
                values = (regis, sec, file_name, file_type, link, date, subject, comment)
                cursor1.execute(sql, values)
                mydb1.commit()
                return HttpResponseRedirect(reverse('course'))
            else:
                return HttpResponse('Something went wrong when writing to database')
    except:
        print("user file input exception")
        return HttpResponse("Can't take file now")


def return_reg(request):
    c_value = filter_data(request,request.COOKIES['userid'])
    ip = get_ip(request)
    mycursor = mydb.cursor()
    sql = "select * from cookie where cookievalue=%s"
    value=(c_value,)
    mycursor.execute(sql, value)
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
        print("ok")
        name = filter_data(request, request.POST['name'])
        reg = filter_data(request, request.POST['reg'])
        pswd = request.POST['password1']
        confirm_pswd = request.POST['password2']
        email = filter_data(request, request.POST['mail'])
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
            print(i, k)
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
        print("creating exception")
        return HttpResponseRedirect(reverse('firstreg'))


def faculty(request):
    template = loader.get_template('facultyaccess.html')
    return HttpResponse(template.render({}, request))


def facultyaccess(request):
    try:
        if request.method == "POST":
            facultyid = filter_data(request, request.POST['facultyid'])
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
                        t = dup_fac(request, facultyid)
                        if t == 0:
                            fac_ip = get_ip(request)
                            cook = Cookies()
                            cookie_value = cook.makecookie()
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
                            return HttpResponseRedirect("pdf_links")
                    else:
                        return HttpResponse("Wrong password !!!")
                elif k == len(myresult):
                    return HttpResponse("No account found !!!")
        else:
            return HttpResponseRedirect(reverse("faculty"))
    except:
        print("faculty access exception")
        return HttpResponseRedirect(reverse('faculty'))


def pdf_links(request):
    try:
        print('pdf-link')
        t=faculty_auth(request, 1)
        if t != 0:
            template = loader.get_template('pdf_links.html')
            mycursor = mydb1.cursor()
            sql = "select * from links_provided where faculty_id=%s"
            values = (t, )
            mycursor.execute(sql, values)
            myresult = mycursor.fetchall()
            list_members = []
            k = 0
            for i in myresult:
                k = k + 1
                mymembers = {}
                mymembers['id'] = k
                mymembers['filename'] = i[2]
                mymembers['link'] = i[3]
                mymembers['branch'] = i[4]
                mymembers['file_type'] = i[5]
                list_members.append(mymembers)
            context = {'mymembers': list_members}
            return HttpResponse(template.render(context, request))
        else:
            return HttpResponseRedirect(reverse('faculty'))
    except:
        print("pdf links exception")
        return HttpResponseRedirect(reverse("faculty"))


def delete(request, filename):
    try:
        t = faculty_auth(request, 0)
        if t == 2:
            print(filename)
            mycursor = mydb1.cursor()
            sql = "delete from links_provided where file_name=%s"
            value = (filename, )
            mycursor.execute(sql, value)
            mydb1.commit()
            return HttpResponseRedirect(reverse('pdf_links'))
        else:
            return HttpResponseRedirect(reverse('faculty'))
    except:
        print("delete file exception")
        return HttpResponseRedirect(reverse('faculty'))


def add(request):
    template = loader.get_template('addlink.html')
    return HttpResponse(template.render({}, request))


def addlink(request):
    try:
        t = faculty_auth(request, 1)
        if t != 0:
            filename_to_upload = filter_data(request, request.POST['filename'])
            file_type = filter_data(request, request.POST['file_type'])
            link_to_upload = request.POST['dlink']
            branch = filter_data(request, request.POST['branch'])
            print(file_type, branch)
            mycursor = mydb1.cursor()
            sql = "select * from links_provided where file_name=%s"
            value = (filename_to_upload,)
            mycursor.execute(sql, value)
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
            value = (t, filename_to_upload, link_to_upload, branch, file_type, date, fac_name)
            mycursor.execute(sql, value)
            mydb1.commit()
            return HttpResponseRedirect(reverse('pdf_links'))
        else:
            return HttpResponseRedirect(reverse('faculty'))
    except:
        print('add link exception')
        return HttpResponse('Problem occurred.Try logout and login again')


def fac_logout(request):
    returned_cookie = request.COOKIES['sessionid']
    mycursor = mydb.cursor()
    sql = "delete from active_users where cookie=%s"
    values = (returned_cookie,)
    mycursor.execute(sql, values)
    mydb.commit()
    print("logged out")
    return HttpResponseRedirect(reverse('firstreg'))


def faculty_auth(request, enable):
    try:
        c_value = request.COOKIES['sessionid']
        print(c_value)
        mycursor = mydb.cursor()
        sql = "select * from active_users where cookie=%s"
        value=(c_value,)
        mycursor.execute(sql, value)
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
        print('faculty auth exception')
        return 0


def dup_fac(request, fac_id):
    try:
        ip = get_ip(request)
        mycursor = mydb.cursor()
        sql = "select * from active_users where faculty_id=%s"
        value=(fac_id,)
        mycursor.execute(sql, value)
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
        print('faculty dup fac exception')
        return 0


def requestings(request):
    try:
        print('requestings')
        t=faculty_auth(request, 1)
        if t != 0:
            mycursor = mydb1.cursor()
            sql = "select sec,subject from assigned_sections where fac_id=%s"
            val=(t,)
            mycursor.execute(sql, val)
            myresult_of_a_s = mycursor.fetchall()
            template = loader.get_template('requestings.html')
            mycursor = mydb1.cursor()
            list_members = []
            k = 0
            for faculty_data in myresult_of_a_s:
                sql = "select * from userlinks where sec=%s and subject=%s"
                value = (faculty_data[0], faculty_data[1])
                mycursor.execute(sql, value)
                myresult = mycursor.fetchall()
                for i in myresult:
                    k = k + 1
                    mymembers = {}
                    mymembers['id'] = k
                    mymembers['reg'] = i[1]
                    mymembers['filename'] = i[3]
                    mymembers['file_type'] = i[4]
                    mymembers['link'] = i[5]
                    mymembers['subject'] = i[7]
                    mymembers['comment'] = i[8]
                    list_members.append(mymembers)
            context = {'mymembers': list_members}
            return HttpResponse(template.render(context, request))
        else:
            return HttpResponseRedirect(reverse('faculty'))
    except:
        print('requestings exception')
        return HttpResponseRedirect(reverse("faculty"))


def apporve(request, filename):
    try:
        t = faculty_auth(request,1)
        mycursor = mydb1.cursor()
        sql = "select * from userlinks where filename=%s"
        value = (filename,)
        mycursor.execute(sql, value)
        myresult = mycursor.fetchall()
        i = myresult[0]
        fac_comment = None
        statement = "insert into apporved_files(regno,file_name,file_type,file_link,subject,stu_comment,apporved_by,fac_comment,datetime) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        values = (i[1], filename, i[4], i[5], i[7], i[8], t, fac_comment, datetime.datetime.now())
        mycursor.execute(statement, values)
        mydb1.commit()
        sql = "delete from userlinks where filename=%s"
        value = (filename,)
        mycursor.execute(sql, value)
        mydb1.commit()
        print(type(i[1]), type(filename), type(i[5]), type(t), type(t))
        send = Mail()
        send.statusmail(i[1], filename, i[5], fac_comment, t, 1)
        return HttpResponseRedirect(reverse('requestings'))
    except:
        print('apporve exception')
        return HttpResponse('Problem occurred when approving file Try logout and login again')


def decline(request, filename):
    try:
        t = faculty_auth(request, 1)
        mycursor = mydb1.cursor()
        sql = "select * from userlinks where filename=%s"
        value = (filename,)
        mycursor.execute(sql, value)
        myresult = mycursor.fetchall()
        i = myresult[0]
        fac_comment = None
        statement = "insert into declined_files(regno,file_name,file_type,file_link,subject,stu_comment,declined_by,fac_comment,datetime) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        values = (i[1], filename, i[4], i[5], i[7], i[8], t, fac_comment, datetime.datetime.now())
        mycursor.execute(statement, values)
        mydb1.commit()
        sql = "delete from userlinks where filename=%s"
        value = (filename,)
        mycursor.execute(sql, value)
        mydb1.commit()
        send = Mail()
        send.statusmail(i[1], filename, i[5], fac_comment, t, 0)
        return HttpResponseRedirect(reverse('requestings'))
    except:
        print('decline exception')
        return HttpResponse('Problem occurred when declining the file. Try logout and login again.')


def comment_section(request,filename):
    print(filename)
    template = loader.get_template('comment_section.html')
    return HttpResponse(template.render({}, request))


def add_comment(request, filename):
    try:
        comment = filter_data(request, request.POST['comment'])
        status = request.POST['radio']
        if comment == "Write your suggestions here._optional_":
            comment = None
        t = faculty_auth(request, 1)
        mycursor = mydb1.cursor()
        sql = "select * from userlinks where filename=%s"
        value = (filename,)
        mycursor.execute(sql, value)
        myresult = mycursor.fetchall()
        i = myresult[0]
        if status == "apporve":
            statement = "insert into apporved_files(regno,file_name,file_type,file_link,subject,stu_comment,apporved_by,fac_comment,datetime) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            values = (i[1], filename, i[4], i[5], i[7], i[8], t, comment, datetime.datetime.now())
            mycursor.execute(statement, values)
            mydb1.commit()
            sql = "delete from userlinks where filename=%s"
            value = (filename,)
            mycursor.execute(sql, value)
            mydb1.commit()
            print(type(i[1]), type(filename), type(i[5]), type(t), type(t))
            send = Mail()
            send.statusmail(i[1], filename, i[5], comment, t, 1)
        else:
            statement = "insert into declined_files(regno,file_name,file_type,file_link,subject,stu_comment,declined_by,fac_comment,datetime) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            values = (i[1], filename, i[4], i[5], i[7], i[8], t, comment, datetime.datetime.now())
            mycursor.execute(statement, values)
            mydb1.commit()
            sql = "delete from userlinks where filename=%s"
            value = (filename,)
            mycursor.execute(sql, value)
            mydb1.commit()
            send = Mail()
            send.statusmail(i[1], filename, i[5], comment, t, 0)
        return HttpResponseRedirect(reverse('requestings'))
    except:
        print('add comment exception')
        return HttpResponse('Problem occurred when adding the comment. Try logout and login again')


def mail_checking(request):
    template = loader.get_template('mail_checking.html')
    return HttpResponse(template.render({}, request))


def comparing_mail(request):
    try:
        mail = filter_data(request, request.POST['mail'])
        reg = filter_data(request, request.POST['reg'])
        choice = request.POST['choice']
        reg = reg.upper()
        print("Entered mail :", mail, "Reg.no", reg)
        my_cursor = mydb.cursor()
        sql = "delete from active_otps where reg=%s"
        value = (reg,)
        my_cursor.execute(sql, value)
        mydb.commit()
        sql = "delete from passwordlink where regno=%s"
        value = (reg,)
        my_cursor.execute(sql, value)
        mydb.commit()
        mycursor = mydb1.cursor()
        sql = "select * from student_info where reg_no=%s"
        val = (reg,)
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()
        print("choice",choice)
        ip = get_ip(request)
        if len(myresult) != 0:
            i = myresult[0]
            if i[4] == mail:
                print("correct mail entered")
                if choice == 'link':
                    value = linkcreation(i[4], reg, i[2], ip)
                    if value:
                        return HttpResponseRedirect(reverse('firstreg'))
                    else:
                        template = loader.get_template('somethingwentwrong.html')
                        return HttpResponse(template.render())
                send = Mail()
                otp = str(send.sendingotp(i[4], i[2], i[3]))
                if otp == 0:
                    template = loader.get_template('somethingwentwrong.html')
                    return HttpResponse(template.render())
                print("sent otp:", otp)
                date = datetime.datetime.now()
                cook = Cookies()
                cookie_value = cook.makecookie()
                mycursor = mydb.cursor()
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
    except:
        print('comparing mail exception')
        template = loader.get_template('somethingwentwrong.html')
        return HttpResponse(template.render())


def updating_password(request):
    template = loader.get_template('updating_password.html')
    return HttpResponse(template.render({}, request))


def importing_password(request):
    try:
        enotp = filter_data(request, request.POST['otp'])
        pswd = request.POST['password1']
        repswd = request.POST['password2']
        mycursor = mydb.cursor()
        web_cookie = request.COOKIES['tcookie']
        sql = "select * from active_otps where cookie=%s"
        value = (web_cookie,)
        mycursor.execute(sql, value)
        myresult = mycursor.fetchall()
        if len(myresult) != 0:
            i = myresult[0]
            reg_from_db = i[1]
            otp_from_db = i[2]
            if enotp == otp_from_db:
                print("OTP confirmation success")
                print(pswd, repswd)
                if pswd != repswd:
                    print("password confirmation failed")
                    return HttpResponse("Password confirmation failed !!!")
                else:
                    mycursor = mydb1.cursor()
                    sql = "update student_info set PassWord=%s where reg_no=%s"
                    values = (pswd, reg_from_db)
                    mycursor.execute(sql, values)
                    mydb1.commit()
                    print("password updated")
                    my_cursor = mydb.cursor()
                    sql = "delete from active_otps where reg=%s"
                    value = (reg_from_db, )
                    my_cursor.execute(sql, value)
                    mydb.commit()
                    return HttpResponseRedirect(reverse('firstreg'))
            else:
                mycursor = mydb.cursor()
                sql = "update active_otps set limit=%s where reg=%s"
                values = (i[6]+1, reg_from_db)
                mycursor.execute(sql, values)
                mydb.commit()
                print("OTP confirmation failed")
                return HttpResponse("wrong OTP entered !!!")
        else:
            return HttpResponse('<h2>OTP expired !!!</h2>')
    except:
        template = loader.get_template('somethingwentwrong.html')
        return HttpResponse(template.render())


def linkcreation(mail, number, name, ip):
    try:
        cook = Cookies()
        cookie_value = cook.makecookie()
        hosting = socket.gethostname()
        ipaddress = socket.gethostbyname(hosting)
        link = 'http://' + ipaddress + ':8000/project/reset-password/' + cookie_value
        send = Mail()
        send.sendinglink(mail, name, link)
        mycursor = mydb.cursor()
        sql = "insert into passwordlink (regno,link,ip,datetime) values (%s,%s,%s,%s)"
        values = (number, cookie_value, ip, datetime.datetime.now())
        mycursor.execute(sql, values)
        mydb.commit()
        return True
    except:
        print("exception occured in link-creation")
        return False
    

def linkpasswordpage(request, link):
    template = loader.get_template('passwordlink.html')
    return HttpResponse(template.render())


def linktype(request, link):
    try:
        pswd = request.POST['password1']
        repswd = request.POST['password2']
        mycursor = mydb.cursor()
        sql = "select * from passwordlink where link=%s"
        value = (link,)
        mycursor.execute(sql, value)
        myresult = mycursor.fetchall()
        if len(myresult) != 0:
            i = myresult[0]
            reg_form_db = i[1]
            link_from_db = i[2]
            if link == link_from_db:
                print("Link confirmation success")
                print(pswd, repswd)
                if pswd != repswd:
                    print("password confirmation failed")
                    return HttpResponse("Password confirmation failed !!!")
                else:
                    mycursor = mydb1.cursor()
                    sql = "update student_info set PassWord=%s where reg_no=%s"
                    values = (pswd, reg_form_db)
                    mycursor.execute(sql, values)
                    mydb1.commit()
                    print("password updated")
                    my_cursor = mydb.cursor()
                    sql = "delete from passwordlink where regno=%s"
                    value = (reg_form_db, )
                    my_cursor.execute(sql, value)
                    mydb.commit()
                    return HttpResponseRedirect(reverse('firstreg'))
            else:
                print("link confirmation failed")
                template = loader.get_template('somethingwentwrong.html')
                return HttpResponse(template.render())
        else:
            template = loader.get_template('somethingwentwrong.html')
            return HttpResponse(template.render())
    except:
        print('exception occured in link-type')
        template = loader.get_template('somethingwentwrong.html')
        return HttpResponse(template.render())



def newadmin(request):
    template = loader.get_template('newadmin.html')
    return HttpResponse(template.render({}, request))


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
    arr = ['`', '!', '#', '$', '%', '^', '&', '*', '(', ')', '+', '=', '/', '<', '>', '|', '?', '~', 'script', '"',
           "'", ';', ':']
    for i in word:
        if i in arr:
            word = word.replace(i, "_")
    return word
