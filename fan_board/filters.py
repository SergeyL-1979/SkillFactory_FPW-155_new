from django_filters import FilterSet
from .models import Advertisement


class AdvertisementFilter(FilterSet):

    class Meta:
        model = Advertisement
        fields = ['ad_author', 'ad_category', 'headline']

