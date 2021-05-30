from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from django.views import generic
from .models import *

# def get_last_objects(model:object, order_by:str, count:int):
#     try:
#         return model.objects.order_by(order_by)[:count]
#     except Exception:
#         return None

# class IndexView(generic.ListView):
#     template_name = 'cars/index.html'
#     context_object_name = 'latest_cars_list'

#     def get_queryset(self):
#         """Return the last five added cars."""
#         return get_last_objects(Offer, '-mark', 5)

# class CarDetails(generic.DetailView):
#     model = Offer
#     template_name = 'cars/details.html'

def test_view(request):
    return render(request, 'cars/base.html')
