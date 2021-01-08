import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from records.models import Category, SalesLogDetail


@login_required
def shop(request):
    section = 'shop'
    categories = Category.objects.filter(active=True)
    return render(request,
                  'catalog/product/index.html',
                  {'categories': categories,
                   'section': section})


now = datetime.datetime.now()


@login_required
def sales_log(request, year=now.year, month=now.month, day=now.day):
    section = 'sales_log'
    logs = SalesLogDetail.objects.filter(sales_log__created__year=year,
                                         sales_log__created__month=month,
                                         sales_log__created__day=day)
    return render(request,
                  'catalog/product/sales_log.html',
                  {'logs': logs,
                   'section': section})

