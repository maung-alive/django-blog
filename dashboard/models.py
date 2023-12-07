from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Action(models.Model):
    msg = models.CharField(max_length=300)
    type = models.CharField(max_length=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name + " " + self.action