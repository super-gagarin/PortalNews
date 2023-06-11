from django.urls import path
# Импортируем созданные нами представления
from .views import NewsList, NewDetail, SearchNews
from .views import ArticleCreate, ArticleUpdate, ArticleDelete
from .views import NewsCreate, NewsUpdate, NewsDelete

urlpatterns = [
   path('', NewsList.as_view(), name='posts_list'),
   path('<int:pk>/', NewDetail.as_view(), name='post_detail'),
   path('search/', SearchNews.as_view(), name='search_posts'),
   path('news/create/', NewsCreate.as_view(), name='news_create'),
   path('news/<int:pk>/edit/', NewsUpdate.as_view(), name='news_update'),
   path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
   path('articles/create/', ArticleCreate.as_view(), name='article_create'),
   path('articles/<int:pk>/edit/', ArticleUpdate.as_view(), name='article_update'),
   path('articles/<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),
]

