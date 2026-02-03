from django.urls import path,include
from todoApp import views

urlpatterns = [
    path('', views.home, name='home'),
    path('all/', views.all, name='all'),
    path('add/', views.add, name='add'),
    path('detail/<int:item_id>/', views.detail, name='detail'),
    path('edit/<int:item_id>/', views.edit, name='edit'),
    path('delete/<int:item_id>/', views.delete, name='delete'),
    path('phoneList/', views.phoneList, name='phoneList'),
    path('phoneDetail/<int:item_id>/', views.phoneDetail, name='phoneDetail'),
]