from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        "display_name",
        "email",
        # "rating",
        "user_type",
        "is_active",
        "is_superuser",
    )
    list_filter = ("user_type",)
    search_fields = ["first_name", "last_name", "email"]


admin.site.register(User, UserAdmin)
