from PIL import Image as Img

from django.db import models
from django.db.models.fields.files import ImageField
from django.db.models.fields.related import ForeignKey


class MinResulionErrorException(Exception):
    pass

class MaxResulionErrorException(Exception):
    pass

class Image(models.Model):

    MIN_RESOLUTION = (400, 400)
    MAX_RESOLUTION = (800, 800)
    MAX_SIZE = 3145728

    image = ImageField()
    offer = ForeignKey('Offer', on_delete=models.CASCADE, related_name='images_of_offer')

    def __str__(self):
        return self.image.url

    def save(self, *args, **kwargs):
        image = self.image
        img = Img.open(image)
        min_height, min_width = self.MIN_RESOLUTION
        if img.height < min_height or img.width < min_width:
            raise MinResulionErrorException('Uploaded image resolution lower than minimum')
        max_height, max_width = self.MAX_RESOLUTION
        if img.height > max_height or img.width > max_width:
            raise MaxResulionErrorException('Uploaded image resolution greater than maximum allowed({}x{}), provided {}x{}'.format(*self.MAX_RESOLUTION, img.width, img.height))
        super().save(*args, **kwargs)