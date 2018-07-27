import json

from django.db.models import Q
from django.shortcuts import render, get_object_or_404

from role_model.models import (
    Assignment,
    ContentType,
    Deliverable,
    Role,
    Group,
    Responsibility,
    ResponsibilityInputType)


"""
This module requires a good refactoring.
"""


def chart_node(id, **kwargs):
    return {
        'data': {
            k: str(v)
                for k, v in dict(id=id, **kwargs).items() if v
        }
    }

colors = [
    "#6FB1FC",
    "#EDA1ED",
    "#86B342",
    "#F5A45D",
    "#6456B7",
    "#FF007C"
]

def role_chart(request, role_id, template='role_model/charts.html'):
    role = get_object_or_404(Role, pk=role_id)
    nodes = []
    edges = []

    content_types = {}
    connections = {}
    roles = {}
    group_colors = {}
    role_colors = {}

    added_nodes = set([role.id])

    for _role in Role.objects.filter(
            group__organization__groups__roles=role).all():
        if not str(_role.group_id) in group_colors:
            color = colors[len(group_colors) % len(colors)]
            group_colors[str(_role.group_id)] = color
        roles[str(_role.id)] = _role
        role_colors[str(_role.id)] = group_colors[str(_role.group_id)]

    for content_type in ContentType.objects.filter(
            deliverable__organization__groups__roles=role).all():
        content_types[str(content_type.id)] = content_type

    _, sources = role.sources()
    sources = sources.all()

    _, targets = role.targets()
    targets = targets.all()

    nodes.append(chart_node(
        id=role.id,
        name=role.name,
        width=len(role.name) * 16,
        color=role_colors[str(role.id)]
    ))

    def add_sources(role, sources):
        for assignment_id, other_assignment_id, source_id, content_type_id \
                in sources:
            if source_id not in added_nodes:
                source = roles[str(source_id)]
                color = role_colors[str(source.id)]
                nodes.append(chart_node(
                    id=source.id,
                    name=source.name,
                    width=len(source.name) * 16,
                    color=color
                ))
                added_nodes.add(source_id)

            content_type = content_types[str(content_type_id)]
            if other_assignment_id:
                color = role_colors[str(source_id)]
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

    def add_targets(role, targets):
        for assignment_id, other_assignment_id, target_id, content_type_id \
                in targets:
            if target_id and target_id not in added_nodes:
                color = role_colors[str(target_id)]
                target = Role.objects.get(id=target_id)
                nodes.append(chart_node(
                    id=target.id,
                    name=target.name,
                    width=len(target.name) * 16,
                    color=color
                ))
                added_nodes.add(target_id)

            content_type = content_types[str(content_type_id)]

            if other_assignment_id:
                color = role_colors[str(target_id)]
                content_type = content_types[str(content_type_id)]
                edges.append({
                    'data': {
                        'id': "-".join([str(role.id), str(target_id),
                                        str(content_type_id),]),
                        'name': content_type.short_name,
                        'source': str(role.id),
                        'target': str(target_id),
                        'source_color': None,
                        'target_color': color,
                        'classes': 'autorotate',
                        'line_color': '#666'
                    }
                })
            else:
                edges.append({
                    'data': {
                        'id': "-".join([str(role), str(role.id),
                                        str(content_type_id),]),
                        'name': content_type.short_name,
                        'source': str(role.id),
                        'target': str(role.id),
                        'source_color': 'red',
                        'target_color': color,
                        'classes': 'autorotate',
                        'line_color': 'red'
                    }
                })

    add_sources(role, sources)
    add_targets(role, targets)

    for role_id in added_nodes:
        if role_id != role.id:
            _role = roles[str(role_id)]
            Alias, sources = _role.sources()
            sources = sources.filter(
                Alias.OtherAssignment.role_id.in_(added_nodes),
                Alias.OtherAssignment.role_id != role.id).all()
            add_sources(_role, sources)

    for edge in edges:
        if not edge['data']['source_color']:
            edge['data']['source_color'] = role_colors[edge['data']['source']]

    return render(request, template, context={
        'name': role.name,
        'layout': 'cose',
        'nodes': json.dumps(nodes),
        'edges': json.dumps(edges),
        'edge': {
            'curve_style': 'bezier',
            'content': 'data(name)',
            'text_outline_width': 3,
            'font_size': 16
        }
    })


