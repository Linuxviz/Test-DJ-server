from django.forms import ModelChoiceField
from django.contrib import admin
from .models import *


# class LaptopCategoryChooseField(forms.ModelChoiceField):
#     pass

# при попытке создания продукта типа ноутбук блокирует выставление ему опций отличных от категория: ноутбук
class LaptopAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='laptops'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


# class SmartphoneCategoryChooseField(forms.ModelChoiceField):
#     pass


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
