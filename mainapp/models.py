from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from PIL import Image
from django.urls import reverse

User = get_user_model()  # говорим джанго что хотим использовать своего пользователся(покупателя)


def get_product_url(obj, view_name):
    ct_object = obj.__class__._meta.model_name
    return reverse(view_name, kwargs={'ct_model': ct_object, 'slug': obj.slug})


class MinResolutionErrorException(Exception):
    pass


class MaxResolutionErrorException(Exception):
    pass


class MaxSizeErrorException(Exception):
    pass


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
    MAX_RESOLUTION = (2000, 2000)
    MIN_RESOLUTION = (400, 400)
    MAX_SIZE = 3145728

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

    def save(self, *args, **kwargs):
        img = Image.open(self.image)
        self.__img_size_check(img)
        super().save(*args, **kwargs)

    def __is_img_smaller_than_min(self, img):
        if img.width < self.MIN_RESOLUTION[0] or img.height < self.MIN_RESOLUTION[1]:
            return True

    def __is_img_bigger_than_max(self, img):
        if img.width > self.MAX_RESOLUTION[0] or img.height > self.MAX_RESOLUTION[1]:
            return True

    def __is_img_size_bigger_than_max(self, image):
        if image.size > self.MAX_SIZE:
            return True

    def __img_size_check(self, img):
        if self.__is_img_smaller_than_min(img):
            raise MinResolutionErrorException("Разрешение изображения меньше минимального")
        if self.__is_img_bigger_than_max(img):
            raise MaxResolutionErrorException("Разрешение изображения больше максимального")
        if self.__is_img_size_bigger_than_max(self.image):
            raise MaxSizeErrorException("Размер изображения больше максимального")


class Laptop(Product):
    diagonal = models.CharField(max_length=40, verbose_name="Диагональ")
    display_type = models.CharField(max_length=255, verbose_name="Тип дисплея")
    processor_frequency = models.CharField(max_length=255, verbose_name="Частота процессора")
    ram = models.CharField(max_length=255, verbose_name="Оперативная память")
    graphics_card = models.CharField(max_length=255, verbose_name="Видеокарта")
    time_without_charge = models.CharField(max_length=255, verbose_name="Время работы без подзарядки")

    def __str__(self):
        return f'{self.category.name}:{self.title}'

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')


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

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')


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


class LatestProductsManager:
    # Выбираем пять моделей для отображения на главной странице
    @staticmethod
    def get_products_for_main_page(self, *args, **kwargs):
        with_respect_to = kwargs.get('with_respect_to')
        products = []
        ct_models = ContentType.objects.filter(model__in=args)
        for ct_model in ct_models:
            model_products = ct_model.model_class()._base_manager.all().order_by('-id')[:5]
            products.extend(model_products)
        if with_respect_to:
            ct_model = ContentType.objects.filter(model=with_respect_to)  # ContentType все таблицы базы данных,
            # objects - объекты, filter - фильтр по... model - конкретной модели
            if ct_model.exist():
                if with_respect_to in args:
                    return sorted(products,
                                  key=(lambda x: x.__class__._meta.model_name.startswith(with_respect_to)),
                                  reverse=True
                                  )

        return products


class LatestProducts:
    object = LatestProductsManager()
