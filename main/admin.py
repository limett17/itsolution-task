from django.contrib import admin
from .models import ViewCount, Quote
# Register your models here.

@admin.register(ViewCount)
class ViewCountAdmin(admin.ModelAdmin):
    pass

@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ('quote', 'source', 'prob_rate')
    list_editable = ('prob_rate',)