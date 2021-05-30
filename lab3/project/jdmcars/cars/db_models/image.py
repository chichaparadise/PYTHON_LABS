from django.db import models
from django.db.models.fields.files import ImageField
from django.db.models.fields.related import ForeignKey

class Image(models.Model):

    image = ImageField()
    offer = ForeignKey('Offer', on_delete=models.CASCADE, related_name='images_of_offer')

    def __str__(self):
        return self.image.url