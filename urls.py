from django.urls import path
from .import views
urlpatterns = [
    path('',views.firstreg,name='firstreg'),
    path('mail_checking/',views.mail_checking,name='mail_checking'),
    path('mail_checking/comparing_mail/',views.comparing_mail,name='comparing_mail'),
    path('updating_password/',views.updating_password,name='updating_password'),
    path('updating_password/importing_password/',views.importing_password,name='importing_password'),
    path('first/',views.first,name='first'),
    path('first/',views.wrongmessage,name='wrongmessage'),
    path('faculty/',views.faculty,name='faculty'),
    path('faculty/facultyaccess/',views.facultyaccess,name='facultyaccess'),
    path('faculty/facultyaccess/pdf_links/',views.pdf_links,name='pdf_links'),
    path('faculty/facultyaccess/pdf_links/delete/<str:filename>',views.delete,name='delete'),
    path('faculty/facultyaccess/pdf_links/add/',views.add,name='add'),
    path('faculty/facultyaccess/pdf_links/add/addlink/',views.addlink,name='addlink'),
    path('createacnt/',views.createacnt,name='createacnt'),
    path('createacnt/creating/',views.creating,name='creating'),
    path('course/',views.course,name='course'),
    path('course/',views.btech,name='btech'),
    path('course/cse',views.cse,name='cse'),
    path('course/cse/admin/',views.admin,name='admin'),
    path('course/',views.pharma,name='pharma'),
    path('course/',views.law,name='law'),
    path('course/',views.manage,name='manage'),
]

