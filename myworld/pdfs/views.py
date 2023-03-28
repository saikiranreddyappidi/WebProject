import datetime
import socket

from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.template import TemplateDoesNotExist, loader
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
    try:
        template = loader.get_template('home.html')
    except TemplateDoesNotExist:
        return HttpResponseNotFound('<h1>Sorry, page not found</h1>')
    return HttpResponse(template.render())


"""get_reg function to get the registration number from the database"""


def get_reg(c_value):
    print("get_reg")
    mycursor = mydb1.cursor()
    sql = "select reg from assigned_cookies where cookies=%s"
    value = (c_value,)
    mycursor.execute(sql, value)
    myresult = mycursor.fetchall()
    print(myresult)
    return myresult


"""
1. First the function is called when the user visits the page for the first time.
2. It first gets the IP address of the user.
3. It then loads the template for the first visit.
4. It then creates a cookie and sets the value of the cookie to "fwist" and the value of the cookie to the value of the cookie created by the makecookie() function.
5. It then checks if the cookie "userid" exists or not. If it exists, it then checks if the cookie value is present in the database or not. If the cookie value is present in the database, it then checks if the cookie value is equal to 0. If the cookie value is not equal to 0, it then returns the user to the page "already_login_once" and if the cookie value is equal to 0, then it then returns the user to the page "first.html" and if the cookie "userid" is not present, then it then returns the user to the page "first.html"
6. It then catches any exceptions that might have occured during the process and then returns the user to the page "first.html"
"""


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
    except Exception as e:
        print(e, 'exception occured in firstreg')
        mycursor = mydb.cursor()
        sql = "insert into first_visit(cookie,ip,datetime) values(%s, %s, %s)"
        values = (cookie_value, ip, datetime.datetime.now())
        mycursor.execute(sql, values)
        mydb.commit()
        return cookie


"""
1. The function newlogin() takes a request as its parameter.
2. The newlogin() function calls the get_ip() function to get the ip address of the user.
3. The newlogin() function loads the html file newlogin.html and creates a template out of it.
4. The newlogin() function creates a cookie using the makecookie() function in the Cookies class.
5. The newlogin() function then sets the cookie for the user.
6. The newlogin() function then inserts the cookie value and ip address of the user into a database.
7. The newlogin() function returns the cookie to the user. 
"""


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


"""
1. First we check if the user has logged in previously or not. If he has logged in previously, then we check if he has logged in once or multiple times.
2. If the user has logged in previously, we get his reg_no from the database and check if he has logged in once or multiple times.
3. If the user has logged in once, then we check the cookie value in the database.
4. If the cookie value in the database matches the cookie value in the browser, then we simply render the already_login_once.html page and set the cookie value for the user.
5. If the cookie value in the database does not match the cookie value in the browser, then we render the already_login_once.html page and set a new cookie value for the user.
6. If the user has logged in multiple times, then we get the cookie value from the database and check if it matches the cookie value in the browser.
7. If the cookie value in the database matches the cookie value in the browser, then we simply render the already_login_once.html page and set the cookie value for the user.
8. If the cookie value in the database does not match the cookie value in the browser, then we render the already_login_once.html page and set a new cookie value for the user.
9. We also store the cookie value in the database to check for multiple logins.
10. We also store the IP address of the user in the database. 
"""


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
    except Exception as e:
        print(e, "exception occured in already login once")
        return HttpResponseRedirect(reverse('firstreg'))


"""
1. I am trying to get the cookie from the request object. If the cookie is not present then it will go to except block.
2. If the cookie is present then it will check the cookie value from the database.
3. If the cookie value is present then it will redirect to the alreadylogin page.
4. In the alreadylogin page, if the user clicks the submit button then it will go to the POST method.
5. In the POST method, I am trying to get the password from the request object.
6. Then I am trying to get the reg value from the database using the cookie value.
7. Then I am trying to insert the password and reg value into the testing table.
8. Then I am trying to get the password and reg value from the request object.
9. Then I am trying to check the password value from the database.
10. If the password value is present then it will redirect to the redirection page.
11. If the password value is not present then it will redirect to the newlogin page. 
"""


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
    except Exception as e:
        print(e, "exception occurred in already-login")
        return HttpResponseRedirect(reverse('newlogin'))


