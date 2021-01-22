from django.urls import path
from . import views

urlpatterns = [
    path('', views.list),
    path('create/', views.create),
    path('edit/', views.edit),
    path('delete/', views.delete),
    path('view/', views.view),
]
