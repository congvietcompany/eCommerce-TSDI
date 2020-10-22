import datetime

from django.urls import reverse
from django.contrib import admin
from .models import Order, OrderItem
from django.utils.safestring import mark_safe
from django.core.mail import send_mail
from django.template.loader import render_to_string


# Register your models here.
def order_name(obj):
    return '%s %s' % (obj.first_name, obj.last_name)


order_name.short_desciption = 'Name'


def order_pdf(obj):
    return mark_safe('<a href="{}">PDF</a>'.format(reverse('admin_order_pdf', args=[obj.id])))


order_name.short_desciption = 'PDF Title'


class OrderItemInLine(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


def admin_order_shipped(modeladmin, request, queryset):
    for order in queryset:
        order.shipped_date = datetime.datetime.now()
        order.status = Order.SHIPPED
        order.save()

        #html = render_to_string('order_sent.html', {'order': order})
        #send_mail('Order Sent', 'Your order has been sent !', 'truongtran@tsdinternational.com.vn', ['truongtran@tsdinternational.com.vn', order.email], fail_silently=False, html_message=html)

    return


admin_order_shipped.short_description = 'Set shipped'


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', order_name, 'status', 'created_at', order_pdf]
    list_filter = ['created_at', 'status']
    search_fields = ['first_name', 'address']
    inlines = [OrderItemInLine]
    actions = [admin_order_shipped]


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)