"""
1. In the first function, the user has to enter his/her registration number and password.
2. The registration number is stored in the variable reg and the password is stored in pswd.
3. The reg variable is then converted to upper case.
4. The reg and pswd variables are then passed to the search function which returns 0 if the user has no account, 1 if the password is wrong and 2 if the user has an account.
5. If the user has an account, the cookie is updated so that the user is directed to the redirection function.
6. If the user has no account, the user is directed to the firstreg function which displays a page to the user to enter his/her registration number and password.
7. If the user has an account but the password is wrong, the user is directed to the firstreg function where he/she can enter the correct password.
8. If there is a problem with the server, the user is directed to the firstreg function.
"""


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
    except Exception as e:
        print(e, "exception occured in first")
        return HttpResponseRedirect(reverse('firstreg'))


'''
1. Get the request object from the user
2. Get the template loader
3. Create a cookie
4. Try to get the cookie from the Alin course
5. If the cookie is present, then extract the regnum from the cookie and check if the user is logged in
6. If the user is logged in, then assign the cookie to the user
7. If the user is not logged in, then assign a new cookie to the user
8. If the cookie is not present, then get the cookie from the fwist course
9. If the cookie is present, then extract the regnum from the cookie and assign the cookie to the user
10. If the cookie is not present, then return an error page
'''


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
    except Exception as e:
        print(e, "redirection exception")
        template = loader.get_template('somethingwentwrong.html')
        return HttpResponse(template.render())


"""
1. First we check if the user is logged in or not. If not, then we redirect them to the first page of the website.
2.  If the user is logged in, then we check if they are the only one logged in at the same time. If not, then we redirect them to the first page of the website.
3.  If the user is the only one logged in at the same time, then we render the course.html template and return it to the user.
"""


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
    except Exception as e:
        print(e, "course exception")
        return HttpResponseRedirect(reverse('firstreg'))


"""To avoid multiple logins at the same time
1. I'm checking if the user is logged in and if so, I'm checking if the user is logged in from another device.
2. If the user is logged in from another device, I'm deleting the cookie from the database.
3. Then, I'm creating a new cookie and redirecting the user to the homepage.
4. If the user is not logged in from another device, I'm just creating a new cookie and redirecting the user to the homepage. 
"""


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
        mydb.commit()
        try:
            print("fwist deletion")
            # c_value_fwist = filter_data(request, request.COOKIES['fwist'])
            mycursor = mydb.cursor()
            sql = "delete from first_visit where reg=%s"
            value = (myresult[0][0],)
            mycursor.execute(sql, value)
            mydb.commit()
        except Exception as e:
            print(e, "exception occured in user response, c_value_fwist")
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
    except Exception as e:
        print(e, "user response exception")
        template = loader.get_template('somethingwentwrong.html')
        return HttpResponse(template.render())


"""
1. Here we are checking the status of the user. If the user is logged in and has a cookie value, we are checking for the value of the cookie in the database.
2. If the value of the cookie is present in the database, we are checking for the IP address of the user.
3. If the IP address of the user is the same as the one in the database, we are returning 2, which means the user is logged in.
4. If the IP address of the user is different than the one in the database, we are returning 1, which means the user has logged in from a different IP address.
5. If the value of the cookie is not present in the database, we are returning 0, which means the user is not logged in. 
"""


def check_status(request):
    try:
        c_value = filter_data(request, request.COOKIES['userid'])
        ip = get_ip(request)
        mycursor = mydb.cursor()
        sql = "select * from cookie where cookievalue=%s"
        value = (c_value,)
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
    except Exception as e:
        print(e, "chck-stat exception")
        return 0


"""
1. The function receives a request and a registration number
2. If the registration number is '00', it returns 0
3. The code then creates a cursor and executes a select statement to find the registration number in the database
4. If the registration number is found, it returns 3
5. If the registration number is not found, it returns 1
6. If there is any exception, it returns 0 
"""


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


"""
1. First we are checking if the user is already logged in or not. If the user is already logged in then we will show the cse.html page to the user.
2. If the user is not logged in then we will redirect the user to the firstreg.html page.
3. If the user is already logged in and he is trying to log in again then we will show a message that "Already one user is active at the same time".
4. In the cse.html page we are showing the files and links provided by the faculty of that particular branch.
5. We are also showing the link files uploaded by the students of that particular branch.
6. For the link files uploaded by the students we are also showing the image of the student. 
"""


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
    except Exception as e:
        print(e, "cse exception")
        template = loader.get_template('somethingwentwrong.html')
        return HttpResponse(template.render())


