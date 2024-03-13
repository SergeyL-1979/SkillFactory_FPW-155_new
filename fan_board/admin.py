from django.contrib import admin
from .models import Advertisement, Response


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'category')
    search_fields = ('title', 'category')
    # Add other configurations as needed


@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ('user', 'advertisement', 'accepted')
    list_filter = ('accepted',)
    search_fields = ('text',)
    # Add other configurations as needed

