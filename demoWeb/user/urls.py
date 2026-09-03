from django.urls import path

from . import views

urlpatterns = [
    path('owner/login/', views.owner_login, name='owner_login'),
    path('owner/registry/', views.owner_registry, name='owner_registry'),
]