from django.urls import path
from django.urls.conf import include
from django.contrib.auth import views as auth_views
from . import views

app_name = 'cars'
urlpatterns = [
    path('accounts/login/', auth_views.LoginView.as_view(template_name='cars/login.html'), name='login'),
    path('<int:pk>/', views.CarDetails.as_view(), name='offerdetails'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.IndexView.as_view(), name='index'),
]