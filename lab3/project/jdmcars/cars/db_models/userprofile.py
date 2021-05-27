from django.db import models
from django.db.models.fields import CharField, EmailField

class UserProfile(models.Model):
    user_name = CharField(max_length=255)
    first_name = CharField(max_length=255)
    last_name = CharField(max_length=255)
    email = EmailField()

    def __str__(self):
        return ' '.join([self.first_name, self.last_name])