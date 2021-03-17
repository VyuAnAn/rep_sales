from django.urls import path

from records import views

app_name = 'records'

urlpatterns = [
    # Журнал продаж
    path('sales_log/', views.sales_log, name='sales_log'),
    path('sales_log/<int:year>/<int:month>/<int:day>', views.sales_log, name='sales_log'),
    path('sales_log/sell', views.sell, name='sell'),

    # Интернет-магазин
    path('shop/', views.shop, name='shop'),
    path('shop/<int:category_id>', views.shop, name='shop'),
    path('shop/detail/<int:group_id>/<str:vendor_code>/', views.product_detail, name='product_info'),
    # path('shop/detail_product/', views.get_product, name='get_product'),
]