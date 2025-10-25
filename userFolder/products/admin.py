from django.contrib import admin
from .models import Category,Product,ProductImage
# Register your models here.
admin.site.register(Category)
class ProductImageInline(admin.TabularInline): # or admin.StackedInline
    model = ProductImage
    extra = 1 
class ProductAdminView(admin.ModelAdmin):
    list_display=['name','description','price','category','stock','created_at','is_featured','is_most_demanded','is_selective']
admin.site.register(Product,ProductAdminView,inlines=[ProductImageInline])

class ProductImageAdminView(admin.ModelAdmin):
    list_display = ['product','image']
admin.site.register(ProductImage,ProductImageAdminView)
