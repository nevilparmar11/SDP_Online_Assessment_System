from django.urls import path
from . import views

urlpatterns = [
    path('', views.list),
    path('create/', views.create),
    path('edit/', views.edit),
    path('delete/', views.delete),
    path('view/', views.view),
    path('join/', views.joinClassroom),
    path('leave/', views.leaveClassroom),
    path('commentCreate/', views.commentCreate),
]
