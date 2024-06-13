from django.contrib import admin
from .models import ColsTypes
from .models import FileContent


@admin.register(ColsTypes)
class ColsTypesAdmin(admin.ModelAdmin):
    list_display = ('name', 'birthdate', 'score', 'grade')


@admin.register(FileContent)
class FileContentAdmin(admin.ModelAdmin):
    list_display = ('name', 'birthdate', 'score', 'grade')