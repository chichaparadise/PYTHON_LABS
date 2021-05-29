from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField, EmailField
from django.contrib.auth import get_user_model
from django.db.models.fields.related import ForeignKey
from django.utils.translation import override

User = get_user_model()

class UserProfile(models.Model):
    user = ForeignKey(User, on_delete=CASCADE)

    def __str__(self):
        return ' '.join([self.user.first_name, self.user.last_name])