import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from records.models import Category, SalesLogDetail, Product, GroupProduct, ProductInfo

""" Журнал продаж """
now = datetime.datetime.now()


@login_required
def sales_log(request, year=now.year, month=now.month, day=now.day):
    section = 'sales_log'
    logs = SalesLogDetail.objects.filter(sales_log__created__year=year,
                                         sales_log__created__month=month,
                                         sales_log__created__day=day)
    return render(request,
                  'sales_logs/sales_log.html',
                  {'logs': logs,
                   'section': section})


""" Интернет-магазин """


@login_required
def shop(request, category_id=None):
    """ Главная страница интернет-магазина """
    section = 'shop'
    categories = Category.objects.filter(active=True)
    info_products = ProductInfo.objects.all()

    if category_id:
        info_products = ProductInfo.objects.filter(group_product__category=category)

    return render(request,
                  'catalog/product/index.html',
                  {'categories': categories,
                   'info_products': info_products,
                   'section': section})


@login_required
def product_detail(request, group_id, vendor_code):
    """ Информация по группе товаров"""
    section = 'shop'
    group_product = get_object_or_404(GroupProduct, id=group_id)
    info_products = ProductInfo.objects.filter(group_product=group_product)
    return render(request,
                  'catalog/product/product_detail.html',
                  {'group_product': group_product,
                   'vendor_code': vendor_code,
                   'info_products': info_products,
                   'section': section})





