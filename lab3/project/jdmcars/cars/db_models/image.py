from PIL import Image as Img

from django.db import models
from django.db.models.fields.files import ImageField
from django.db.models.fields.related import ForeignKey
from django.core.files.uploadedfile import InMemoryUploadedFile

from io import BytesIO
import sys

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
        return ' '.join([str(self.offer), self.image.url])

    def save(self, *args, **kwargs):
        image = self.image
        img = Img.open(image)
        new_img = img.convert('RGB')
        resized_new_img = new_img.resize((900, 500), Img.ANTIALIAS)
        filestream = BytesIO()
        resized_new_img.save(filestream, 'JPEG', quality=90)
        filestream.seek(0)
        name = '{}.{}'.format(*self.image.name.split('.'))
        self.image = InMemoryUploadedFile(
            filestream, 'ImageField', name, 'jpeg/image', sys.getsizeof(filestream), None
        )
        super().save(*args, **kwargs)