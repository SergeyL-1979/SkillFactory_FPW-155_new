from django.contrib import admin
from .models import Advertisement, Response, Category


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ['ad_author', 'headline', 'ad_category']
    search_fields = ['headline', 'ad_category']
    list_filter = ['headline', 'ad_category']
    # Add other configurations as needed


@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ['ad', 'user_answer', 'accepted_answer', ]
    list_filter = ['accepted_answer', ]
    search_fields = ['text', ]
    # Add other configurations as needed


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', ]


admin.site.register(Category, CategoryAdmin)
