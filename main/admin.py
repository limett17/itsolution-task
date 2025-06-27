from django.contrib import admin
from .models import ViewCount
# Register your models here.

@admin.register(ViewCount)
class ViewCountAdmin(admin.ModelAdmin):
    pass