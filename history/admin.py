from django.contrib import admin
from django.utils.html import format_html

from history.models import History, MigrationState


class MigrationStateAdmin(admin.ModelAdmin):
    list_display = ('id', 'app_migrations_table')

    def app_migrations_table(self, instance):
        app_migrations = instance.app_migrations
        html_args = []
        html = ['<table>']
        for app_label, migration_names in sorted(app_migrations.items()):
            html.append('<tr>')
            html.append('<th>')
            html.append('{}')
            html_args.append(app_label)
            html.append('</th>')
            html.append('<td>')
            html.append('{}')
            html_args.append(", ".join(migration_names))
            html.append('</td>')
            html.append('</tr>')
        html.append('</table>')

        return format_html("\n".join(html), *html_args)

    app_migrations_table.allow_tags = True
    app_migrations_table.short_description = "app migrations"


class HistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'content_type', 'object_id_link',
                    'object_description', 'modification', 'changes_table',
                    'created')

    def object_description(self, instance):
        return str(instance.instance)

    def object_id_link(self, instance):
        from django.urls import reverse
        return format_html(
            "<a href='{0}'>{1}</a>",
            reverse('admin:{}_{}_change'.format(
                instance.content_type.app_label.lower(),
                instance.content_type.model.lower()
            ), args=(instance.object_id,)),
            instance.object_id)

    object_id_link.allow_tags = True
    object_id_link.short_description = "object id"

    def changes_table(self, instance):
        changes = instance.changes()
        html_args = []
        html = ['<table>']
        for change in changes:
            field, values = change
            html.append('<tr>')
            html.append('<th>')
            html.append('{}')
            html_args.append(field)
            html.append('</th>')
            html.append('<td>')
            html.append('{}')
            html_args.append(" → ".join(reversed(list(map(str, values)))))
            html.append('</td>')
            html.append('</tr>')
        html.append('</table>')

        return format_html("\n".join(html), *html_args)

    changes_table.allow_tags = True
    changes_table.short_description = "changes"


admin.site.register(History, HistoryAdmin)
admin.site.register(MigrationState, MigrationStateAdmin)
