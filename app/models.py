"""
Definition of models.
"""

from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Item(models.Model):
    text = models.CharField(max_length=200)
    user = models.ForeignKey(User)
    
    def __unicode__(self):
        return self.text