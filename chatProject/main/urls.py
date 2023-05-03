
from django.urls import path, include
from . import views
from .views import getmessage, deletemessage


urlpatterns = [
    path('', views.index, name="chat"),
    path('login/', views.login_user, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('register/', views.register, name="register"),
    path('settings/', views.settings, name="settings"),
    path('sendmessage', views.sendmessage, name="sendmessage"),
    path('getmessage', getmessage.as_view(), name="getmessage"),
    path('deletemessage', views.deletemessage, name="deletemessage"),
    path('updatemessage', views.updatemessage, name="updatemessage"),

]
