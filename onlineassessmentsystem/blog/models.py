from django.db import models


# Create your models here.

class Blog(models.Model):
    blogId = models.AutoField(primary_key=True)
    title = models.CharField(null=False, max_length=50, default="DEFAULT-BLOG")
    description = models.CharField(null=False, max_length=1000, default="Default Blog description")
    attachmentPath = models.FileField(upload_to="blogs/", max_length=254)  # TODO: update
