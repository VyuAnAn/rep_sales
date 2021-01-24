from django.db import models
from django.urls import reverse

from account.models import Profile


class Category(models.Model):
    """ Категория товара """
    name = models.CharField(max_length=250,
                            verbose_name='Наименование категории')
    # slag - потом
    active = models.BooleanField(default=True,
                                 verbose_name='Активность категории')

    # внешние ключики
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

    def get_absolute_url(self):
        return reverse('records:shop', args=[self.id])


class GroupProduct(models.Model):
    """ Группировка товаров """
    name = models.CharField(max_length=250,
                            verbose_name='Наименование товара')
    # slag = models.SlagField()
    description = models.CharField(max_length=1000,
                                   verbose_name='Описание товара')

    created = models.DateTimeField(auto_now_add=True,
                                   verbose_name='Дата добавления')

    updated = models.DateTimeField(auto_now=True,
                                   verbose_name='Дата обновления')

    active = models.BooleanField(verbose_name='Активность товара',
                                 default=True)

    # внешние ключики
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


class ProductInfo(models.Model):
    """ Информаия по товару """
    vendor_code = models.CharField(max_length=15,
                                   verbose_name='Артикул')
    created = models.DateTimeField(auto_now_add=True,
                                   verbose_name='Дата добавления')
    updated = models.DateTimeField(auto_now=True,
                                   verbose_name='Дата обновления')
    active = models.BooleanField(verbose_name='Товар активен',
                                 default=True)
    # available = models.BooleanField(verbose_name='Товар в наличии',
    #                                 default=True)

    purchase_price = models.DecimalField(max_digits=10,
                                         decimal_places=0,
                                         verbose_name='Закупочная стоимость товара')

    price = models.DecimalField(max_digits=10,
                                decimal_places=0,
                                verbose_name='Цена')

    # внешние ключики
    group_product = models.ForeignKey(GroupProduct,
                                      blank=True,
                                      null=True,
                                      on_delete=models.CASCADE,
                                      related_name='group_products',
                                      related_query_name='group_product',
                                      verbose_name='Группы товаров')

    class Meta:
        verbose_name = 'Информация по товару'
        verbose_name_plural = 'Информация по товарам'

    def __str__(self):
        return '{} по {}р. арт {}'\
            .format(self.group_product.name, self.price, self.vendor_code)

    def get_absolute_url(self):
        """ Абсолютный путь """
        return reverse('records:product_info', args=[self.group_product.id, self.vendor_code])

    def show_main_image(self):
        """ Получить основное изображение """
        image = Image.objects.get(main=True,
                                  product_info__id=self.id)
        return image.image.url if image else False


class Product(models.Model):
    """ Товар """
    quantity = models.IntegerField(verbose_name='Количество',
                                   default=1)

    created = models.DateTimeField(auto_now_add=True,
                                   verbose_name='Дата добавления')
    updated = models.DateTimeField(auto_now=True,
                                   verbose_name='Дата обновления')
    active = models.BooleanField(verbose_name='Товар активен',
                                 default=True)

    # внешние ключики
    product_info = models.ForeignKey(ProductInfo,
                                     blank=True,
                                     null=True,
                                     on_delete=models.CASCADE,
                                     related_name='product_info',
                                     related_query_name='products_info',
                                     verbose_name='Информация по товару')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.product_info.__str__()


class Parameter(models.Model):
    """ Параметры """
    value = models.CharField(max_length=100,
                             verbose_name='Значение параметра')

    display_tag = models.CharField(max_length=100,
                                   verbose_name='Тэг',
                                   blank=True,
                                   null=True,
                                   )
    display_label = models.CharField(max_length=100,
                                     verbose_name='Отображение параметра',
                                     blank=True,
                                     null=True,
                                     )
    parameter = models.ForeignKey('self',
                                  on_delete=models.CASCADE,
                                  blank=True,
                                  null=True,
                                  related_name='parameter_parameters',
                                  related_query_name='parameter_parameter',
                                  verbose_name='Набор')

    class Meta:
        verbose_name = 'Параметр'
        verbose_name_plural = 'Параметры'

    def __str__(self):
        return self.value


class ProductParameter(models.Model):
    """ Комбинации параметров товара """
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
        verbose_name = 'Комбинация параметров товара'
        verbose_name_plural = 'Комбинации параметров  товаров'
        index_together = (('product', 'parameter'),)


class Image(models.Model):
    """ Изображения товара"""
    image = models.ImageField(upload_to='products/%Y/%m/%d',
                              verbose_name="Изображение")

    main = models.BooleanField(default=False,
                               verbose_name="Главное изображение")

    product_info = models.ForeignKey(ProductInfo,
                                     blank=True,
                                     null=True,
                                     related_name='images',
                                     related_query_name='image',
                                     on_delete=models.CASCADE,
                                     verbose_name='Товары')

    class Meta:
        verbose_name = 'Изображение товара'
        verbose_name_plural = 'Изображения товара'


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
                                decimal_places=0,
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
