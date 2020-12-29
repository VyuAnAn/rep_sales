from django.urls import path

from records import views

app_name = 'records'

urlpatterns = [
    path('', views.index, name='index')
]