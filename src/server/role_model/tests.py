import json

from django.test import TestCase, override_settings
from django.urls import reverse

import schema

from role_model.models import (
    # Assignment,
    ContentType,
    Deliverable,
    Facet,
    Format,
    Group,
    Responsibility,
    Role)
from crm.models import Organization


class RoleModelAPITestCase(TestCase):
    """
    Test the GraphQL API.
    """

    @override_settings(
        GRAPHENE = {
            'SCHEMA': 'role_model.schema.schema'
        })
    def test_1(self):
        self.organization = Organization.objects.create(name="iOSLtd")
        self.deliverable = Deliverable.objects.create(
            name='RaceGame',
            organization=self.organization)

        response = self.client.get(
            reverse('graphql'), {
                'query': """
                    query Query {
                        deliverable {
                          id
                        }
                    }"""})

        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)

        """
        Validate response using Python Schema
        https://pypi.org/project/schema/
        """

        schema.Schema({
            'data': {
                'deliverable': [{
                    'id': str
                }]
            }
        }).validate(data)


class RoleModelTestCase(TestCase):
    """
    Tests using a iOS game company with a single product "RaceGame".
    It's sold on iOS app store for $10, and no in-app purchases.
    """
    def test_1(self):
        self.organization = Organization.objects.create(name="iOSLtd")
        self.deliverable = Deliverable.objects.create(
            name='RaceGame',
            organization=self.organization)
        self.deliverable.formats.add(
            Format(name="Concept",
                   description="Concept of new features"),
            Format(name="Requirements Document",
                   description="Specific product requirements"),
            Format(name="Build Ticket",
                   description="Ticket containing approach of implementation"),
            Format(name="Test Product",
                   description="Implemented software deployed to test server"),
            Format(name="Deployed Product",
                   description="A deployed product"),
            Format(name="Use", description="Use of the product"),
            Format(name="Query", description="A query about the product"),
            Format(name="Response", description="A response to the customer"),
            Format(name="Use Pattern", description="A pattern of queries"),
            Format(name="Bug Report", description="A bug report"),
            Format(name="Feature Request", description="A feature request"),
            bulk=False)

        self.group_user = Group.objects.create(
            name="User",
            organization=self.organization)
        self.group_support = Group.objects.create(
            name="Support",
            organization=self.organization)
        self.group_product = Group.objects.create(
            name="Product",
            organization=self.organization)
        self.group_operations = Group.objects.create(
            name="Operations",
            organization=self.organization)
        self.facet_support_interface = Facet.objects.create(
            name="Support Interface",
            deliverable=self.deliverable)
        self.facet_user_interface = Facet.objects.create(
            name="User Interface",
            deliverable=self.deliverable)

        self.deliverable.content_types.add(
            ContentType(
                group=self.group_user,
                format=self.deliverable.formats.get(name="Use"),
                facet=self.facet_user_interface),
            ContentType(
                group=self.group_user,
                format=self.deliverable.formats.get(name="Query"),
                facet=self.facet_user_interface),
            ContentType(
                group=self.group_user,
                format=self.deliverable.formats.get(name="Use Pattern"),
                facet=self.facet_user_interface),
            ContentType(
                group=self.group_support,
                format=self.deliverable.formats.get(name="Bug Report"),
                facet=self.facet_user_interface),
            ContentType(
                group=self.group_support,
                format=self.deliverable.formats.get(name="Feature Request"),
                facet=self.facet_user_interface),
            ContentType(
                group=self.group_product,
                format=self.deliverable.formats.get(name="Concept"),
                facet=self.facet_user_interface),
            ContentType(
                group=self.group_product,
                format=self.deliverable.formats.get(
                    name="Requirements Document"),
                facet=self.facet_user_interface),
            ContentType(
                group=self.group_product,
                format=self.deliverable.formats.get(name="Build Ticket"),
                facet=self.facet_user_interface),
            ContentType(
                group=self.group_product,
                format=self.deliverable.formats.get(name="Test Product"),
                facet=self.facet_user_interface),
            ContentType(
                group=self.group_product,
                format=self.deliverable.formats.get(name="Deployed Product"),
                facet=self.facet_user_interface),
            ContentType(
                group=self.group_support,
                format=self.deliverable.formats.get(name="Use"),
                facet=self.facet_support_interface),
            ContentType(
                group=self.group_support,
                format=self.deliverable.formats.get(name="Query"),
                facet=self.facet_support_interface),
            ContentType(
                group=self.group_support,
                format=self.deliverable.formats.get(name="Use Pattern"),
                facet=self.facet_support_interface),
            ContentType(
                group=self.group_operations,
                format=self.deliverable.formats.get(name="Bug Report"),
                facet=self.facet_support_interface),
            ContentType(
                group=self.group_operations,
                format=self.deliverable.formats.get(name="Feature Request"),
                facet=self.facet_support_interface),
            ContentType(
                group=self.group_product,
                format=self.deliverable.formats.get(name="Concept"),
                facet=self.facet_support_interface),
            bulk=False)

        def get_content_type(group, format, facet="User Interface"):
            return ContentType.objects.get(
                group__name=group,
                format__name=format,
                facet__name=facet)

        for content_type in self.deliverable.content_types.all():
            print(content_type.prose())

        responsibility = Responsibility.objects.create(
            organization=self.organization,
            operator=Responsibility.Operator.transform,
            output_type=get_content_type("Product", "Build Ticket")
        )
        responsibility.input_types.through.objects.create(
            content_type=get_content_type("Product", "Requirements Document"),
            responsibility=responsibility
        )

        print(responsibility.prose())
        # print(responsibility.prose())

        developer = Role.objects.create(
            name="developer",
            group=self.group_product)

        # developer.responsibilities.add(responsibility)

        responsibility = Responsibility.objects.create(
            organization=self.organization,
            operator=Responsibility.Operator.transform,
            output_type=get_content_type("Product", "Test Product")
        )
        responsibility.input_types.through.objects.create(
            content_type=get_content_type("Product", "Build Ticket"),
            responsibility=responsibility
        )

        # print(responsibility.prose())
        # developer.responsibilities.add(responsibility)
        # print(developer)
        self.deliverable.history().all().count()
