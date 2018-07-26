import json

from django.shortcuts import render, get_object_or_404

from role_model.models import (
    Assignment,
    ContentType,
    Deliverable,
    Role,
    Group,
    Responsibility,
    ResponsibilityInputType)


def chart_node(id, **kwargs):
    return {
        'data': {
            k: str(v)
                for k, v in dict(id=id, **kwargs).items() if v
        }
    }


def deliverable_organization_chart(request, deliverable_id,
                                   template='role_model/charts.html'):
    """
    TODO:
    0. Consider using aldjemy to write more efficient query.
    1. Get the chart to look how we want it to look
    2. Figure out a pattern to these .filter calls and move them to the
    model managers.
    3. Create an intermediary data structure so we can write model methods
    that return these nodes and edges information.
    """
    deliverable = get_object_or_404(Deliverable, pk=deliverable_id)
    nodes = []
    edges = []
    content_types = {}
    colors = [
        "#6FB1FC",
        "#EDA1ED",
        "#86B342",
        "#F5A45D",
        "#6456B7",
        "#FF007C"
    ]
    connections = {}

    group_colors = {}
    role_colors = {}

    for group in deliverable.organization.groups.all():
        color = colors[len(group_colors) % len(colors)]
        group_colors[str(group.id)] = color

        for role in group.roles.all():
            role_colors[str(role.id)] = color

    for content_type in deliverable.content_types.all():
        content_types[str(content_type.id)] = content_type


    for group in Group.objects.filter(
            roles__responsibilities__input_types__deliverable=deliverable) \
            .distinct():
        nodes.append({
            'data': {
                'id': str(group.id),
                'name': group.name,
                'width': '100',
                'color': group_colors[str(group.id)]
            }
        })

    for role in Role.objects.filter(
            responsibilities__input_types__deliverable=deliverable).distinct():
        color = role_colors[str(role.id)]
        nodes.append(chart_node(
            id=role.id,
            name=role.name,
            width=len(role.name) * 16,
            color=color,
            parent=role.group.id
        ))
        sources = role.sources().all()
        targets = role.targets().all()

        inserted = {}

        for assignment_id, other_assignment_id, source_id, content_type_id \
                in sources:
            content_type = content_types[str(content_type_id)]

            if other_assignment_id:
                edges.append({
                    'data': {
                        'id': "-".join([str(source_id), str(role.id),
                                        str(content_type_id),]),
                        'name': content_type.short_name,
                        'source': str(source_id),
                        'target': str(role.id),
                        'source_color': None,
                        'target_color': color,
                        'classes': 'autorotate',
                        'line_color': '#666'
                    }
                })
            else:
                pass

        for assignment_id, other_assignment_id, target_id, content_type_id \
                in targets:
            if not other_assignment_id:
                content_type = content_types[str(content_type_id)]
                print(content_type.short_name)
                edges.append({
                    'data': {
                        'id': "-".join([str(role), str(role.id),
                                        str(content_type_id),]),
                        'name': content_type.short_name,
                        'source': str(role.id),
                        'target': str(role.id),
                        'source_color': None,
                        'target_color': color,
                        'classes': 'autorotate',
                        'line_color': 'red'
                    }
                })

    for edge in edges:
        edge['data']['source_color'] = role_colors[edge['data']['source']]

    return render(request, template, context={
        'deliverable': deliverable,
        'nodes': json.dumps(nodes),
        'edges': json.dumps(edges)
    })
