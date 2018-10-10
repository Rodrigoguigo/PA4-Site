"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf.urls import url

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/login', views.login, name='login'),
    path('admin/', views.admin, name='home'),
    path('admin/cardapio', views.adminCardapio, name='adminCardapio'),
    path('admin/add', views.addPizza, name='addPizza'),
    path('sendMessage', views.sendMessage, name='message'),
    path('checkUpdates', views.checkUpdates, name='checkUpdates'),
    path('completeOrder', views.completeOrder, name='completeOrder')
]
