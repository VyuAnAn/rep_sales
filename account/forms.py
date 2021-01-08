from django import forms
# from django.contrib.auth.models import User
from account.models import Profile


class ChangeProfileForm(forms.ModelForm):
    """ Изменить профиль пользователя """
    # email = forms.EmailField(required=True,
    #                          label="Адрес электронной почты")

    class Meta:
        model = Profile
        fields = ('username', 'first_name', 'last_name',
                  'email', 'date_of_birth', 'phone_number', 'send_messages')


class UserRegistrationForm(forms.ModelForm):
    """ Зарегистрировать пользователя"""
    password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль',
                                widget=forms.PasswordInput)

    class Meta:
        model = Profile
        fields = ('username', 'first_name', 'last_name',
                  'email', 'date_of_birth',
                  'phone_number', 'send_messages')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают.')
        return cd['password2']

