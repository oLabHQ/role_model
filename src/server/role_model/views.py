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

    for group in Group.objects.filter(
            roles__responsibilities__input_types__deliverable=deliverable):
        nodes.append({
            'data': {
                'id': str(group.id),
                'name': group.name
            }
        })

    for role in Role.objects.filter(
            responsibilities__input_types__deliverable=deliverable):
        nodes.append({
            'data': {
                'id': str(role.id),
                'name': role.name,
                'parent': str(role.group.id)
            }
        })

        from sqlalchemy.orm import aliased
        RoleAssignment = aliased(Assignment.sa)
        RoleResponsibility = aliased(Responsibility.sa)
        RoleInputType = aliased(ResponsibilityInputType.sa)
        OtherResponsibility = aliased(Responsibility.sa)
        OtherAssignment = aliased(Assignment.sa)
        OtherInputType = aliased(ResponsibilityInputType.sa)
        InputType = aliased(ContentType.sa)
        OutputType = aliased(ContentType.sa)

        sources = (RoleAssignment
            .query(RoleAssignment.id,
                   OtherAssignment.role_id)
            .join(RoleResponsibility,
                  RoleResponsibility.id ==
                  RoleAssignment.responsibility_id)
            .join(RoleInputType,
                  RoleInputType.responsibility_id ==
                  RoleResponsibility.id)
            .join(InputType,
                  RoleInputType.content_type_id ==
                  InputType.id)
            .join(OtherResponsibility,
                  OtherResponsibility.output_type_id ==
                  InputType.id)
            .join(OtherAssignment,
                  OtherAssignment.responsibility_id ==
                  OtherResponsibility.id)
            .filter(
                RoleAssignment.role_id == role.id,
                OtherAssignment.role_id != role.id
            )
        ).all()

        for assignment_id, source_id in sources:
            edges.append({
                'data': {
                    'id': "-".join([str(assignment_id), "from"]),
                    'source': str(source_id),
                    'target': str(role.id),
                }
            })

        targets = (RoleAssignment
            .query(RoleAssignment.id,
                   OtherAssignment.role_id)
            .join(RoleResponsibility,
                  RoleResponsibility.id ==
                  RoleAssignment.responsibility_id)
            .join(OutputType,
                  RoleResponsibility.output_type_id ==
                  OutputType.id)
            .join(OtherInputType,
                  OtherInputType.content_type_id ==
                  OutputType.id)
            .join(OtherResponsibility,
                  OtherInputType.responsibility_id ==
                  OtherResponsibility.id)
            .join(OtherAssignment,
                  OtherAssignment.responsibility_id ==
                  OtherResponsibility.id)
            .filter(
                RoleAssignment.role_id == role.id,
                OtherAssignment.role_id != role.id
            )
        ).all()

        for assignment_id, target_id in targets:
            edges.append({
                'data': {
                    'id': "-".join([str(assignment_id), "to"]),
                    'source': str(role.id),
                    'target': str(target_id),
                }
            })

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
