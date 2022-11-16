from django.urls import path
from . import views

urlpatterns = [
    path('', views.loginform, name='loginform'),
    path('login/', views.newlogin, name='newlogin'),
    path('home/', views.index, name='index'),
    path('home/message/', views.tweet, name='tweet'),
    path('home/<str:identity>', views.change_present_page, name='change_present_page'),
    path('test/', views.test, name='test'),
    path('home/child-iframe.html/', views.iframe, name='iframe'),
    path('child-iframe.html/', views.iframe, name='iframe'),
    path('home/logout/', views.logout, name='logout'),
path('test/child-iframe.html/', views.iframe, name='iframe'),
]
