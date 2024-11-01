from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib import auth
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
import random
import string
from django.conf import settings


# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView

from account.forms import *
from account.models import OneTimeCode
from board.models import Post


def generate_string(length):
    all_symbols = string.ascii_uppercase + string.digits
    result = ''.join(random.choice(all_symbols) for _ in range(length))
    return result


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'account/account.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["posts"] = Post.objects.filter(author=self.request.user).order_by('-date')
        return context


class RegisterView(CreateView):
    form_class = RegisterUserForm
    template_name = 'account/register.html'
    extra_context = {'title': 'Регистрация'}
    success_url = reverse_lazy('onetimecode')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        return super().form_valid(form)


def login_view(request):
    if request.method == 'POST':
        password = request.POST['password']
        email = request.POST['email']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            new_code = OneTimeCode.objects.create(code=generate_string(6), user=user)
            # отправляем одноразовый код на почту
            new_code.save()

            message = f'Ваш код авторизации на форуме: \n' \
                      f'{new_code.code}'
            send_mail(
                f'Код авторизации пользователя',
                message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
            )
            # выводим страницу с сообщением, что отправлено письмо
            return redirect('onetimecode')

        else:
            raise ValueError('Неверные имя пользователя или пароль')
    else:
        form = LoginUserForm()
        return render(request, 'account/login.html', {'form': form})


def login_with_code_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        code = request.POST['code']
        one_time = OneTimeCode.objects.filter(code=code, user__username=username)
        if one_time:
            login(request, one_time[0].user)
            return redirect('home')
    else:
        form = OneTimeCodeForm()
        return render(request, 'account/onetimecode.html', {'form': form})





# def one_time_code(request):
#     if request.method == 'POST':
#         form = OneTimeCodeForm(request.POST)
#         if form.is_valid():
#             print('form valid')
#             request.user.is_active = True
#             login(request, request.user)
#             return redirect('home')
#     else:
#         form = OneTimeCodeForm()
#         return render(request, 'account/onetimecode.html', {'form': form})
#
#
# def one_time_code_update(request):
#     usercode = OneTimeCode.objects.get(user=request.user.pk)
#     usercode.code = generate_string(6)
#     usercode.save()
#
#     message = f'Ваш код авторизации на форуме: \n' \
#               f'{usercode.code}'
#     send_mail(
#         f'Код авторизации пользователя',
#         message,
#         settings.DEFAULT_FROM_EMAIL,
#         [request.user.email],
#     )
#     return redirect('onetimecode')
#
#
# def login_view(request):
#     if request.method == 'POST':
#         if request.user.is_active:
#             form = LoginUserForm(request.POST)
#             if form.is_valid():
#                 cd = form.cleaned_data
#                 user = authenticate(request, email=cd['email'],
#                                     password=cd['password'])
#                 login(request, user)
#                 return redirect('home')
#         else:
#             return redirect('onetimecode')
#     else:
#         form = LoginUserForm()
#         return render(request, 'account/login.html', {'form': form})


# class LoginUser(LoginView):
#     form_class = LoginUserForm
#     template_name = 'account/login.html'
#     extra_context = {'title': 'Авторизация'}


# class RegisterView(CreateView):
#     form_class = RegisterUserForm
#     template_name = 'account/register.html'
#     extra_context = {'title': 'Регистрация'}
#     success_url = 'account/register'