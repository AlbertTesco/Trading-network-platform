from django.contrib import admin
from django.utils.html import format_html

from trading_platform.models import NetworkNode, Product


"""
Django Admin Model for NetworkNode
"""
from django.contrib import admin
from django.utils.html import format_html

from trading_platform.models import NetworkNode, Product


@admin.register(NetworkNode)
class NetworkNodeAdmin(admin.ModelAdmin):
    """
    Django Admin Model for NetworkNode
    """
    list_display = (
        'id', 'name', 'level', 'email', 'city', 'street', 'house_number', 'node_type', 'supplier_link', 'debt',
        'created_at',
        'object_link')
    list_filter = ('city',)
    actions = ['clear_debt']

    def supplier_link(self, obj):
        """
        Returns a link to the Supplier of the given NetworkNode
        """
        if obj.supplier:
            url = f"/platform/network-node/{obj.supplier.pk}"
            return format_html('<a href="{}">{}</a>', url, obj.supplier.name)
        return '-'

    supplier_link.short_description = 'Поставщик'
    supplier_link.allow_tags = True

    def object_link(self, obj):
        """
        Returns a link to the detail page of the given NetworkNode
        """
        url = f"/platform/network-node/{obj.pk}/"
        return format_html('<a href="{}">{}</a>', url, "Страница объекта")

    object_link.short_description = 'Страница объекта'
    object_link.allow_tags = True

    @admin.action(description='Очистить задолженность перед поставщиком')
    def clear_debt(self, request, queryset):
        """
        Clears the debt of the selected NetworkNodes and displays a message
        """
        queryset.update(debt=0)
        self.message_user(request, "Задолженность очищена у выбранных объектов.")


admin.site.register(Product)
