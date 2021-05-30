from django.contrib import admin
from django.forms.models import ModelChoiceField
from .models import *


admin.site.register(Offer)
admin.site.register(UserProfile)
admin.site.register(Statistics)
admin.site.register(Image)
admin.site.register(Model)
admin.site.register(Mark)