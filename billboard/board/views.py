from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from board.forms import *

# Create your views here.
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from board.models import Post


class PostsList(ListView):
    model = Post
    ordering = '-date'
    context_object_name = 'posts'
    paginate_by = 10
    template_name = 'board/home.html'


class PostDetail(DetailView):
    model = Post
    template_name = 'board/post_detail.html'
    context_object_name = 'post'


class PostCreate(LoginRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'board/post_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        return super().form_valid(form)


class PostUpdate(LoginRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post

    def get_template_names(self):
        return 'board/post_create.html'


class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('account')

    def get_template_names(self):
        return 'board/post_delete.html'


class ReplyCreate(LoginRequiredMixin, CreateView):
    form_class = ReplyForm
    model = Reply
    template_name = 'board/reply_create.html'

    def form_valid(self, form):
        reply = form.save(commit=False)
        reply.author = self.request.user
        reply.post = Post.objects.get(pk=self.request.path.split('/')[2])
        reply.save()
        return super().form_valid(form)

# Вызовется так же, если в функции будет: raise Http404()
def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')

