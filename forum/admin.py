from django.contrib import admin
from .models import Permission, Category

admin.site.register(Permission)
admin.site.register(Category)