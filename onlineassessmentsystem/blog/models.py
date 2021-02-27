from django.db import models
from users.models import User


# Create your models here.

# helper method used for saving input file to upload in specific folder with proper name
def blogAttachmentFileName(instance, filename):
    totalBlogAttachment = BlogComments.objects.all().filter(blog=instance.blog).count() + 1
    return 'blogs/' + instance.blog.blogId.__str__() + "/" + totalBlogAttachment.__str__() + "_" + filename


class Blog(models.Model):
    blogId = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    title = models.CharField(null=False, max_length=50, default="DEFAULT-BLOG")
    description = models.CharField(null=False, max_length=1000, default="Default Blog description")


class BlogComments(models.Model):
    bcId = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    comment = models.CharField(max_length=2000)
    attachmentPath = models.FileField(upload_to=blogAttachmentFileName, max_length=254, blank=True, null=True)