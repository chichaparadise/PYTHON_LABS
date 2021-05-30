from django.db import models
from .db_models.offer import Offer
from .db_models.statistics import Statistics
from .db_models.userprofile import UserProfile
from .db_models.image import Image
from .db_models.model import Model
from .db_models.mark import Mark

# one to many -> user and his car offers
# many to many -> user and his fav cars ofers <-> car offer and its following users
# one to one -> car offer and its statistics