"""
1. It checks the status of the user
2. If the status is 2, it means that the user is logged in
3. If the status is 2, it fetches the cookie value and regno of the user
4. It fetches the list of files which has been approved and the list of files which has been requested for deletion
5. It renders the my_files.html page with the lists of files which has been approved and the list of files which has been requested for deletion 
"""


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
    except Exception as e:
        print(e, "myfiles exception")
        template = loader.get_template('somethingwentwrong.html')
        return HttpResponse(template.render())


"""
1. Here we are checking the status of the user. If the user is logged in then we will return the requested user profile page. Otherwise, we will redirect the user to the first registration page.
2. Here we are fetching the requested user profile data from the database and storing them in a list.
3. We are rendering the requested user profile page with the list of requested user profile data. 
"""


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
    except Exception as e:
        print("requested userprofile exception")
        template = loader.get_template('somethingwentwrong.html')
        return HttpResponse(template.render())


"""
1. We are importing the required modules.
2. We are creating a function named delete_requests which takes two arguments request and filename.
3. We are checking the status of the request using the check_status function.
4. If the status is 2 we are loading the template delete_requests.html and returning the response.
5. If the status is not 2 we are loading the template somethingwentwrong.html and returning the response. 
"""


def delete_requests(request, filename):
    if check_status(request) == 2:
        template = loader.get_template('delete_requests.html')
        return HttpResponse(template.render())
    else:
        print("delete-requests condition exception")
        template = loader.get_template('somethingwentwrong.html')
        return HttpResponse(template.render())


""" 
The function raise_deletion_requests() is called when a user submits a deletion request for a file. 
The function gets the filename from the URL and a comment from the user. 
It then inserts the filename, the comment and the current date into the deletion_requests table in the database. 
It also disables the file in the apporved_files table so that the file is no longer listed in the my_files page. 
"""


def raise_deletion_requests(request, filename):
    if check_status(request) == 2:
        comment = filter_data(request, request.POST['comment'])
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


"""
1. This function is called when the user wants to log out.
2. The cookie is filtered and stored in a variable.
3. Then the cookie value is checked in the database for the user.
4. If the cookie value is present, then the user is logged out.
5. A try-except block is used to check if the user has been logged in before.
6. If the user has been logged in before then the cookie is deleted from the database.
7. After that, the user is redirected to the already login once page. 
"""


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
    except Exception as e:
        print(e, "exeception occured in user logout, c_value_alin")
    try:
        print("fwist deletion")
        # c_value_fwist = filter_data(request, request.COOKIES['fwist'])
        mycursor = mydb.cursor()
        sql = "delete from first_visit where reg=%s"
        value = (myresult[0][0],)
        mycursor.execute(sql, value)
        mydb.commit()
    except Exception as e:
        print(e, "exception occured in user logout, c_value_fwist")
    print(myresult[0][0], "--logged out")
    return HttpResponseRedirect(reverse('already_login_once'))


"""
1. This function is used to display the user profile.
2. First we check whether the session is active or not.
3. If the session is active then we fetch the data from database and display it to the user.
4. If the session is not active then we redirect the user to the homepage. 
"""


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
    except Exception as e:
        print(e, "user profile exception")
        return HttpResponseRedirect(reverse('firstreg'))


def userinp(request):
    t = check_status(request)
    if t == 2:
        template = loader.get_template('userfiles.html')
        return HttpResponse(template.render())
    else:
        return HttpResponseRedirect(reverse('course'))


"""
1. The file is uploaded to the server
2. It is checked whether the student is registered in the database
3. If the student is registered, the file is saved to the database and the student is redirected to the course page. Otherwise, an error message is displayed. 
"""


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
    except Exception as e:
        print(e, "user file input exception")
        return HttpResponse("Can't take file now")


"""
1. If the cookie value and client ip address exist in the database then we are returning the registration number of the user.
2. If the cookie value and client ip address doesn't exist in the database then we are returning 0. 
"""


