from django.contrib import admin
from .models import Problem, ProblemComment, TestCase

admin.site.register(Problem)
admin.site.register(ProblemComment)
admin.site.register(TestCase)