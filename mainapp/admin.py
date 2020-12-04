from django.forms import ModelChoiceField, ModelForm, ValidationError
from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import *
from PIL import Image






class LaptopAdminForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(LaptopAdminForm, self).__init__(*args, **kwargs)
        self.MIN_RESOLUTION = Product.MIN_RESOLUTION
        self.MAX_RESOLUTION = Product.MAX_RESOLUTION
        self.MAX_SIZE = Product.MAX_SIZE
        self.fields['image'].help_text = mark_safe(f'<span style="color:green; font-size:14px;">'
                                                   f'Загружайте изображение с минимальным разрешением:'
                                                   f' {self.MIN_RESOLUTION[0]}x{self.MIN_RESOLUTION[1]}'
                                                   f' и максимальным разрешением: {self.MAX_RESOLUTION[0]}'
                                                   f'x{self.MAX_RESOLUTION[1]}; \n'
                                                   f'Размер изображения не должен превышать '
                                                   f'{self.MAX_SIZE / (1024 * 1024)} Мб</span>')

    #                                            перевод байтов в мегабайты ^

    def clean_image(self):
        image = self.cleaned_data['image']
        img = Image.open(image)
        self.__img_size_check(img, image)
        return image

    def __is_img_smaller_than_min(self, img):
        if img.width < self.MIN_RESOLUTION[0] or img.height < self.MIN_RESOLUTION[1]:
            return True

    def __is_img_bigger_than_max(self, img):
        if img.width > self.MAX_RESOLUTION[0] or img.height > self.MAX_RESOLUTION[1]:
            return True

    def __is_img_size_bigger_than_max(self, image):
        if image.size > self.MAX_SIZE:
            return True

    def __img_size_check(self, img, image):
        if self.__is_img_smaller_than_min(img):
            raise ValidationError("Разрешение изображения меньше минимального")
        if self.__is_img_bigger_than_max(img):
            raise ValidationError("Разрешение изображения больше максимального")
        if self.__is_img_size_bigger_than_max(image):
            raise ValidationError("Размер изображения больше максимального")


# при попытке создания продукта типа ноутбук блокирует выставление ему опций отличных от категории: ноутбуки
class LaptopAdmin(admin.ModelAdmin):
    form = LaptopAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='laptops'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class SmartphoneAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='smartphones'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


# Регистрация моделей
# Product не регестрируем т.к. это мета класс

admin.site.register(Category)
admin.site.register(Customers)
admin.site.register(CartProduct)
admin.site.register(Cart)
admin.site.register(Laptop, LaptopAdmin)
admin.site.register(Smartphone, SmartphoneAdmin)
