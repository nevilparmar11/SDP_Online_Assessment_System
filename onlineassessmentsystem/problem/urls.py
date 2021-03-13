from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import  static

urlpatterns = [
    path('', views.list),
    path('create/', views.create),
    path('edit/', views.edit),
    path('delete/', views.delete),
    path('view/', views.view),
    path('tests/', views.testList),
    path('testCreate/', views.testCreate),
    path('testDelete/', views.testDelete),
    path('testEdit/', views.testEdit),
    path('comments/', views.comments),
    path('commentCreate/', views.commentCreate),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
