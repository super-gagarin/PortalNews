from django_filters import FilterSet
import django_filters
import django.forms
from .models import Post, Category

# Создаем свой набор фильтров для модели Product.
# FilterSet, который мы наследуем,
# должен чем-то напомнить знакомые вам Django дженерики.
class PostFilter(FilterSet):

    posttitle = django_filters.CharFilter(
        field_name='posttitle', label='Заголовок содержит', lookup_expr='icontains',
        widget=django.forms.TextInput(
            attrs={'type': 'text', 'class': "form-control", 'placeholder': "Ведите текст..."}))

    postcat = django_filters.ModelMultipleChoiceFilter(
        field_name='postcat', label='Искать в категориях', lookup_expr='exact', queryset=Category.objects.all(),
        widget=django.forms.CheckboxSelectMultiple(
            attrs={'type': 'checkbox', 'class': "form-check-inline"}))

    postdatecreate__gt = django_filters.DateFilter(
        field_name="postdatecreate", label="От даты", lookup_expr='gt',
        widget=django.forms.DateInput(
            attrs={'type': 'date', 'class': "form-control"}))

    postdatecreate__lt = django_filters.DateFilter(
        field_name="postdatecreate", label="От даты", lookup_expr='gt',
        widget=django.forms.DateInput(
            attrs={'type': 'date', 'class': "form-control"}))

    class Meta:
       # В Meta классе мы должны указать Django модель,
       # в которой будем фильтровать записи.
       model = Post
       # В fields мы описываем по каким полям модели
       # будет производиться фильтрация.
       fields = {
           # поиск по названию
           'posttitle': ['icontains'],
           # по категории
           'postcat': ['icontains'],
           'postdatecreate': [
               'lt',  # до даты
               'gt',  # оо даты
           ],
       }

