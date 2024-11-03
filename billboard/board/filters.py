import django_filters
from django import forms
from django_filters import FilterSet, MultipleChoiceFilter
from .models import Reply


class ReplyFilter(FilterSet):

    text = django_filters.CharFilter(
        field_name='text',
        label='Текст',
        lookup_expr='iregex'
    )
    post = django_filters.CharFilter(
        field_name='post',
        label='Пост',
        lookup_expr='iregex'
    )
    date = django_filters.DateFilter(
        field_name='date',
        label='Дата отклика',
        lookup_expr='lt',
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Reply
        fields = ('text', 'post', 'date')