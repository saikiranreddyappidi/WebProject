from django.db import models

class Members(models.Model):
  reg = models.CharField(max_length=255)
  sec = models.CharField(max_length=255)