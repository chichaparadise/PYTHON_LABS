from django.db import models
from django.db.models.fields import CharField, IntegerField
from django.db.models.fields.related import ForeignKey, ManyToManyField, OneToOneField
from .userprofile import UserProfile
from .offerstatistics import OfferStatistics

class CarOffer(models.Model):
    mark = CharField(max_length=255)
    model = CharField(max_length=255)
    year = IntegerField(default=2000)
    owner = ForeignKey(UserProfile, on_delete=models.CASCADE)
    followers = ManyToManyField(UserProfile, related_name='favorite_offers', blank=True)
    statistics = OneToOneField(OfferStatistics, on_delete=models.CASCADE, primary_key=True, blank=True)
    
    def __str__(self):
        return ' '.join([self.mark, self.model])