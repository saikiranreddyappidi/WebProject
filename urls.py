from django.urls import path
from .import views
urlpatterns=[
    path('',views.firstreg,name='firstreg'),
    path('first/',views.first,name='first'),
    path('first/createacnt/',views.createacnt,name='createacnt'),
    path('first/createacnt/creating/',views.creating,name='creating'),
    path('course/',views.course,name='course'),
    path('course/btech/',views.btech,name='btech'),
    path('course/btech/cse/',views.cse,name='cse'),
    path('course/btech/cse/admin/',views.admin,name='admin'),
    path('course/pharma/',views.pharma,name='pharma'),
    path('course/law/',views.law,name='law'),
    path('course/manage/',views.manage,name='manage'),
]