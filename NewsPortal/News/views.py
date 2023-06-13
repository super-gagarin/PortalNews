from datetime import datetime

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin


from .models import Author, Post, Category, Comment, PostCategory
from .filters import PostFilter
from .forms import PostForm

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('/news/')
    return render(request, 'registration/logout.html')


class NewsList(ListView):
    paginate_by = 2
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    ordering = '-postdatecreate'

class SearchNews(ListView):
    """ Представление всех постов в виде списка. """
    paginate_by = 3
    model = Post
    ordering = '-postdatecreate'
    template_name = 'search.html'
    context_object_name = 'news'

    def get_queryset(self):
        """ Переопределяем функцию получения списка статей. """
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs) -> dict:
        """ Метод get_context_data позволяет изменить набор данных, который будет передан в шаблон. """
        context = super().get_context_data(**kwargs)
        context['search_filter'] = self.filterset
        return context


class NewDetail(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'

class ArticleCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('News.add_post',)
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'new_edit.html'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Добавить статью"
        context['postnewstype'] = "Статья"
        return context


class ArticleUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('News.change_post',)
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'new_edit.html'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Редактировать статью"
        return context


class ArticleDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('News.delete_post',)
    raise_exception = True
    model = Post
    template_name = 'new_delete.html'
    success_url = reverse_lazy('posts_list')

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Удалить статью"
        context['previous_page_url'] = reverse_lazy('posts_list')
        return context

class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('News.add_post',)
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'new_edit.html'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Добавить новость"
        context['postnewstype'] = "Новость"
        return context


class NewsUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('News.change_post',)
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'new_edit.html'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Редактировать новость"
        return context


class NewsDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('News.delete_post',)
    raise_exception = True
    model = Post
    template_name = 'new_delete.html'
    success_url = reverse_lazy('posts_list')

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Удалить новость"
        context['previous_page_url'] = reverse_lazy('posts_list')
        return context