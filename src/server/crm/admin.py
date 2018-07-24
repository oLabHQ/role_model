from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from crm.models import User, Organization


class UserAdmin(BaseUserAdmin):
    """
    Override the default UserAdmin to use with our custom user model.
    They are similar enough we can get away by overriding the following
    attributes.
    """
    list_display = ('username', 'email', 'first_name', 'last_name',
                    'user_type')
    list_filter = ('user_type', 'groups')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('user_type',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'created')}),
    )
    readonly_fields = ["created"]


class OrganizationAdmin(admin.ModelAdmin):
    pass


admin.site.register(User, UserAdmin)
admin.site.register(Organization, OrganizationAdmin)
