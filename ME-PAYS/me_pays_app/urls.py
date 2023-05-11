"""Me_pays URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from me_pays_app.views.users import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path("", index, name='index'),
    path("register", registerenduser, name='register'),
    path("home", home, name='home'),
    path("transactions", transactions, name='transactions'),
    path("account", account, name='account'),
    path("cashdiv_home", cashdiv_home, name='cashdiv_home'),
    path("cashdiv_transaction", cashdiv_transaction, name='cashdiv_transaction'),
    path("cashdiv_account", cashdiv_account, name='cashdiv_account'),
    path("admin_home", admin_home, name='admin_home'),
    path("admin_addUser", admin_addUser, name='admin_adduser'),
    path("admin_listOfStaff", admin_listOfStaff, name='admin_listOfStaff'),
    path("admin_listOfStudent", admin_listOfStudent, name='admin_listOfStudent'),
    path("canteen_home", canteen_home, name='canteen_home'),
    path("canteen_products", canteen_products, name='canteen_products'),
    path("canteen_history", canteen_history, name='canteen_history'),
    path("logout", logout_request, name= "logout"),   #add this

    # functions
    path("insertMenu", views.insertMenu),
    path("menuList", views.menuList, name="menuList"),

]
