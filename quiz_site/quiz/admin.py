from django.contrib import admin

from .models import Slide


# Register your models here.

@admin.register(Slide)
class SlideAdmin(admin.ModelAdmin):
    list_display = ("number", 'title')
    ordering = ("number",)
