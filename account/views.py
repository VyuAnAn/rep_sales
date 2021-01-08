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


# def user_login(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(
#                 request,
#                 username=cd['username'],
#                 password=cd['password']
#             )
#             if user is not None:
#                 if user.is_active:
#                     login(request, user)
#                     return HttpResponse('Аутентификация прошла успешно')
#                 else:
#                     return HttpResponse('Учетная запись отключена')
#             else:
#                 return HttpResponse('Некорректный логин')
#     else:
#         form = LoginForm()
#     return render(request, 'account/login.html', {'form': form})
#
#

# @login_required
# def user_list(request):
#     users = User.objects.filter(is_active=True)
#     return render(request,
#                   'account/user/list.html',
#                   {'section': 'people',
#                    'users': users})
#
#
# @login_required
# def user_detail(request, username):
#     user = get_object_or_404(
#         User,
#         username=username,
#         is_active=True
#     )
#
#     return render(request,
#                   'account/user/detail.html',
#                   {'section': 'people',
#                    'user': user})
#
#
# @ajax_required
# @require_POST
# @login_required
# def user_follow(request):
#     user_id = request.POST.get('id')
#     action = request.POST.get('action')
#     if user_id and action:
#         try:
#             user = User.objects.get(id=user_id)
#             if action == 'follow':
#                 Contact.objects.get_or_create(user_from=request.user, user_to=user)
#                 create_action(request.user, ' подписался на ', user)
#             else:
#                 Contact.objects.filter(user_from=request.user, user_to=user).delete()
#             return JsonResponse({'status': 'ok'})
#         except User.DoesNotExist:
#             return JsonResponse({'status': 'ok'})
#     return JsonResponse({'status': 'ok'})
