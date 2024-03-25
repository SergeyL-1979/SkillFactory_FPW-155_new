from django.contrib import admin
from .models import Advertisement, Response, Category, PrivatePage


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ['ad_author', 'headline', 'ad_category']
    search_fields = ['headline', 'ad_category']
    # Add other configurations as needed


@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ['ad', ]
    list_filter = ['accepted_answer', ]
    search_fields = ['text', ]
    # Add other configurations as needed


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', ]


class PrivateAdmin(admin.ModelAdmin):
    list_display = ['user', 'response', ]


admin.site.register(PrivatePage, PrivateAdmin)
admin.site.register(Category, CategoryAdmin)
