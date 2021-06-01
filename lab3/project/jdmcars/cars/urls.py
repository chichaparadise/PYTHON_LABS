from django.urls import path

from . import views
from . import forms

app_name = 'cars'
urlpatterns = [
    path('offers/<str:mark>/<str:model>/<int:pk>/', views.OfferDetails.as_view(), name='offer-details'),
    path('offers/<str:mark>/<str:model>/', views.modelsview, name='models'),
    path('offers/<str:mark>', views.marksview, name='marks'),
    path('offers/', views.OffersView.as_view(), name='offers'),
    path('', views.IndexView.as_view(), name='index'),
    path('signin/', views.SignInView.as_view(), name='signin'),
]