from django.contrib import admin

from records.models import Category, GroupProduct, Product, Parameter, ProductParameter


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    list_filter = ['name']
    search_fields = ('name',)
    # prepopulated_fields = {'slag': ('name', )}
    # list_editable = ['name']  # позволяет изменять не переходя к списку


@admin.register(Parameter)
class ParameterAdmin(admin.ModelAdmin):
    list_display = ['value', 'parameter', 'category']
    list_filter = ['value']
    search_fields = ('value',)


class ProductInline(admin.TabularInline):
    model = Product
    raw_id_fields = ['group_product']


@admin.register(GroupProduct)
class GroupProductAdmin(admin.ModelAdmin):
    list_display = ['vendor_code', 'name', 'category', 'description', 'created', 'updated', 'active']
    list_filter = ['name', 'category', 'created', 'updated', 'active']
    search_fields = ('vendor_code', 'name')
    inlines = [ProductInline]
    date_hierarchy = 'created'
    # ordering = ('status', 'publish')


class ProductParameterInline(admin.TabularInline):
    model = ProductParameter
    raw_id_fields = ['product']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['group_product', 'purchase_price', 'price', 'created',
                    'updated', 'active', 'available', 'quantity']
    inlines = [ProductParameterInline]
    date_hierarchy = 'created'
    # ordering = ('status', 'publish')