def deliverable_content_type_chart(request, deliverable_id,
                                   template='role_model/charts.html'):

    deliverable = get_object_or_404(Deliverable, pk=deliverable_id)
    nodes = []
    edges = []
    roles = {}
    content_types = {}
    content_type_colors = {}
    connections = {}

    group_colors = {}
    role_colors = {}

    for group in deliverable.organization.groups.all():
        color = colors[len(group_colors) % len(colors)]
        group_colors[str(group.id)] = color

        for role in group.roles.all():
            role_colors[str(role.id)] = color
            roles[str(role.id)] = role

        for content_type in group.content_types.all():
            content_type_colors[str(content_type.id)] = color

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


    for content_type in ContentType.objects.filter(deliverable=deliverable):
        color = content_type_colors[str(content_type.id)]
        name = content_type.short_name
        nodes.append(chart_node(
            id=content_type.id,
            name=name,
            width=len(name) * 16,
            color=color,
            parent=content_type.group.id
        ))

        _, sources = content_type.sources()
        sources = sources.all()

        for assignment_id, role_id, source_id in sources:
            content_type = content_types[str(content_type.id)]
            color = content_type_colors[str(source_id)]
            role = roles[str(role_id)]
            edges.append({
                'data': {
                    'id': "-".join([str(source_id), str(role.id),
                                    str(content_type.id),]),
                    'name': role.name,
                    'source': str(source_id),
                    'target': str(content_type.id),
                    'source_color': None,
                    'target_color': color,
                    'classes': 'autorotate',
                    'line_color': '#666'
                }
            })

    for edge in edges:
        if not edge['data']['source_color']:
            edge['data']['source_color'] = \
                content_type_colors[edge['data']['source']]

    return render(request, template, context={
        'name': deliverable.name,
        'layout': 'grid',
        'nodes': json.dumps(nodes),
        'edges': json.dumps(edges),
        'edge': {
            'curve_style': 'bezier',
            'content': 'data(name)',
            'text_outline_width': 4,
            'font_size': 32
        }
    })


def deliverable_chart(request, deliverable_id,
                               template='role_model/charts.html',
                               collapsed=False):
    """
    TODO:
    2. Figure out a pattern to these .filter calls and move them to the
    model managers.
    3. Create an intermediary data structure so we can write model methods
    that return these nodes and edges information.
    """
    deliverable = get_object_or_404(Deliverable, pk=deliverable_id)
    nodes = []
    edges = []
    content_types = {}
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
        _, sources = role.sources()
        sources = sources.all()
        _, targets = role.targets()
        targets = targets.all()

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
                edges.append({
                    'data': {
                        'id': "-".join([str(role), str(role.id),
                                        str(content_type_id),]),
                        'name': content_type.short_name,
                        'source': str(role.id),
                        'target': str(role.id),
                        'source_color': 'red',
                        'target_color': color,
                        'classes': 'autorotate',
                        'line_color': 'red'
                    }
                })

    for edge in edges:
        if not edge['data']['source_color']:
            edge['data']['source_color'] = role_colors[edge['data']['source']]

    if collapsed:
        edge_configuration = {
            'curve_style': 'unbundled-bezier',
            'content': '',
            'text_outline_width': 4,
            'font_size': 32
        }
    else:
        edge_configuration = {
            'curve_style': 'bezier',
            'content': 'data(name)',
            'text_outline_width': 4,
            'font_size': 32
        }


    return render(request, template, context={
        'name': deliverable.name,
        'layout': 'circle',
        'nodes': json.dumps(nodes),
        'edges': json.dumps(edges),
        'edge': edge_configuration
    })