def return_reg(request):
    c_value = filter_data(request, request.COOKIES['userid'])
    ip = get_ip(request)
    mycursor = mydb.cursor()
    sql = "select * from cookie where cookievalue=%s"
    value = (c_value,)
    mycursor.execute(sql, value)
    myresult = mycursor.fetchall()
    if len(myresult) != 0:
        i = myresult[0]
        if i[2] == c_value and i[3] == ip:
            print("Check status ok--returning reg")
            return i[1]
    else:
        return 0


def createacnt(request):
    template = loader.get_template('createacnt.html')
    return HttpResponse(template.render())


""" 
It will create the user account by taking some basic information.
1. If the registration number and email already exists in the database then the user will be shown a message saying "Already account exits on this Registration.no and E-mail !!!".
2. If the registration number already exists in the database then the user will be shown a message saying "Already account exists on this Registration.No !!!".
3. If the email already exists in the database then the user will be shown a message saying "Already account exists on this E-mail.Use different one !!!".
4. If the registration number and email doesn't exist in the database then a new account will be created and the user will be redirected to the firstreg.html page."""


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
                values = (reg, name, pswd, email, link)
                mycursor.execute(sql, values)
                mydb1.commit()
                print("new account created")
                return HttpResponseRedirect(reverse('firstreg'))
    except Exception as e:
        print(e, "creating exception")
        return HttpResponseRedirect(reverse('firstreg'))


def faculty(request):
    template = loader.get_template('facultyaccess.html')
    return HttpResponse(template.render({}, request))


"""
1. This function is called when the faculty tries to login.
2. It checks if the faculty is already logged in or not.
3. If he is not logged in then it authenticates him and gives him access to the pdf links page.
4. It also stores his login details in the database. 
"""


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
                            cookie = HttpResponseRedirect("pdf_links")
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
    except Exception as e:
        print(e, "faculty access exception")
        return HttpResponseRedirect(reverse('faculty'))


"""
1. The function pdf_links is called when the user clicks on the pdf links
2. The function faculty_auth is called to authenticate the user.
3. The branch and file_type of the pdf links are fetched from the database and are displayed on the page.
"""


def pdf_links(request):
    try:
        print('pdf-link')
        t = faculty_auth(request, 1)
        if t != 0:
            template = loader.get_template('pdf_links.html')
            mycursor = mydb1.cursor()
            sql = "select * from links_provided where faculty_id=%s"
            values = (t,)
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
    except Exception as e:
        print(e, "pdf links exception")
        return HttpResponseRedirect(reverse("faculty"))


"""
1. The try-except block handles the exception if any.
2. The faculty_auth function is used to check if the user is logged in or not.
3. If the user is logged in then the filename is obtained and the query is executed to delete the row from the database. 
"""


def delete(request, filename):
    try:
        t = faculty_auth(request, 0)
        if t == 2:
            print(filename)
            mycursor = mydb1.cursor()
            sql = "delete from links_provided where file_name=%s"
            value = (filename,)
            mycursor.execute(sql, value)
            mydb1.commit()
            return HttpResponseRedirect(reverse('pdf_links'))
        else:
            return HttpResponseRedirect(reverse('faculty'))
    except Exception as e:
        print(e, "delete file exception")
        return HttpResponseRedirect(reverse('faculty'))


def add(request):
    template = loader.get_template('addlink.html')
    return HttpResponse(template.render({}, request))


"""
1. First we check whether the user is logged in or not. If logged in then check whether the user is a faculty or not. If the user is a faculty then we get the user id of the faculty.
2. Then we get the file name, the file type, drive link, branch and date of the file added.
3. We check whether the file name is already present or not. If it is not present then we add the details of the file into the database.
4. If the user is not a faculty then we redirect the user to the faculty login page.
"""


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
    except Exception as e:
        print(e, 'add link exception')
        return HttpResponse('Problem occurred.Try logout and login again')


"""For faculty logout.
1. We check if the cookie is in the database of active users
2. If it is, we delete it from the database
3. We redirect the user to the homepage 
"""


def fac_logout(request):
    returned_cookie = request.COOKIES['sessionid']
    mycursor = mydb.cursor()
    sql = "delete from active_users where cookie=%s"
    values = (returned_cookie,)
    mycursor.execute(sql, values)
    mydb.commit()
    print("logged out")
    return HttpResponseRedirect(reverse('firstreg'))


"""
1. Gets the sessionid cookie from the request
2. Checks if the cookie is present in the active_users table
3. If it is present, then the user is logged in
4. If it is not present, then the user is not logged in
5. The function also returns the id of the user, which can be used to fetch the details of the user 
"""


