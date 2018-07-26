from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import SafeText


from common import admin_change_link

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
        return admin_change_link(instance.organization)

    organization_link.allow_tags = True
    organization_link.short_description = "organization"


class HasDeliverableAdminMixin:
    def deliverable_link(self, instance):
        return admin_change_link(instance.deliverable)

    deliverable_link.allow_tags = True
    deliverable_link.short_description = "deliverable"


class GroupAdmin(OwnershipAdminMixin, admin.ModelAdmin):
    search_fields = ['organization__name']
    list_display_links = ('name', 'id')
    list_display = ('name', 'organization_link', 'id',
                    'created')


class ResponsibilityAdmin(OwnershipAdminMixin, admin.ModelAdmin):
    list_display = ('operator', 'input_types_table', 'output_type_link',
                    'prose', 'organization_link', 'id', 'created')
    list_display_links = ('operator', 'id')
    search_fields = ['organization__name']

    def output_type_link(self, instance):
        return admin_change_link(instance.output_type)

    output_type_link.allow_tags = True
    output_type_link.short_description = "output type"

    def input_types_table(self, instance):
        input_types = list(instance.input_types.all())
        html_args = []
        html = []
        if len(input_types) > 1:
            html.append('<table>')
            for input_type in input_types:
                html.append('<tr>')
                html.append('<td>')
                html.append(admin_change_link(input_type))
                html.append('</td>')
                html.append('</tr>')
            html.append('</table>')
        elif input_types:
            return admin_change_link(input_types[0])

        return format_html("\n".join(html), *html_args)

    input_types_table.allow_tags = True
    input_types_table.short_description = "input types"


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

    fieldsets = (
        (None, {'fields': ('name', 'users', 'group', 'created',
                           'chart_link',
                           'chart',)}),
    )
    readonly_fields = ['created',
                       'chart',
                       'chart_link',]

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


    def chart_link(self, instance):
        return format_html('<a href="{}">Chart</a>',
            reverse('role_chart',
                    kwargs={
                        'role_id': str(instance.id)
                    }))

    def chart(self, instance):
        return SafeText(
            format_html("""
<iframe src="{}" width="800px" height="600px"></iframe>""",
                reverse('role_chart',
                        kwargs={
                            'role_id': str(instance.id)
                        })))


class FormatAdmin(
        HasDeliverableAdminMixin,
        OwnershipAdminMixin,
        admin.ModelAdmin):

    list_display = ('name', 'deliverable_link', 'organization_link', 'id',
                    'created')
    list_display_links = ('name', 'id')

    def deliverable_link(self, instance):
        return admin_change_link(instance.deliverable)

    deliverable_link.allow_tags = True
    deliverable_link.short_description = "deliverable"


FacetAdmin = FormatAdmin


class DeliverableAdmin(OwnershipAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'organization_link', 'id',
                    'created')
    list_display_links = ('name', 'id')
    fieldsets = (
        (None, {'fields': ('name', 'organization',
                           'chart_link',
                           'chart_collapsed_link',
                           'chart_collapsed',
                           'chart',)}),
    )
    readonly_fields = ['created',
                       'chart',
                       'chart_collapsed',
                       'chart_link',
                       'chart_collapsed_link']

    def chart_link(self, instance):
        return format_html('<a href="{}">Chart</a>',
            reverse('deliverable_chart',
                    kwargs={
                        'deliverable_id': str(instance.id)
                    }))
    def chart_collapsed_link(self, instance):
        return format_html('<a href="{}">Chart (collapsed)</a>',
            reverse('deliverable_chart_collapsed',
                    kwargs={
                        'deliverable_id': str(instance.id)
                    }))
    def chart_collapsed(self, instance):
        return SafeText(
            format_html("""
<iframe src="{}" width="800px" height="600px"></iframe>""",
                reverse('deliverable_chart_collapsed',
                        kwargs={
                            'deliverable_id': str(instance.id)
                        })))
    def chart(self, instance):
        return SafeText(
            format_html("""
<iframe src="{}" width="800px" height="600px"></iframe>""",
                reverse('deliverable_chart',
                        kwargs={
                            'deliverable_id': str(instance.id)
                        })))

class ContentTypeAdmin(
        HasDeliverableAdminMixin,
        OwnershipAdminMixin,
        admin.ModelAdmin):

    list_display = ('prose', 'deliverable_link', 'group_link', 'facet_link',
                    'format_link', 'organization_link', 'id', 'created')
    list_display_links = ('prose', 'id')

    def group_link(self, instance):
        return admin_change_link(instance.group)

    group_link.allow_tags = True
    group_link.short_description = "group"

    def facet_link(self, instance):
        return admin_change_link(instance.facet)

    facet_link.allow_tags = True
    facet_link.short_description = "facet"

    def format_link(self, instance):
        return admin_change_link(instance.format)

    format_link.allow_tags = True
    format_link.short_description = "format"


class AssignmentAdmin(OwnershipAdminMixin, admin.ModelAdmin):
    list_display = ('id', 'role_link', 'responsibility_link',
                    'organization_link', 'status',  'created')
    list_display_links = ('id',)

    def role_link(self, instance):
        return admin_change_link(instance.role, label=lambda role: role.name)

    role_link.allow_tags = True
    role_link.short_description = "role"
    role_link.admin_order_field = 'role__name'

    def responsibility_link(self, instance):
        return admin_change_link(instance.responsibility)

    responsibility_link.allow_tags = True
    responsibility_link.short_description = "responsibility"
    responsibility_link.admin_order_field = 'responsibility_id'



admin.site.register(Deliverable, DeliverableAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Format, FormatAdmin)
admin.site.register(Facet, FacetAdmin)
admin.site.register(ContentType, ContentTypeAdmin)
admin.site.register(Assignment, AssignmentAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(Responsibility, ResponsibilityAdmin)
