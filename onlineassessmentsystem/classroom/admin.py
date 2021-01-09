from django.contrib import admin
from django.contrib.auth.models import User
from .models import Classroom,ClassComments
# Register your models here.

admin.site.register(Classroom)
admin.site.register(ClassComments)