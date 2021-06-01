from django.urls import path
from django.contrib.auth.views import LogoutView

from . import views
from . import forms

app_name = 'cars'
urlpatterns = [
    path('offers/<str:mark>/<str:model>/<int:pk>/', views.OfferDetails.as_view(), name='offer-details'),
    path('offers/<str:mark>/<str:model>/', views.modelsview, name='models'),
    path('offers/<str:mark>', views.marksview, name='marks'),
    path('offers/', views.OffersView.as_view(), name='offers'),
    path('profile/selfoffers/delete/<int:pk>', views.DeleteOfferView.as_view(), name='delete'),
    path('profile/selfoffers/addfavorite/<int:pk>', views.AddFavoriteView.as_view(), name='add-favorite'),
    path('profile/selfoffers/addoffer/', views.AddOfferView.as_view(), name='add-offer'),
    path('profile/selfoffers/', views.selfoffersview, name='self-offers'),
    path('profile/favoriteoffers/', views.favoriteoffersview, name='favorite-offers'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('logout/', LogoutView.as_view(next_page="/"), name='logout'),
    path('signin/', views.SignInView.as_view(), name='signin'),
    path('', views.IndexView.as_view(), name='index'),
]