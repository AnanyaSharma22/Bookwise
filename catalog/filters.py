from django import forms
import django_filters
from .models import Book, Genre, Author , Publisher

class CatalogFilter(django_filters.FilterSet):
    genre_id = django_filters.ModelMultipleChoiceFilter(queryset=Genre.objects.all(),
        widget=forms.CheckboxSelectMultiple)
    author = django_filters.ModelMultipleChoiceFilter(queryset=Author.objects.all(),
        widget=forms.CheckboxSelectMultiple)
    publisher_id = django_filters.ModelMultipleChoiceFilter(queryset=Publisher.objects.all(),
        widget=forms.CheckboxSelectMultiple)
    price = django_filters.NumericRangeFilter(name='price', lookup_expr='range')

    class Meta(object):
        model = Book
        fields = ['genre', 'author', 'publisher', 'price']
