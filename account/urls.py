from django.urls import path, include
from django.contrib.auth import views as auth_views

# app_name = 'account'

from account import views
from records import views as rec_views

urlpatterns = [
    # Обработчик
    path('', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    # Главная интернет-магазина
    path('', rec_views.index, name='index'),

    # Страница входа
    # path('login/', auth_views.LoginView.as_view(), name='login'),
    # Страница выхода
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Шаблоны для доступа к обработчикам смены пароля.
    # path('password_change/', auth_views.PasswordChangeView.as_view(),
    #      name='password_change'),
    # path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(),
    #      name='password_change_done'),

    # Обработчики восстановления пароля.
    # path('password_reset/', auth_views.PasswordResetView.as_view(),
    #      name='password_reset'),
    # path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(),
    #      name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
    #      name='password_reset_confirm'),
    # path('reset/done/', auth_views.PasswordResetCompleteView.as_view(),
    #      name='password_reset_complete'),
]
