import django_filters
from .models import Post,Category

# Создаем свой набор фильтров для модели Product.
# FilterSet, который мы наследуем,
# должен чем-то напомнить знакомые вам Django дженерики.
class PostFilter(django_filters.FilterSet):
#    class Meta:
    heading = django_filters.CharFilter(field_name='heading', lookup_expr='icontains', label='Заголовок')
    content = django_filters.CharFilter(field_name='content', lookup_expr='icontains', label='Содержание')
    date_after = django_filters.DateFilter(field_name='date_time', lookup_expr='gte', label='Дата после')
    category = django_filters.ModelChoiceFilter(queryset=Category.objects.all(), label='Категория')

    class Meta:
        model = Post
        fields = ['heading', 'content', 'date_after', 'category']