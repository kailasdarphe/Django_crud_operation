from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    age = models.IntegerField()
    phone = models.IntegerField()

    def __str__(self):        # _str_ this is used to print the object in readable format 
        return self.name

# ✅ New Model for Chat Messages
class ChatMessage(models.Model):
    sender = models.CharField(max_length=10)  
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender}: {self.message[:30]}"