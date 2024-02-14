from django.db import models
from django.contrib.auth.models import User

# Post.objects.filer(user_id="") ...

# Create your models here.


class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    markdown = models.TextField(max_length=5000)
    url = models.CharField(max_length=500)
