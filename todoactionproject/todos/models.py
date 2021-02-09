from django.db import models
from django.contrib.auth.models import User

class ToDo(models.Model):
    title = models.CharField(max_length=30)
    memo = models.TextField(blank = True)
    date_created = models.DateTimeField(auto_now_add = True)
    date_completed = models.DateTimeField(null = True, blank = True)
    important = models.BooleanField(default = False)
    user = models.ForeignKey(User, on_delete = models.CASCADE,default='')

    def __str__(self):
    	return self.title