from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from records.models import Category


@login_required
def index(request):
    section = 'shop'
    categories = Category.objects.filter(active=True)
    return render(request,
                  'catalog/product/index.html',
                  {'categories': categories,
                   'section': section})
