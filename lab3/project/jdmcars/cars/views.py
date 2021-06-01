from django import forms
from django.contrib.auth import authenticate, login
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.views.generic import View
from django.http import HttpResponse
from django.views import generic

from .forms import SignInForm, SignUpForm
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
        return get_last_objects(Offer, '-mark', 5)

class OfferDetails(generic.DetailView):

    model = Offer
    template_name = 'cars/offerdetails.html'

class OffersView(generic.ListView):
    
    template_name = 'cars/offers.html'
    context_object_name = 'offers'

    queryset = Offer.objects.all()

def marksview(request, mark):
    related_mark = get_object_or_404(Mark, mark=mark)
    offers_of_mark = get_list_or_404(Offer, mark=related_mark.pk)
    return render(request, 'cars/mark.html', {'offers' : offers_of_mark, 'mark' : mark })

def modelsview(request, mark, model):
    related_mark = get_object_or_404(Mark, mark=mark)
    related_model = get_object_or_404(Model, model=model)
    offers_of_model = get_list_or_404(Offer, model=related_model.pk, mark=related_mark.pk)
    return render(request, 'cars/model.html', {'offers' : offers_of_model, 'mark' : mark, 'model' : model})

class SignInView(View):

    def get(self, requset, *args, **kwargs):
        form = SignInForm(requset.POST or None)
        context = {'form':form, 'offers' : get_list_or_404(Offer)}
        return render(requset, 'cars/signin.html', context)

    def post(self, requset, *args, **kwargs):
        form = SignInForm(requset.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(requset, user)
                return HttpResponseRedirect('/')
        context = {'form' : form, 'offers' : get_list_or_404(Offer)}
        return render(requset, 'cars/signin.html', context)


class SignUpView(View):

    def get(self, request, *args, **kwargs):
        form = SignUpForm(request.POST or None)
        context = {'form':form, 'offers' : get_list_or_404(Offer)}
        return render(request, 'cars/signup.html', context)

    def post(self, request, *args, **kwargs):
        form = SignUpForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.username = form.cleaned_data['username']
            new_user.email = form.cleaned_data['email']
            new_user.first_name = form.cleaned_data['first_name']
            new_user.last_name = form.cleaned_data['last_name']
            new_user.save()
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            UserProfile.objects.create(
                user=new_user,
                # phone=form.cleaned_data['phone'],
                # address=form.cleaned_data['address']
            )
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            login(request, user)
            return HttpResponseRedirect('/')
        context = {'form' : form}
        return render(request, 'cars/signup.html', context)