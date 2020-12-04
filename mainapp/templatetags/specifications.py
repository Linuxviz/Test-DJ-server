from django import template
from django.utils.safestring import mark_safe
register = template.Library()

TABLE_HEAD = """
    <table class="table table-striped">
  <tbody>
"""
TABLE_TAIL = """
  </tbody>
    </table>
"""
TABLE_CONTENT = """
        <tr>
            <td>{name}</td>
            <td>{value}</td>
        </tr>
"""

PRODUCT_SPEC = {
    'laptop': {
        'Диагональ': 'diagonal',
        'Тип дисплея': 'display_type',
        'Частота процессора': 'processor_frequency',
        'Оперативная память': 'ram',
        'Видеокарта': 'graphics_card',
        'Время работы без подзарядки': 'time_without_charge',
    },
    'smartphone': {
        'Диагональ': 'diagonal',
        'Тип дисплея': 'display_type',
        'Разрешение': 'resolution',
        'Оперативная память': 'ram',
        'Наличие СД карты': 'have_sd',
        'Макимальная ёмкость СД карты': 'sd_volume_max',
        'Ёмкость аккамулятора': 'accum_volume',
        'Главная камера': 'main_cam',
        'Фронтальная камера': 'frontal_cam',

    }
}


def get_product_spec(product, model_name):
    table_content = ''
    for name, value in PRODUCT_SPEC[model_name].items():
        table_content += TABLE_CONTENT.format(name=name, value=getattr(product, value))
    return table_content


@register.filter
def product_spec(product):
    model_name = product.__class__._meta.model_name
    return mark_safe(f'{TABLE_HEAD}{get_product_spec(product, model_name)}{TABLE_TAIL}')
