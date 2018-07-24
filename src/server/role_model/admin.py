from django.contrib import admin

from role_model.models import (
    Deliverable,
    Group,
    Format,
    Facet,
    ContentType,
    Assignment,
    Role,
    Responsibility,)


admin.site.register(Deliverable, admin.ModelAdmin)
admin.site.register(Group, admin.ModelAdmin)
admin.site.register(Format, admin.ModelAdmin)
admin.site.register(Facet, admin.ModelAdmin)
admin.site.register(ContentType, admin.ModelAdmin)
admin.site.register(Assignment, admin.ModelAdmin)
admin.site.register(Role, admin.ModelAdmin)
admin.site.register(Responsibility, admin.ModelAdmin)
