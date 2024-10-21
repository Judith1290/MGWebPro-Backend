from django.db import models

class ContactModel(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=20)
    message = models.TextField()

    def __str__(self):
        return self.name
