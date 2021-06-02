from django import forms
from django.contrib.auth import authenticate, login
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_list_or_404, get_object_or_404, redirect, render
from django.views.generic import View
from django.http import HttpResponse
from django.views import generic

from datetime import datetime

from .forms import EditProfileForm, SignInForm, SignUpForm, AddOfferForm, EditOfferForm
from .models import *

def get_last_objects(model:object, order_by:str, count:int):
    try:
        return model.objects.order_by(order_by)[:count]
    except Exception:
        return None

class IndexView(generic.ListView):

    template_name = 'cars/index.html'
    context_object_name = 'latest_offers_list'

    def get_queryset(self):
        """Return the last five added cars."""
        return get_last_objects(Offer, '-mark', 8)

class OfferDetails(generic.DetailView):

    def get(self, request, mark, model, pk, *args, **kwargs):
        offer = get_object_or_404(Offer, pk=pk)
        print(offer.statistics.todays_views)
        offer.statistics.total_views += 1
        offer.statistics.todays_views += 1
        print(offer.statistics.todays_views)
        offer.statistics.save()
        context = {
            'offer' : offer
        }
        return render(request, 'cars/offerdetails.html', context)

class OffersView(generic.ListView):

    def get(self, request, *args, **kwargs):
        favorite_offers = None
        if request.user.is_authenticated:
            related_user = UserProfile.objects.get(user=request.user)
            favorite_offers = related_user.favorite_offers.filter(userprofile=related_user)
        context = {
            'offers' : Offer.objects.all(),
            'favorite_offers' : favorite_offers
        }
        return render(request, 'cars/offers.html', context)


class MarksView(generic.ListView):

    def get(self, request, mark, *args, **kwargs):
        favorite_offers = None
        if request.user.is_authenticated:
            related_user = UserProfile.objects.get(user=request.user)
            favorite_offers = related_user.favorite_offers.filter(userprofile=related_user)
        related_mark = get_object_or_404(Mark, mark=mark)
        offers_of_mark = get_list_or_404(Offer, mark=related_mark.pk)
        context = {
            'offers' : offers_of_mark,
            'favorite_offers' : favorite_offers,
            'mark' : mark
        }
        return render(request, 'cars/mark.html', context)


class ModelsView(generic.ListView):

    def get(self, request, mark, model, *args, **kwargs):
        favorite_offers = None
        if request.user.is_authenticated:
            related_user = UserProfile.objects.get(user=request.user)
            favorite_offers = related_user.favorite_offers.filter(userprofile=related_user)
        related_mark = get_object_or_404(Mark, mark=mark)
        related_model = get_object_or_404(Model, model=model)
        offers_of_model = get_list_or_404(Offer, model=related_model.pk, mark=related_mark.pk)
        context = {
            'offers' : offers_of_model,
            'favorite_offers' : favorite_offers,
            'mark' : mark,
            'model' : model
        }
        return render(request, 'cars/model.html', context)


class FavoriteOffersView(generic.ListView):

    def get(self, request, *args, **kwargs):
        related_user = get_object_or_404(UserProfile, user=request.user)
        favorite_offers = related_user.favorite_offers.filter(userprofile=related_user)
        context = {
            'offers' : favorite_offers,
        }
        return render(request, 'cars/favoriteoffers.html', context)


class SelfOffersView(generic.ListView):

    def get(self, request, *args, **kwargs):
        related_user = get_object_or_404(UserProfile, user=request.user)
        user_offers = Offer.objects.filter(owner=related_user)
        context = {
            'offers' : user_offers,
        }
        return render(request, 'cars/selfoffers.html', context)


class DeleteOfferView(View):

    def get(self, request, pk):
        redirect_to = request.GET.get('next', '')
        offer = Offer.objects.get(pk=pk)
        offer.delete()
        return HttpResponseRedirect(redirect_to)

class AddFavoriteView(View):

    def get(self, request, pk):
        redirect_to = request.GET.get('next', '')
        offer = Offer.objects.get(pk=pk)
        related_user = get_object_or_404(UserProfile, user=request.user)
        if not offer in related_user.favorite_offers.all():
            related_user.favorite_offers.add(offer)
        else:
            related_user.favorite_offers.remove(offer)
        return HttpResponseRedirect(redirect_to)

class UserProfileView(View):
    
    def get(self, request, *args, **kwargs):
        user = UserProfile.objects.get(user=request.user)
        context = {
            'user' : user,
        }
        return render(request, 'cars/profile.html', context)


class SignInView(View):

    def get(self, request, *args, **kwargs):
        form = SignInForm(request.POST or None)
        context = {'form':form,}
        return render(request, 'cars/signin.html', context)

    def post(self, request, *args, **kwargs):
        redirect_to = request.GET.get('next', '')
        form = SignInForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect(redirect_to)
        context = {'form' : form, 'offers' : get_list_or_404(Offer)}
        return render(request, 'cars/signin.html', context)


class SignUpView(View):

    def get(self, request, *args, **kwargs):
        form = SignUpForm(request.POST or None)
        context = {'form':form, }
        return render(request, 'cars/signup.html', context)

    def post(self, request, *args, **kwargs):
        redirect_to = request.GET.get('next', '')
        form = SignUpForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.username = form.cleaned_data['username']
            new_user.save()
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            UserProfile.objects.create(
                user=new_user,
            )
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            login(request, user)
            return HttpResponseRedirect(redirect_to)
        context = {'form' : form}
        return render(request, 'cars/signup.html', context)


class AddOfferView(View):

    def get(self, request, *args, **kwargs):
        form = AddOfferForm(request.POST or None)
        context = {'form':form}
        return render(request, 'cars/addoffer.html', context)

    def post(self, request, *args, **kwargs):
        redirect_to = request.GET.get('next', '')
        form = AddOfferForm(request.POST, request.FILES)
        if form.is_valid():
            new_offer_statistics = Statistics.objects.create(publish_date=datetime.now())
            related_user = get_object_or_404(UserProfile, user=request.user)
            Offer.objects.create(
                mark = form.cleaned_data['mark'],
                model = form.cleaned_data['model'],
                year = form.cleaned_data['year'],
                owner = related_user,
                description = form.cleaned_data['description'],
                price = form.cleaned_data['price'],
                statistics=new_offer_statistics,
                image = form.cleaned_data['image']
            )
            return HttpResponseRedirect(redirect_to)
        context = {'form' : form}
        return render(request, 'cars/addoffer.html', context)


class EditProfileView(View):

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(UserProfile, user=request.user)
        form = EditProfileForm(instance=user)
        context = {'form':form}
        return render(request, 'cars/editprofile.html', context)

    def post(self, request, *args, **kwargs):
        redirect_to = request.GET.get('next', '')
        user = get_object_or_404(UserProfile, user=request.user)
        form = EditProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(redirect_to)
        context = {'form' : form}
        return render(request, 'cars/editprofile.html', context)


class EditOfferView(View):

    def get(self, request, pk, *args, **kwargs):
        offer = get_object_or_404(Offer, pk=pk)
        form = EditOfferForm(instance=offer)
        context = {
            'form':form,
            'offer' : offer
        }
        return render(request, 'cars/editoffer.html', context)

    def post(self, request, pk, *args, **kwargs):
        redirect_to = request.GET.get('next', '')
        offer = get_object_or_404(Offer, pk=pk)
        form = EditOfferForm(request.POST, instance=offer)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(redirect_to)
        context = {
            'form':form,
            'offer' : offer
        }
        return render(request, 'cars/editoffer.html', context)
