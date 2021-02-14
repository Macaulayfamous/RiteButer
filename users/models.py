from django.db import models

# Create your models here.



class ContactPage(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField(max_length=30)
    message = models.TextField()

    def __str__(self):
        return self.name
    