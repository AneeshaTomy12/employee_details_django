from django.db import models

class Empmodel(models.Model):
    name=models.CharField(max_length=30)
    age=models.CharField(max_length=30)
    def __str__(self):
        return self.name