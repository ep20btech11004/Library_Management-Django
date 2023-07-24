import django_filters
from django import forms
from django_filters import CharFilter, filters
from administration.models import *

class BookFilter(django_filters.FilterSet):
    name = CharFilter(field_name='name', label="", lookup_expr='icontains', widget=forms.TextInput(attrs={
        'placeholder': 'Search Book Name', 'class': 'form-control border-0 shadow-none'}))

    class Meta:
        model = Book
        fields = ('name',)

class GenreFilter(django_filters.FilterSet):
    genre = CharFilter(field_name='genre', label="", lookup_expr='icontains', widget=forms.TextInput(attrs={
        'placeholder': 'Search Book Name', 'class': 'form-control border-0 shadow-none'}))

    class Meta:
        model = Genre
        fields = ('genre',)

class LangFilter(django_filters.FilterSet):
    lang = CharFilter(field_name = 'lang', label="", lookup_expr='icontains', widget=forms.TextInput(attrs={
        'placeholder': 'Search Book Name', 'class': 'form-control border-0 shadow-none'}))
    
    class Meta:
        model = Language
        fields = ('lang',)

class CustomerFilter(django_filters.FilterSet):
    name = CharFilter(field_name='name', label="", lookup_expr='icontains', widget=forms.TextInput(attrs={
        'placeholder': 'Search Name', 'class': 'form-control border-0 shadow-none'}))

    class Meta:
        model = Customer
        fields = ('name',)

