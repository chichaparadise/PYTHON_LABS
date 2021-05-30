from django.urls import path
from . import views

app_name = 'cars'
urlpatterns = [
    # path('<int:pk>/', views.CarDetails.as_view(), name='details'),
    # path('', views.IndexView.as_view(), name='index'),
    path('', views.test_view, name='base')
]