from django.contrib import admin
from django.utils.html import format_html

from common.language import join_comma
from role_model.models import (
    Deliverable,
    Group,
    Format,
    Facet,
    ContentType,
    Assignment,
    Role,
    Responsibility,)


class OwnershipAdminMixin:
    def organization_link(self, instance):
        from django.urls import reverse
        return format_html("<a href='{0}'>{1}</a>",
            reverse('admin:{}_{}_change'.format(
                instance.organization._meta.app_label.lower(),
                instance.organization._meta.model_name.lower()
            ), args=(instance.organization.id,)),
            str(instance.organization) or instance.organization.id)

    organization_link.allow_tags = True
    organization_link.short_description = "organization"


class GroupAdmin(OwnershipAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'organization_link', 'id',
                    'created')
    list_display_links = ('name', 'id')
    search_fields = ['organization__name']


class ResponsibilityAdmin(OwnershipAdminMixin, admin.ModelAdmin):
    list_display = ('operator', 'prose', 'organization_link', 'id',
                    'created')
    list_display_links = ('operator', 'id')
    search_fields = ['organization__name']


class RoleAdmin(OwnershipAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'responsibilities_table', 'organization_link',
                    'id', 'created')
    list_display_links = ('name', 'id')
    search_fields = [
        'group__organization__name',
        'responsibilities__input_types__deliverable__name',
        'responsibilities__input_types__group__name',
        'responsibilities__input_types__facet__name',
        'responsibilities__input_types__format__name']

    def responsibilities_table(self, instance):
        responsibilities = instance.responsibilities.all()
        html_args = []
        html = ['<table>']
        for responsibility in responsibilities:
            html.append('<tr>')
            html.append('<td>')
            html.append('{}')
            html_args.append(str(responsibility.operator))
            html.append('</td>')
            html.append('<td>')
            for input_type in responsibility.input_types.all():
                html.append("{}")
                html_args.append(str(input_type))
                html.append("<br>")
            html.append("→<br>")
            html.append('{}')
            html_args.append(str(responsibility.output_type))
            html.append('</td>')
            html.append('</tr>')
        html.append('</table>')

        return format_html("\n".join(html), *html_args)

    responsibilities_table.allow_tags = True
    responsibilities_table.short_description = "responsibilities"


admin.site.register(Deliverable, admin.ModelAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Format, admin.ModelAdmin)
admin.site.register(Facet, admin.ModelAdmin)
admin.site.register(ContentType, admin.ModelAdmin)
# admin.site.register(Assignment, admin.ModelAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(Responsibility, ResponsibilityAdmin)
