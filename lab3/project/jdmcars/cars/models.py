from django.db import models
from django.db.models.fields import CharField, IntegerField

class Car(models.Model):
    mark = CharField(max_length=255)
    model = CharField(max_length=255)
    year = IntegerField(default=2000) 
    
    def __str__(self):
        return ' '.join([self.mark, self.model])
