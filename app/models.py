from django.db import models

# User class for built-in authentication module
from django.contrib.auth.models import User

class Item(models.Model):
    name = models.CharField(blank=True,max_length=160)
    Bus = models.CharField(blank=True,max_length=160)
    Direction = models.CharField(blank=True,max_length=160)
    stopname = models.CharField(blank=True,max_length=160)
    # stpid = models.IntegerField()
    url = models.URLField(blank=True)
    user = models.ForeignKey(User)		
    def __unicode__(self):
        return self.text
