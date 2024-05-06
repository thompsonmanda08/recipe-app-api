"""" Django Admin Customizations"""

from core import models
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _


class UserAdmin(BaseUserAdmin):
    """Define the admin pages for user accounts"""

    ordering = ["id"]
    list_display = (
        "email",
        "name",
    )

    fieldsets = (
        (
            _("User Information"),  # User information Heading on admin page
            {
                "fields": ("email", "password"),
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    # "name",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    # "groups",
                    # "user_permissions",
                ),
            },
        ),
        (
            _("Important date"),
            {
                "fields": ("last_login",),
            },
        ),
    )

    readonly_fields = ["last_login"]

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "name",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )


admin.site.register(models.User, UserAdmin)
