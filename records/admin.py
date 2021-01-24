from django.contrib import admin

from records.models import Category, GroupProduct, ProductInfo, Product, Parameter, ProductParameter, SalesLog, \
    SalesLogDetail, Image


class SalesLogDetailInline(admin.TabularInline):
    model = SalesLogDetail
    raw_id_fields = ['sales_log']


@admin.register(SalesLog)
class SalesLogAdmin(admin.ModelAdmin):
    list_display = ['created', 'shop', 'seller', 'customer', 'comment']
    list_filter = ['created', 'shop', 'seller']
    inlines = [SalesLogDetailInline]
    date_hierarchy = 'created'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    list_filter = ['name']
    search_fields = ('name',)
    # prepopulated_fields = {'slag': ('name', )}
    # list_editable = ['name']  # позволяет изменять не переходя к списку


@admin.register(Parameter)
class ParameterAdmin(admin.ModelAdmin):
    list_display = ['value', 'parameter', 'display_tag', 'display_label']
    list_filter = ['value']
    search_fields = ('value',)


class ProductInfoInline(admin.TabularInline):
    model = ProductInfo
    raw_id_fields = ['group_product']


@admin.register(GroupProduct)
class GroupProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'description', 'created', 'updated', 'active']
    list_filter = ['name', 'category', 'created', 'updated', 'active']
    search_fields = ('name',)
    inlines = [ProductInfoInline]
    date_hierarchy = 'created'
    # ordering = ('status', 'publish')


class ProductParameterInline(admin.TabularInline):
    model = ProductParameter
    raw_id_fields = ['product']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['quantity']
    inlines = [ProductParameterInline]
    date_hierarchy = 'created'
    # ordering = ('status', 'publish')


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['image', 'main', 'product_info']
