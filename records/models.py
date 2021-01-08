from django.db import models

from account.models import Profile


class Category(models.Model):
    """ Категория товара """
    name = models.CharField(max_length=250,
                            verbose_name='Наименование категории')
    # slag
    active = models.BooleanField(default=True,
                                 verbose_name='Активность категории')

    category = models.ForeignKey('self',
                                 on_delete=models.CASCADE,
                                 blank=True,
                                 null=True,
                                 related_name='category_categories',
                                 related_query_name='category_category',
                                 verbose_name='Категория')

    class Meta:
        ordering = ('name', )
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории товаров'

    def __str__(self):
        return self.name


class GroupProduct(models.Model):
    """ Группа товаров """
    name = models.CharField(max_length=250,
                            verbose_name='Наименование группы товаров')
    # slag = models.SlagField()
    description = models.CharField(max_length=1000,
                                   verbose_name='Описание группы товаров')
    vendor_code = models.CharField(max_length=15,
                                   verbose_name='Артикул')
    created = models.DateTimeField(auto_now_add=True,
                                   verbose_name='Дата добавления')
    updated = models.DateTimeField(auto_now=True,
                                   verbose_name='Дата обновления')
    active = models.BooleanField(verbose_name='Группа активна',
                                 default=True)

    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE,
                                 related_name='product_categories',
                                 related_query_name='product_category',
                                 verbose_name='Категория товаров')

    class Meta:
        verbose_name = 'Группа товаров'
        verbose_name_plural = 'Группы товаров'

    def __str__(self):
        return self.name


class Product(models.Model):
    """ Товар """
    purchase_price = models.DecimalField(max_digits=10,
                                         decimal_places=2,
                                         verbose_name='Закупочная стоимость товара')
    price = models.DecimalField(max_digits=10,
                                decimal_places=2,
                                verbose_name='Цена')
    created = models.DateTimeField(auto_now_add=True,
                                   verbose_name='Дата добавления')
    updated = models.DateTimeField(auto_now=True,
                                   verbose_name='Дата обновления')
    active = models.BooleanField(verbose_name='Товар активен',
                                 default=True)
    available = models.BooleanField(verbose_name='Товар в наличии',
                                    default=True)
    quantity = models.IntegerField(verbose_name='Количество',
                                   default=1)

    group_product = models.ForeignKey(GroupProduct,
                                      on_delete=models.CASCADE,
                                      related_name='group_products',
                                      related_query_name='group_product',
                                      verbose_name='Группы товаров')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return '{} по {}р. (всего на складе {})'\
            .format(self.group_product.name, self.price, self.quantity)


class Parameter(models.Model):
    """ Набор характеристик """
    value = models.CharField(max_length=100,
                             verbose_name='Значение параметра')

    parameter = models.ForeignKey('self',
                                  on_delete=models.CASCADE,
                                  blank=True,
                                  null=True,
                                  related_name='parameter_parameters',
                                  related_query_name='parameter_parameter',
                                  verbose_name='Набор')

    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE,
                                 blank=True,
                                 null=True,
                                 related_name='parameter_categories',
                                 related_query_name='parameter_category',
                                 verbose_name='Категория'
                                 )

    class Meta:
        verbose_name = 'Набор характеристик'
        verbose_name_plural = 'Наборы характеристик'

    def __str__(self):
        return self.value


class ProductParameter(models.Model):
    """ Характеристики товара """
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                related_name='product_parameter_products',
                                related_query_name='product_parameter_product',
                                verbose_name='Товары')

    parameter = models.ForeignKey(Parameter,
                                  on_delete=models.CASCADE,
                                  related_name='product_parameter_parameters',
                                  related_query_name='product_parameter_parameter',
                                  verbose_name='Характеристики')

    class Meta:
        verbose_name = 'Характеристики товара'
        verbose_name_plural = 'Характеристики товаров'
        index_together = (('product', 'parameter'),)


# class Image(models.Model):
#     """ Изображения """
#     path = models.CharField(max_length=350)
#
#     class Meta:
#         verbose_name = 'Изображение'
#         verbose_name_plural = 'Изображения'
#
#
# class ProductImage(models.Model):
#     """ Изображения товара """
#     product = models.ForeignKey(Product,
#                                 related_name='products',
#                                 on_delete=models.CASCADE,
#                                 verbose_name='Товары')
#
#     image = models.ForeignKey(Product,
#                               related_name='images',
#                               on_delete=models.CASCADE,
#                               verbose_name='Изображения')

class SalesLog(models.Model):
    """ Журнал продаж """
    created = models.DateTimeField(auto_now_add=True,
                                   verbose_name='Дата создания записи')
    comment = models.CharField(max_length=1500,
                               blank=True,
                               null=True,
                               verbose_name="Комментарий")

    seller = models.ForeignKey(Profile,
                               blank=True,
                               null=True,
                               on_delete=models.CASCADE,
                               related_name='seller_profiles',
                               related_query_name='seller_profile',
                               verbose_name='Продавец')

    customer = models.ForeignKey(Profile,
                                 blank=True,
                                 null=True,
                                 on_delete=models.CASCADE,
                                 related_name='customer_profiles',
                                 related_query_name='customer_profile',
                                 verbose_name='Покупатель')

    SHOP_CHOICES = [
        ('B', 'BlossomShop'),
        ('K', 'Kokos'),
        ('OS', 'Online store'),
    ]

    shop = models.CharField(
        max_length=2,
        choices=SHOP_CHOICES,
        default='OS'
    )

    class Meta:
        verbose_name = 'Продажи'
        verbose_name_plural = 'Продажи'


class SalesLogDetail(models.Model):
    """ Детали продаж """
    price = models.DecimalField(max_digits=10,
                                decimal_places=2,
                                verbose_name='Цена товара')

    quantity = models.IntegerField(default=1)

    comment = models.CharField(max_length=1500,
                               blank=True,
                               null=True,
                               verbose_name="Комментарий")

    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                related_name='detail_products',
                                related_query_name='detail_product',
                                verbose_name='Товары')

    sales_log = models.ForeignKey(SalesLog,
                                  on_delete=models.CASCADE,
                                  related_name='sales_logs',
                                  related_query_name='sales_log',
                                  verbose_name='Журнал')

    class Meta:
        verbose_name = 'Детали по журналу продаж'
        verbose_name_plural = 'Детали по журналу продаж'
