from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from account.forms import UserRegistrationForm, ChangeProfileForm


def register(request):
    """ Регистрация нового пользователя """
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)

        if user_form.is_valid():
            # Создаем нового пользователя, но пока не сохраняем в базу данных.
            new_user = user_form.save(commit=False)
            # Задаем пользователю зашифрованный пароль.
            new_user.set_password(user_form.cleaned_data['password'])

            # Создание профиля пользователя.
            # Profile.objects.create(user=new_user)
            # create_action(new_user, 'создан аккаунт')
            # Сохраняем пользователя в базе данных.
            new_user.save()

            return render(request,
                          'account/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()

    return render(request,
                  'account/register.html',
                  {'user_form': user_form})


# @login_required
# def profile(request):
#     if request.method == 'GET':
#         user_form = ProfileForm(instance=request.user)
#     else:
#         user_form = ProfileForm(instance=request.user,
#                                 data=request.POST)
#     return render(request,
#                   "account/profile.html",
#                   {"user_form": user_form})


@login_required
def change_profile(request):
    if request.method == 'POST':
        user_form = ChangeProfileForm(instance=request.user,
                                      data=request.POST,
                                      files=request.FILES)

        if user_form.is_valid():
            user_form.save()
            # messages.success(request, 'Профиль успешно обновлен')
        # else:
            # messages.error(request, 'Ошибка обновления профиля')
    else:
        user_form = ChangeProfileForm(instance=request.user)
    return render(request,
                  'account/change_profile.html',
                  {'user_form': user_form})