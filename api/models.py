from django.db import models

# Post.objects.filer(user_id="") ...

# Create your models here.


class Note(models.Model):
    # user_id = models.ForeignKey("app.Model", verbose_name=_(""), on_delete=models.CASCADE)
    title = models.CharField(max_length=50, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    text = models.TextField(max_length=5000)
    url = models.CharField(max_length=500)
