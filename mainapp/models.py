from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

User = get_user_model()  # говорим джанго что хотим использовать своего пользователся(покупателя)


# В данном файле каждого приложения веб сервара создаются модели хранимых данных в ООП стиле,
# после чего django автоматически формирует запросы к базамм данных и настраивает их в соответсвтии
# ранее введенными моделями.

# Необходимые таблицы:
#   Product
#   Cart_Product
#   Category
#   Cart
#   Order
#   Customer
#   Specification

class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name="Имя категории")  # verbose_name - имя в админке
    slug = models.SlugField(unique=True)  # Поле - метка, используется для указания URL

    def __str__(self):
        return self.name


# -------------------------------------------------------------------------------------------------------------------- #
class Product(models.Model):
    class Meta:
        abstract = True

    category = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name="Наименование")
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name="Изображение")
    description = models.TextField(null=True, verbose_name="Описание")
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="Цена")

    def __str__(self):
        return self.title


class Laptop(Product):
    diagonal = models.CharField(max_length=40, verbose_name="Диагональ")
    display_type = models.CharField(max_length=255, verbose_name="Тип дисплея")
    processor_frequency = models.CharField(max_length=255, verbose_name="Частота процессора")
    ram = models.CharField(max_length=255, verbose_name="Оперативная память")
    graphics_card = models.CharField(max_length=255, verbose_name="Видеокарта")
    time_without_charge = models.CharField(max_length=255, verbose_name="Время работы без подзарядки")

    def __str__(self):
        return f'{self.category.name}:{self.title}'


class Smartphone(Product):
    diagonal = models.CharField(max_length=40, verbose_name="Диагональ")
    display_type = models.CharField(max_length=255, verbose_name="Тип дисплея")
    resolution = models.CharField(max_length=255, verbose_name="Разрешение экрана")
    ram = models.CharField(max_length=255, verbose_name="Оперативная память")
    have_sd = models.BooleanField(default=True)
    sd_volume_max = models.CharField(max_length=255, verbose_name="Максимальный объем встраиваемой памяти")
    accum_volume = models.CharField(max_length=255, verbose_name="Объем аккамулятора")
    main_cam = models.CharField(max_length=255, verbose_name="Главная камера")
    frontal_cam = models.CharField(max_length=255, verbose_name="Фронтальная")

    def __str__(self):
        return f'{self.category.name}:{self.title}'


# -------------------------------------------------------------------------------------------------------------------- #
class CartProduct(models.Model):
    user = models.ForeignKey('Customers', verbose_name="Покупатель", on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name="Корзина", on_delete=models.CASCADE, related_name="related_products")
    # product = models.ForeignKey(Product, verbose_name="Продукт", on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # ContentType - видит все модели созданные внутри прокета
    object_id = models.PositiveIntegerField()
    # Id конкретной модели
    content_object = GenericForeignKey('content_type', 'object_id')

    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="Общая цена")

    def __str__(self):
        return f'Продукт: {self.product.title} (для корзины)'


class Cart(models.Model):
    owner = models.ForeignKey('Customers', verbose_name="Владелец", on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, blank=True, related_name="related_card")
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="Общая цена")

    def __str__(self):
        return f"Корзина покупателя {str(self.owner)}, с продуктами {str(self.products)}, по цене {self.final_price}"


class Customers(models.Model):
    user = models.ForeignKey(User, verbose_name="Покупатель", on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name="Номер телефона")
    address = models.CharField(max_length=255, verbose_name="Адрес")

    def __str__(self):
        return f"Покупатель: {self.user.first_name} {self.user.last_name}"

# class Specifications(models.Model):  # Характеристики
#     content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
#     object_id = models.PositiveIntegerField()
#     name = models.CharField(max_length=255, verbose_name="Имя товара для характеристик")
#
#     def __str__(self):
#         return f"Характеристики для товара: {self.name}"
