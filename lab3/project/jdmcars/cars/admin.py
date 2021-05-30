from PIL import Image as Img

from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from .models import *


class ImageAdminForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].help_text = 'Upload images with minimum resolution {}x{}'.format(*Image.MIN_RESOLUTION)

    def clean_image(self):
        image = self.cleaned_data['image']
        img = Img.open(image)
        min_height, min_width = Image.MIN_RESOLUTION
        if image.size > Image.MAX_SIZE:
            raise ValidationError('Uploaded image size is greater than 3 MB')
        if img.height < min_height or img.width < min_width:
            raise ValidationError('Uploaded image resolution lower than minimum')
        max_height, max_width = Image.MAX_RESOLUTION
        if img.height > max_height or img.width > max_width:
            raise ValidationError('Uploaded image resolution greater than maximum allowed({}x{}), provided {}x{}'.format(*Image.MAX_RESOLUTION, img.width, img.height))
        return image


admin.site.register(Offer)
admin.site.register(UserProfile)
admin.site.register(Statistics)
admin.site.register(Image, form=ImageAdminForm)
admin.site.register(Model)
admin.site.register(Mark)