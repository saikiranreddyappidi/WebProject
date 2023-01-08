from django.urls import path
from . import views

urlpatterns = [
    path('', views.firstreg, name='firstreg'),
    # path('alreadylogin/home/', views.home, name='home'),
    path('first/', views.first, name='first'),
    path('file/', views.file, name='file'),
    path('file/fileinp/', views.fileinp, name='fileinp'),
    path('redirection/', views.redirection, name='redirection'),
    # path('alreadylogin/', views.alreadylogin, name='alreadylogin'),
    path('newlogin/', views.newlogin, name='newlogin'),
    path('newlogin/first/', views.first, name='first'),
    path('course/', views.course, name='course'),
    path('redirection/user_response/', views.user_response, name='user_response'),
    path('course/<str:branch>/', views.cse, name='cse'),
    path('requestedprofile/<str:regno>', views.requested_userprofile, name='requested_userprofile'),
    path('creator/', views.newadmin, name='newadmin'),
    path('userprofile/', views.userprofile, name='userprofile'),
    path('myfiles/', views.my_files, name='my_files'),
    path('myfiles/delete_requests/<str:filename>/', views.delete_requests, name='delete_requests'),
    path('myfiles/delete_requests/<str:filename>/raise_deletion_requests/', views.raise_deletion_requests,
         name='raise_deletion_requests'),
    path('logout/', views.user_logout, name='user_logout'),
    path('already_login_once/', views.already_login_once, name='already_login_once'),
    path('already_login_once/alreadylogin/', views.alreadylogin, name='alreadylogin'),
    path('verifying/', views.check_status, name='check_status'),
    path('reset-password/<str:link>/', views.linkpasswordpage, name='linkpasswordpage'),
    path('reset-password/<str:link>/linktype/', views.linktype, name='linktype'),
    path('mail_checking/', views.mail_checking, name='mail_checking'),
    path('mail_checking/comparing_mail/', views.comparing_mail, name='comparing_mail'),
    path('updating_password/', views.updating_password, name='updating_password'),
    path('updating_password/importing_password/', views.importing_password, name='importing_password'),
    path('faculty/', views.faculty, name='faculty'),
    path('faculty/facultyaccess/', views.facultyaccess, name='facultyaccess'),
    path('faculty/facultyaccess/requestings/', views.requestings, name='requestings'),
    path('faculty/facultyaccess/requestings/comment_section/<str:filename>/', views.comment_section,
         name='comment_section'),
    path('faculty/facultyaccess/requestings/comment_section/<str:filename>/add_comment/', views.add_comment,
         name='add_comment'),
    path('faculty/facultyaccess/requestings/apporve/<str:filename>', views.apporve, name='apporve'),
    path('faculty/facultyaccess/requestings/decline/<str:filename>', views.decline, name='decline'),
    path('faculty/facultyaccess/pdf_links/', views.pdf_links, name='pdf_links'),
    path('faculty/facultyaccess/pdf_links/delete/<str:filename>', views.delete, name='delete'),
    path('faculty/facultyaccess/pdf_links/add/', views.add, name='add'),
    path('faculty/facultyaccess/pdf_links/add/addlink/', views.addlink, name='addlink'),
    path('faculty/fac_logout/', views.fac_logout, name='fac_logout'),
    path('createacnt/', views.createacnt, name='createacnt'),
    path('createacnt/creating/', views.creating, name='creating'),
    path('upload/', views.userinp, name='userinp'),
    path('upload/userfileinp/', views.userfileinp, name='userfileinp'),
    path('editor/', views.creating_profile, name='creating_profile'),
    path('example/', views.example_template, name='example_template'),
    path('editor/saveOnly/', views.saveOnly, name='saveOnly'),
    path('editor/saveNleave/', views.saveNleave, name='saveNleave'),
    path('profile/<str:regno>', views.ownProfile, name='ownProfile'),
    # path('first/first/',views.first,name='first'),
    # path('wrongpassword/first/',views.wrongpassword,name='wrongpassword'),
    # path('noaccount/first/first/',views.first,name='first'),
    # path('noaccount/first/',views.noaccountfound,name='noaccountfound'),
    # path('first/',views.wrongmessage,name='wrongmessage'),
    # path('course/',views.pharma,name='pharma'),
    # path('course/',views.law,name='law'),
    # path('testing/',views.manage,name='manage'),
    # path('testing/fileip/',views.fileip,name='fileip'),
    # path('setcookie/',views.setcookie,name='setcookie'),
    # path('first/cse/',views.cse,name='cse'),
    # path('course/',views.btech,name='btech'),
    # path('course/<str:name>',views.files,name='files'),
]