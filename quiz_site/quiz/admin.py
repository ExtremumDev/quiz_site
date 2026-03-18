from django.contrib import admin

from .models import Slide, Question


# Register your models here.

@admin.register(Slide)
class SlideAdmin(admin.ModelAdmin):
    list_display = ("number", 'title')
    ordering = ("number",)


@admin.register(Question)
class SlideAdmin(admin.ModelAdmin):
    list_display = ("content", 'pk')
    ordering = ("pk",)
