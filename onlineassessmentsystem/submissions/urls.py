from django.urls import path

from . import views

urlpatterns = [
    path('submit/', views.submitCode),
    path('list/', views.list),
    path('view/', views.view),
]
