from django.contrib import admin
from public.models import Category,Product,ServiceProvider,Review
# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ServiceProvider)
admin.site.register(Review)