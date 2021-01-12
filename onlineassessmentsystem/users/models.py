from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid,os

# this function will generate unique filename each time
def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('profiles/', filename)

class User(AbstractUser):
    isStudent = models.BooleanField(default=False, verbose_name="student")
    profilePicture = models.ImageField(upload_to=get_file_path, default="profiles/default.png", verbose_name="Profile Picture")