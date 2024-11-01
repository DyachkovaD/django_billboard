from django.contrib.auth.views import LogoutView
from django.urls import path
from account.views import *



urlpatterns = [
    path('', IndexView.as_view(), name='account'),
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('onetimecode/', login_with_code_view, name='onetimecode'),
]