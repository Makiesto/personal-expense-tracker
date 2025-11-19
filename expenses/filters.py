import django_filters

from .models import Expense


class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Expense
        fields = {
            'category': ['exact'],
            'cost': ['lt', 'gt'],

        }
