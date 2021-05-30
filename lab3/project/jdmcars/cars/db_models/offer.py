from django.db import models
from django.db.models.fields import IntegerField, TextField
from django.db.models.fields.related import ForeignKey, OneToOneField

class Offer(models.Model):

    mark = ForeignKey('Mark', on_delete=models.CASCADE)
    model = ForeignKey('Model', on_delete=models.CASCADE)
    year = IntegerField(default=2000)
    owner = ForeignKey('UserProfile', on_delete=models.CASCADE, related_name='owner')
    description = TextField(blank=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, blank=True)
    statistics = OneToOneField('Statistics', on_delete=models.CASCADE, primary_key=True)
    
    def __str__(self):
        return ' '.join([str(self.mark), str(self.model), str(self.year)])