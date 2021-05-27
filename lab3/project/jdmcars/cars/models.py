from django.db import models
from .db_models.caroffer import CarOffer
from .db_models.offerstatistics import OfferStatistics
from .db_models.userprofile import UserProfile

# one to many -> user and his car offers
# many to many -> user and his fav cars ofers <-> car offer and its following users
# one to one -> car offer and its statistics
