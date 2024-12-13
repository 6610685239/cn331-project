from django.contrib import admin
from .models import AlertPost


@admin.register(AlertPost)
class AlertPostAdmin(admin.ModelAdmin):
    list_display = ("title", "post_type", "created_at")
    list_filter = ("post_type", "created_at")
    search_fields = ("title", "content")
