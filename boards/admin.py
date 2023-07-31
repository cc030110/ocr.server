from django.contrib import admin
from . import models

@admin.register(models.Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = [
        'no',
        'title',
        'author',
        'create_at',
        'update_at',     
    ]

    list_filter = [
        'author',
    ]

    search_fields = [
        'title',
        'author'
    ]

    sortable_by = [
        'no',
    ]