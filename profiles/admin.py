from django.contrib import admin

from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """
    Register UserProfile model with admin
    """
    list_filter = ('country', )
    list_display = ('user', 'first_name', 'last_name', 'town_or_city',
                    'country', 'postcode',)
    search_fields = ('last_name', 'town_or_city', 'country', 'postcode')
