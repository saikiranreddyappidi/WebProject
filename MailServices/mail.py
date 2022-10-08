import math
import random
import smtplib
import mysql.connector
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

mydb1 = mysql.connector.connect(
	host="localhost",
	user="root",
	password="databasepassword",
	database="databasename"
)


class Mail:
	def statusmail(self, reg, filename, link, comments, fac_id, enable):
		try:
			mycursor = mydb1.cursor()
			sql = "select name,email from student_info where reg_no=%s"
			value = (reg,)
			mycursor.execute(sql, value)
			myresult = mycursor.fetchall()
			mycursor = mydb1.cursor()
			name = myresult[0][0]
			mail = myresult[0][1]
			sql = "select name from faculty where faculty_id=%s"
			value = (fac_id,)
			mycursor.execute(sql, value)
			myresult = mycursor.fetchall()
			smtp = smtplib.SMTP('smtp.gmail.com', 587)
			smtp.ehlo()
			smtp.starttls()
			smtp.login('developingproject7@gmail.com', 'lxezucynqaoeyijh')
			msg = MIMEMultipart()
			if enable == 1:
				subject = "Your file has been approved"
				msg['Subject'] = subject
				text1 = 'Hi ' + name + ',' + '\n' + '\n' + 'The file that you are uploaded has been verified by ' + \
				myresult[0][0] + '.' + '\n' + '\n'
				text2 = 'File name : ' + filename + '\n' + 'File link : ' + link + '\n'
				if comments != None:
					text2 += 'Faculty comments: ' + comments + '\n'
				text3 = '\n' + 'If you want to delete this uploaded file ,raise a request to delete the file in the pdfs website.'
				text4 = 'The concerned faculty will verify your request and the file may be deleted by that faculty.' + '\n' + '\n'
				text = text1 + text2 + text3 + text4 + 'Thank you,' + '\n' + 'Project Team.'
				print("apporval")
			else:
				subject = "Your file has been Declined"
				msg['Subject'] = subject
				text1 = 'Hi ' + name + ',' + '\n' + '\n' + 'The file that you are uploaded has been verified and declined by ' + \
				        myresult[0][0] + '.' + '\n' + '\n'
				text2 = 'File name : ' + filename + '\n' + 'File link : ' + link + '\n'
				if comments != None:
					text2 += 'Faculty comments: ' + comments + '\n'
				text3 = '\n' + 'You can again upload the file by correcting the mistakes that you have done.'
				text = text1 + text2 + text3 + 'Thank you,' + '\n' + 'Project Team.'
				print("decline")
			msg.attach(MIMEText(text))
			smtp.sendmail(from_addr="developingproject7@gmail.com", to_addrs=mail, msg=msg.as_string())
			smtp.quit()
			print("Mail sent")
			return True
		except:
			print('status mail exception')
			return True
	
	def sendingotp(self, mail, name, psawd):
		try:
			smtp = smtplib.SMTP('smtp.gmail.com', 587)
			smtp.ehlo()
			smtp.starttls()
			smtp.login('developingproject7@gmail.com', 'lxezucynqaoeyijh')
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
				hotp) + '\n' + "This otp will expires after 5 minutes" + "\n" + "\n"
			text2 = "If you didn't request this code, you can safely ignore this email. " \
			"Someone else might have typed your email address by mistake." + "\n" + "\n"
			text3 = "Thanks," + "\n" + '\n' + "The Project account team"
			text = text1 + text2 + text3
			msg.attach(MIMEText(text))
			to = [str(mail)]
			smtp.sendmail(from_addr="developingproject7@gmail.com", to_addrs=to, msg=msg.as_string())
			smtp.quit()
			print("Mail sent")
			return hotp
		except:
			print('sending otp exception')
			return 0
	
	def sendinglink(self, mail, name, link):
		try:
			smtp = smtplib.SMTP('smtp.gmail.com', 587)
			smtp.ehlo()
			smtp.starttls()
			smtp.login('developingproject7@gmail.com', 'lxezucynqaoeyijh')
			msg = MIMEMultipart()
			subject = "Reset Password link"
			msg['Subject'] = subject
			text1 = "Hi " + name + "," + "\n" + "\n" + "We received your request for changing the password of your " \
			"Project Django account." + "\n" + "\n" + "Click on this link: " + str(
				link) + '\n' + "If it doesn't work " \
			"just paste it in your browser." + "\n" + "\n"
			text2 = "If you didn't request this link, you can safely ignore this email. " \
			"Someone else might have typed your email address by mistake." + "\n" + "\n"
			text3 = "Thanks," + "\n" + '\n' + "The Project account team"
			text = text1 + text2 + text3
			msg.attach(MIMEText(text))
			to = [str(mail)]
			smtp.sendmail(from_addr="developingproject7@gmail.com", to_addrs=to, msg=msg.as_string())
			smtp.quit()
			print("Mail sent")
			return True
		except:
			print('sending otp exception')
			return False
