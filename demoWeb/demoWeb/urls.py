"""
URL configuration for demoWeb project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
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
from django.shortcuts import render, redirect, get_object_or_404

def main_page(request):
    return render(request, 'base.html') 

def about_page(request):
    return render(request, 'base.html')

def elements_page(request):
    return render(request, 'base.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_page, name='home'),
    path('about/', about_page, name='about'),
    path('elements/', elements_page, name='elements'),
]
