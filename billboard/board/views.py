from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic import ListView

from board.models import Post


class PostsList(ListView):
    model = Post
    ordering = '-date'
    context_object_name = 'posts'
    paginate_by = 10
    template_name = 'home.html'


# Вызовется так же, если в функции будет: raise Http404()
def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
