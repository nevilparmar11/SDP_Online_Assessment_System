from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.loginUser),
    path('register/', views.registerStudents),
    path('home/', views.home, name='home'),
    path('logout/', views.logoutUser, name='logout'),
    path('accessDenied/', views.accessDemied),
    path('viewProfile', views.viewProfile),
    path('editProfile', views.editProfile),
    path('changePassword', views.changePassword),
]
