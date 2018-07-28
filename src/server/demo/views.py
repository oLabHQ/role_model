import json

from django.conf import settings
from django.shortcuts import render

from role_model.models import Deliverable


def serialize_history(history):
    if not history.delta:
        data = {
            'event': 'created',
            'timestamp': history.created.isoformat(),
            'instance': history.serialized_data
        }
    else:
        data = {
            'event': 'modified',
            'timestamp': history.created.isoformat(),
            'fields': dict(history.changes())
        }
    return data


def index(request):
    from history.apps import register_models
    register_models()
    deliverable = Deliverable.objects.get(name=settings.DEMO_DELIVERABLE_NAME)
    entries = []
    for entry in deliverable.history().all():
        entries.append(serialize_history(entry))

    return render(request, "demo/index.html", context={
        'entries': json.dumps(entries),
        'entries_count': len(entries)
    })
