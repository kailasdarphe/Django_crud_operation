from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    age = models.IntegerField()
    phone = models.IntegerField()

    def __str__(self):        # _str_ this is used to print the object in readable format 
        return self.name
# Create your models here.
