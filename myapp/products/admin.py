from django.contrib import admin
from .models import *


# Register your models here.
class CategoryAdmin(admin.ModelAdmin):

    list_display = ['name', 'available', 'feature', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    change_form_template = 'admin/category/edit.html'
    change_list_template = 'admin/category/list.html'


class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'image', 'available', 'feature', 'created_at']
    prepopulated_fields = {'slug': ('title',)}


admin.site.site_header = "STDI - Admin Tutorial Dashboard"
admin.site.register(ProductImage)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductReview)