from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.loginUser),
    path('home/', views.home),
    path('logout/', views.logoutUser),
    path('accessDenied/', views.accessDemied)
]
