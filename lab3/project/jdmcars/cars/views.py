from cars.models import Car
from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from django.views import generic
from .models import Car

class IndexView(generic.ListView):
    template_name = 'cars/index.html'
    context_object_name = 'latest_cars_list'

    def get_queryset(self):
        """Return the last five added cars."""
        return Car.objects.order_by('-mark')[:5]