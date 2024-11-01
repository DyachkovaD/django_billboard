from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from account.models import OneTimeCode
from django.conf import settings


class LoginUserForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['email', 'password']


class RegisterUserForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password']

    def email_uniqe(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с таким email уже существует')
        return email


class OneTimeCodeForm(forms.Form):
    code = forms.CharField(label='Код подтверждения')
    username = forms.CharField(label='Логин',
                               widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    def clean(self):
        cleaned_data = super().clean()
        code = cleaned_data.get('code')
        if OneTimeCode.objects.get(code=code):
            return cleaned_data
        else:
            raise forms.ValidationError('Неверный код')

# class OneTimeCodeForm(forms.ModelForm):
#     code = forms.CharField(label='Код подтверждения')
#
#     class Meta:
#         model = get_user_model(),
#         fields = ['email', 'password']
#
#     def clean(self):
#         cleaned_data = super(OneTimeCodeForm, self).clean()
#         code = cleaned_data.get('code')
#         if OneTimeCode.objects.get(code=code):
#             print('code here')
#             return cleaned_data
#         else:
#             raise forms.ValidationError('Неверный код')



# class LoginUserForm(AuthenticationForm):
#     class Meta:
#         model = get_user_model()
#         fields = ['email', 'password']

# class RegisterUserForm(UserCreationForm):
#     username = forms.CharField(label="Логин", widget=forms.TextInput(attrs={'class': 'form-input'}))
#     password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput)
#     password2 = forms.CharField(label="Повтор пароля", widget=forms.PasswordInput)
#
#     class Meta:
#         model = get_user_model()
#         fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
#         labels = {
#             'first_name': 'Имя',
#             'last_name': 'Фамилия',
#         }
#         widgets = {
#             'first_name': forms.TextInput(attrs={'class': 'form-input'}),
#             'last_name': forms.TextInput(attrs={'class': 'form-input'}),
#         }
#
#     def email_uniqe(self):
#         email = self.cleaned_data['email']
#         if get_user_model().objects.filter(email=email).exists():
#             raise forms.ValidationError('Пользователь с таким email уже существует')
#         return email