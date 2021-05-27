from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from django.views import generic
from .models import *

class IndexView(generic.ListView):
    template_name = 'cars/index.html'
    context_object_name = 'latest_cars_list'

    def get_queryset(self):
        """Return the last five added cars."""
        return CarOffer.objects.order_by('-mark')[:5]

# one to many -> user and his car offers
# many to many -> user and his fav cars ofers <-> car offer and its following users
# one to one -> car offer and its statisto