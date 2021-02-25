from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.loginUser),
    path('register/', views.registerStudents),
    path('home/', views.home, name='home'),
    path('logout/', views.logoutUser, name='logout'),
    path('accessDenied/', views.accessDemied)
]
