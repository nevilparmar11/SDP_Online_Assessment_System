from django.db import models
from users.models import User


# Create your models here.

# helper method used for saving input file to upload in specific folder with proper name
def blogAttachmentFileName(instance, filename):
    totalBlogAttachment = Blog.objects.all().filter(classroom=instance.classroom).count() + 1
    return 'blogs/' + instance.classroom.classId.__str__() + "/" + totalBlogAttachment.__str__() + "_" + filename


class Blog(models.Model):
    blogId = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    title = models.CharField(null=False, max_length=50, default="DEFAULT-BLOG")
    description = models.CharField(null=False, max_length=1000, default="Default Blog description")
