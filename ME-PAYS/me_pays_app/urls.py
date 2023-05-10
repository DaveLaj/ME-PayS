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
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns



urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index),
    path("index", views.index, name='index'),
    path("register", views.register),
    path("home", views.home),
    path("transactions", views.transactions),
    path("account", views.account),
    path("cashdiv_home", views.cashdiv_home),
    path("cashdiv_transaction", views.cashdiv_transaction),
    path("cashdiv_account", views.cashdiv_account),
    path("admin_home", views.admin_home),
    path("admin_addUser", views.admin_addUser),
    path("admin_listOfStaff", views.admin_listOfStaff),
    path("admin_listOfStudent", views.admin_listOfStudent),
    path("canteen_home", views.canteen_home),
    path("canteen_products", views.canteen_products),
    path("canteen_history", views.canteen_history),
    path("logout", views.logout_request, name= "logout"),   #add this

    # functions
    path("insertMenu", views.insertMenu),
    path("menuList", views.menuList, name="menuList"),

]
