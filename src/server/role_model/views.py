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

        inserted = {}

        for assignment_id, other_assignment_id, source_id, content_type_id \
                in sources:
            content_type = ContentType.objects.id(id=str(content_type_id))

            edges.append({
                'data': {
                    'id': str(role.id) + str(source_id) + str(content_type_id),
                    'name': content_type.short_name,
                    'source': str(source_id),
                    'target': str(role.id),
                    'source_color': None,
                    'target_color': color,
                    'classes': 'autorotate'
                }
            })

        for edge in edges:
            edge['data']['source_color'] = role_colors[edge['data']['source']]

            # nodes.append({
            #     'data': {
            #         'id': str(role.id),
            #         'name': role.name,
            #         'width': str(len(role.name) * 10),
            #         'color': color,
            #         'parent': str(role.group.id)
            #     }
            # })
            #
            # connection = connections.setdefault(
            #     (str(source_id), str(role.id)), {
            #         'id': "-".join([str(assignment_id), "from"]),
            #         'content_types': set()
            #     })
            #
            # connection['content_types'].add(
            #     str(ContentType.objects.id(id=content_type_id)))

        targets = role.targets().all()

        # for assignment_id, other_assignment_id, target_id, content_type_id \
        #         in targets:
        #     content_type = ContentType.objects.id(id=str(content_type_id))
        #     pass
            # edges.append({
            #     'data': {
            #         'id': str(assignment_id) + "-edge",
            #         'name': "Hello",
            #         'source': str(role.id),
            #         'target': str(assignment_id),
            #         'source_color': color,
            #         'target_color': color,
            #     }
            # })
            # connection = connections.setdefault(
            #     (str(role.id), str(target_id)), {
            #         'id': "-".join([str(assignment_id), "to"]),
            #         'content_types': set()
            #     })
            #
            # connection['content_types'].add(
            #     str(ContentType.objects.id(id=content_type_id)))

    # for key, value in connections.items():
    #     source, target = key
    #     edges.append({
    #         'data': {
    #             'id': value['id'],
    #             'name': "<br>".join(list(value['content_types'])),
    #             'source': source,
    #             'target': target,
    #             'source_color': role_colors[source],
    #             'target_color': role_colors[target],
    #         }
    #     })


        # For comparison, Django only implementation.
        # for responsibility in role.responsibilities.all():
        #     for target in Role.objects.filter(
        #             responsibilities__input_types=responsibility.output_type):
        #         edges.append({
        #             'data': {
        #                 'id': ",".join([
        #                     str(responsibility.id),
        #                     str(responsibility.output_type.id)
        #                 ]),
        #                 'source': str(role.id),
        #                 'target': str(target.id),
        #             }
        #         })
        #     for input_type in responsibility.input_types.all():
        #         for source in Role.objects.filter(
        #                 responsibilities__output_type=input_type):
        #             edges.append({
        #                 'data': {
        #                     'id': ",".join(
        #                         [str(responsibility.id), str(input_type.id)]),
        #                     'source': str(source.id),
        #                     'target': str(role.id)
        #                 }
        #             })
    return render(request, template, context={
        'deliverable': deliverable,
        'nodes': json.dumps(nodes),
        'edges': json.dumps(edges)
    })
