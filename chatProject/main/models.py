from django.db import models
from datetime import datetime
from django.contrib.auth.models import User


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    dateCreated = models.DateTimeField(auto_now_add=True, null=True)
    profilePic = models.ImageField(default='defaultUser.jpg', null=True, blank=True)

    def __str__(self):
        return self.user.username


class Messages(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    text = models.CharField(max_length=1000, null=True)
    dateCreated = models.DateTimeField(default=datetime.now(), null=True)
    changed = models.BooleanField(default=False, null=True, blank=True)
    textChanged = models.CharField(max_length=1000, null=True, blank=True)
    dateChanged = models.DateTimeField(default=datetime.now(), null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}, {self.dateCreated} "


class UserLogs(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    dateLoged = models.DateTimeField(null=True)

    def __str__(self):
        return f"{self.user.username}, {self.dateLoged} "