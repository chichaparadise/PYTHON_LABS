from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth import get_user_model
from django.db.models.fields.related import ForeignKey, ManyToManyField

User = get_user_model()

class UserProfile(models.Model):

    user = ForeignKey(User, on_delete=CASCADE)
    favorite_offers = ManyToManyField('UserProfile')

    def __str__(self):
        if self.user.last_name != ' ':
            return ' '.join([self.user.first_name, self.user.last_name])
        return self.user.user_name