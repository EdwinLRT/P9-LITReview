from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'ticket', 'created_on', 'active')
    list_filter = ('active', 'created_on')
    search_fields = ('user', 'body', 'name')
    actions = ['hide_reviews']

    def approve_comments(self, request, queryset):
        queryset.update(active=False)
