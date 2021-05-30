from PIL import Image as Img

from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from .models import *


class ImageAdminForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].help_text = 'Uploaded images with resolution greater than {}x{} will be resized'.format(*Image.MIN_RESOLUTION)


admin.site.register(Offer)
admin.site.register(UserProfile)
admin.site.register(Statistics)
admin.site.register(Image, form=ImageAdminForm)
admin.site.register(Model)
admin.site.register(Mark)