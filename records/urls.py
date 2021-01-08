from django.urls import path

from records import views

app_name = 'records'

urlpatterns = [
    path('sales_log/', views.sales_log, name='sales_log'),
    path('sales_log/<int:year>/<int:month>/<int:day>', views.sales_log, name='sales_log'),
    path('shop/', views.shop, name='shop')
]