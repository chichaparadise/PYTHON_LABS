from django.db import models
from django.urls import reverse

from .db_models.offer import Offer
from .db_models.statistics import Statistics
from .db_models.userprofile import UserProfile
from .db_models.image import Image
from .db_models.model import Model
from .db_models.mark import Mark


def get_offer_url(obj, urlpattern_name, model_name):
    return reverse