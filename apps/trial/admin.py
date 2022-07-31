from django.contrib import admin
from .models import Post, Product, ProductCategory

# Register your models here.
admin.site.register(Post)
admin.site.register(ProductCategory)
# admin.site.register(Product)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'category', 'name', 'price', 'photo']
    list_filter = ['category']