def faculty_auth(request, enable):
    try:
        c_value = request.COOKIES['sessionid']
        print(c_value)
        mycursor = mydb.cursor()
        sql = "select * from active_users where cookie=%s"
        value = (c_value,)
        mycursor.execute(sql, value)
        myresult = mycursor.fetchall()
        if len(myresult) != 0:
            i = myresult[0]
            print(i)
            if enable == 1:
                return i[1]
            else:
                return 2
        else:
            print("not logged in a-c-u")
            return 0
    except Exception as e:
        print(e, 'faculty auth exception')
        return 0


def dup_fac(request, fac_id):
    try:
        ip = get_ip(request)
        mycursor = mydb.cursor()
        sql = "select * from active_users where faculty_id=%s"
        value = (fac_id,)
        mycursor.execute(sql, value)
        myresult = mycursor.fetchall()
        print('d-f')
        if len(myresult) != 0:
            i = myresult[0]
            print(i)
            if i[1] == fac_id:
                print("One active user")
                return ip
        else:
            print("not logged in a-c-u")
            return 0
    except Exception as e:
        print(e, 'faculty dup fac exception')
        return 0


"""
1. If the user is a faculty, we are fetching the details of the sections assigned to the user from the database.
2. We are fetching the details of the files uploaded by the students for the sections assigned to the user from the database.
3. We are rendering the page with the details of the files uploaded by the students for the sections assigned to the faculty.
"""


def requestings(request):
    try:
        print('requestings')
        t = faculty_auth(request, 1)
        if t != 0:
            mycursor = mydb1.cursor()
            sql = "select sec,subject from assigned_sections where fac_id=%s"
            val = (t,)
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
    except Exception as e:
        print(e, 'requesting exception')
        return HttpResponseRedirect(reverse("faculty"))


"""
1. The function takes request and filename.
2. It uses faculty_auth to check if the user is a faculty and if he is a faculty, it returns the faculty id.
3. Then it fetches the filename from the database.
4. Then it inserts the file into the apporved_files table in the database.
5. Then it deletes the file from the userlinks table.
6. Then it sends a mail to the student to notify him that his file has been approved by the faculty. 
"""


def apporve(request, filename):
    try:
        t = faculty_auth(request, 1)
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
    except Exception as e:
        print(e, 'approve exception')
        return HttpResponse('Problem occurred when approving file Try logout and login again')


"""
1. This is a function that is used to decline the file that is requested by the student.
2. Then the function fetches the data from the database.
3. The declined file data is inserted into the declined_files table in the database.
4. The data is then deleted from the userlinks table in the database.
5. The statusmail() function is called to send the status of the file to the student.
6. The function returns the requestings view. """


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
    except Exception as e:
        print(e, 'decline exception')
        return HttpResponse('Problem occurred when declining the file. Try logout and login again.')


def comment_section(request, filename):
    print(filename)
    template = loader.get_template('comment_section.html')
    return HttpResponse(template.render({}, request))


"""
1. The add_comment() function is used to add the comment for the file that the faculty is viewing.
2. The function checks if the status of the file is apporved or declined.
3. If the status is apporved, it inserts the file details into the apporved_files table.
4. If the status is declined, it inserts the file details into the declined_files table.
5. The function returns the user to the requestings page. 
"""


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
    except Exception as e:
        print(e, 'add comment exception')
        return HttpResponse('Problem occurred when adding the comment. Try logout and login again')


def mail_checking(request):
    template = loader.get_template('mail_checking.html')
    return HttpResponse(template.render({}, request))


"""
1. The function takes the mail and reg.no from the form and compares it with the mail and reg.no of the user in the database.
2. If the mail and reg.no match then the user is sent a link to his/her mail or an otp is sent to the user through mail.
3. Whichever the user chooses the otp is sent to the database and the user is redirected to the updating_password page.
4. The user enters the otp and if it matches the otp in the database then the user is redirected to the updating password page.
5. If the user chooses the link option then a link is created and sent to the user's mail.
6. The link is created and the user is redirected to the updating password page. 
"""


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
        print("choice", choice)
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
    except Exception as e:
        print(e, 'comparing mail exception')
        template = loader.get_template('somethingwentwrong.html')
        return HttpResponse(template.render())


def updating_password(request):
    template = loader.get_template('updating_password.html')
    return HttpResponse(template.render({}, request))


"""
1. We are getting the OTP and password from the user.
2. We are getting the cookie from the user.
3. We are using the cookie to get the OTP and reg_no from the database.
4. We are checking whether the OTP entered by the user is same as the OTP in the database.
5. If the OTP entered by the user is same as the OTP in the database, then we are updating the password for that particular reg_no.
6. We are deleting the OTP from the database after the user successfully resets the password.
7. If the OTP entered by the user is wrong, then we are incrementing the limit by 1 in the database.
8. If the limit is greater than 5, then we are deleting the OTP from the database.
9. If the OTP is wrong and limit is less than 5, then we are re-directing the user to the same page.
10. If the OTP is wrong and limit is greater than 5, then we are deleting the OTP from the database and re-directing the user to the OTP expired page. 
"""


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
                    value = (reg_from_db,)
                    my_cursor.execute(sql, value)
                    mydb.commit()
                    return HttpResponseRedirect(reverse('firstreg'))
            else:
                mycursor = mydb.cursor()
                sql = "update active_otps set limit=%s where reg=%s"
                values = (i[6] + 1, reg_from_db)
                mycursor.execute(sql, values)
                mydb.commit()
                print("OTP confirmation failed")
                return HttpResponse("wrong OTP entered !!!")
        else:
            return HttpResponse('<h2>OTP expired !!!</h2>')
    except Exception as e:
        print(e, "exception occured in importing password")
        template = loader.get_template('somethingwentwrong.html')
        return HttpResponse(template.render())


"""
1. The linkcreation function receives the mail id, regno, name, and ip address of the user.
2. The function calls the makecookie method from the Cookies class to generate a random string.
3. The function uses the socket library to get the ip address of the server.
4. The function creates the link using the ip address and the random string.
5. The function calls the sendinglink method from the Mail class to send the link to the user.
6. The function uses the connection established to insert the link, regno, ip address, and date time into the passwordlink table.
7. The function returns True if the link is successfully sent to the user, else False. 
"""


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
    except Exception as e:
        print(e, "exception occured in link-creation")
        return False


def linkpasswordpage(request, link):
    template = loader.get_template('passwordlink.html')
    return HttpResponse(template.render())


"""
1. I am getting the link from the user and the passwords from the user.
2. I am fetching the data from the table passwordlink using the link sent to the user.
3. I am checking whether the link is correct or not.
4. If the link is correct, I am checking whether the passwords are correct or not.
5. If the passwords are correct, I am updating the password in the student_info table.
6. I am deleting the row from the passwordlink table.
7. I am redirecting the user to the firstreg page.
8. If the link is incorrect, I am redirecting the user to the somethingwentwrong page.
"""


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
                    value = (reg_form_db,)
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
    except Exception as e:
        print(e, 'exception occured in link-type')
        template = loader.get_template('somethingwentwrong.html')
        return HttpResponse(template.render())


"""
1. It first checks the request from the browser and checks whether the user is logged in or not by using return_reg() function.
2. If the user is logged in, it reads the file in the path given and checks whether the file is empty or not.
3. If the file is not empty, it loads the content from the file and  displays it in the creating_profile.html template.
4. If the file is empty, it loads the creating_profile.html template without any content. 
"""


def creating_profile(request):
    template = loader.get_template('creating_profile.html')
    regno = return_reg(request).upper().strip()
    if regno != 0:
        path = r"C:\Users\saiki\PycharmProjects\WebProject\myworld\pdfs\templates\profile\%s.html" % regno
        with open(path, 'r') as f:
            content = f.read().strip()
            f.close()
        if len(content) != 0:
            list_members = [{"cont": content}]
            context = {'ownContent': list_members}
            print(context, regno)
            return HttpResponse(template.render(context, request))
    return HttpResponse(template.render({}, request))


"""
1. The function takes in the request object.
2. The content is extracted from the request object.
3. The content is passed to the saving function which will save the data in the database.
4. If the content is saved successfully, the user is redirected to the page where he can create his profile.
5. Else the user is redirected to the somethingwentwrong page.
6. The exception is caught and the user is redirected to the somethingwentwrong page. 
"""


