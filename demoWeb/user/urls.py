from django.urls import path

from . import views

urlpatterns = [
    path('owner/login/', views.owner_login, name='owner_login'),
    path('owner/logout/', views.owner_logout, name='owner_logout'),
    path('owner/registry/', views.owner_registry, name='owner_registry'),
    path('owner/edit/', views.owner_edit, name='owner_edit'),
    path('owner/dashboard/', views.owner_dashboard, name='owner_dashboard'),
    path('owner/items/<str:model_name>/', views.item_list, name='item_list'),
    path('owner/items/<str:model_name>/create/', views.item_create, name='item_create'),
    path('owner/items/<str:model_name>/<int:pk>/edit/', views.item_update, name='item_update'),
    path('owner/items/<str:model_name>/<int:pk>/delete/', views.item_delete, name='item_delete'),
    path('projects/<int:pk>/', views.project_detail, name='project_detail'),
    path('blog/<int:pk>/', views.blog_detail, name='blog_detail'),
]