def saveOnly(request):
    try:
        content = request.POST['content']
        if saving(request, content):
            return HttpResponseRedirect(reverse('creating_profile'))
        else:
            template = loader.get_template('somethingwentwrong.html')
            return HttpResponse(template.render())
    except Exception as e:
        print(e, "exception occured in saveOnly")
        template = loader.get_template('somethingwentwrong.html')
        return HttpResponse(template.render())


def saveNleave(request):
    try:
        content = request.POST['content']
        if saving(request, content):
            return HttpResponseRedirect(reverse('course'))
        else:
            template = loader.get_template('somethingwentwrong.html')
            return HttpResponse(template.render())
    except Exception as e:
        print(e, "exception occured in saveNleave")
        template = loader.get_template('somethingwentwrong.html')
        return HttpResponse(template.render())


"""
In this function the HTML code entered by the user is saved in his corresponding file which is already created.
"""


def saving(request, text):
    try:
        text = text.strip()
        regno = return_reg(request)
        mycursor = mydb1.cursor()
        sql = "select * from html_content where regno=%s"
        value = (regno.upper(),)
        mycursor.execute(sql, value)
        myresult = mycursor.fetchall()
        path = r"C:\Users\saiki\PycharmProjects\WebProject\myworld\pdfs\templates\profile\%s.html" % regno
        with open(path, 'w') as f:
            f.write(text)
            f.close()
        if len(myresult) != 0:
            sql = "update html_content set content=%s,lastmodified=%s where regno=%s"
            values = (text, datetime.datetime.now(), regno)
            mycursor.execute(sql, values)
            mydb1.commit()
            return True
        else:
            sql = "insert into html_content (regno,content) values (%s,%s)"
            values = (regno, text)
            mycursor.execute(sql, values)
            mydb1.commit()
            return True
    except Exception as e:
        print(e, 'exception occured in saving')
        return False


"""
1. The function takes two arguments: request, regno
2. It then takes the regno and converts it to upper case and strips the white spaces
3. It then tries to load the profile page of the regno
4. If it fails, it loads the 404 page
5. If it succeeds, it loads the profile page of the regno and renders that page with this HTML code.
"""


def ownProfile(request, regno):
    regno = regno.upper().strip()
    try:
        template = loader.get_template('profile/%s.html' % regno)
        return HttpResponse(template.render({}, request))
    except Exception as e:
        print(e, "exception occured in ownProfile")
        template = loader.get_template('404.html')
        return HttpResponse(template.render({}, request))


def example_template(request):
    template = loader.get_template('Example.html')
    return HttpResponse(template.render({}, request))


def newadmin(request):
    template = loader.get_template('newadmin.html')
    return HttpResponse(template.render({}, request))


"""This function simply returns the IP address of the user's Computer when it is hit by a request from the user"""


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


def pagenotfound(request):
    template = loader.get_template('404.html')
    return HttpResponse(template.render({}, request))


def testing(request):
    template = loader.get_template('testing.html')
    return HttpResponse(template.render({}, request))


def fileinp(request):
    # name = request.POST['filename']
    fileinput = request.FILES['file']
    print(type(fileinput), fileinput)
    # cursor = mydb.cursor()
    # files = open(fileinp, 'rb').read()
    # files = base64.b64encode(files)
    # print(type(files), files)
    # args = (name, file)
    # query = 'INSERT INTO files(file_name,document) VALUES(%s, %s)'
    # cursor.execute(query, args)
    # mydb.commit()
    return HttpResponse('ok')


"""
1. The filter_data method is a function that takes in two parameters, the request and the word.
2. The method then creates a list of characters which it uses to check if the word contains any of them.
3. The code then goes through the word and checks if it contains any of the characters in the list.
4. If there is a character in the list, it will be replaced with an underscore.
5. If not, then the word is returned as it is. 
6. The method is called when server is taking information from the user.
7. The function then checks the username to see if it contains any of the characters in the list.
8. If it does, the character is replaced with an underscore.
9. If not, then the username is saved as it is.
10. This is done to prevent SQL injection attacks and avoid's running vunerable scripts in the server.
"""


def filter_data(request, word):
    arr = ['`', '!', '#', '$', '%', '^', '&', '*', '(', ')', '+', '=', '/', '<', '>', '|', '?', '~', 'script', '"',
           "'", ';', ':', 'select']
    for i in word:
        if i.lower() in arr:
            word = word.replace(i, "_")
    return word
