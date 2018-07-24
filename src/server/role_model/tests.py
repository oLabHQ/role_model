import json

from django.test import TestCase
from django.urls import reverse

import schema

from role_model.models import *
from crm.models import *


class RoleModelAPITestCase(TestCase):
    """
    Test the GraphQL API.
    """
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
                format=self.deliverable.formats.get(name="Requirements Document"),
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
            operator = Responsibility.Operator.transform,
            output_type = get_content_type("Product", "Build Ticket")
        )
        responsibility.input_types.set([
            get_content_type("Product", "Requirements Document")])

        print(responsibility.prose())
        # print(responsibility.prose())

        developer = Role.objects.create(
            name="developer",
            group=self.group_product)

        developer.responsibilities.add(responsibility)

        responsibility = Responsibility.objects.create(
            organization=self.organization,
            operator = Responsibility.Operator.transform,
            output_type = get_content_type("Product", "Test Product")
        )
        responsibility.input_types.set([
            get_content_type("Product", "Build Ticket")])

        print(responsibility.prose())
        developer.responsibilities.add(responsibility)
        print(developer)


        # self.division_product = Division.objects.create('Product')
        # self.format_concept = Format.objects.create(
        #     name="Concept",
        #     division=self.division_product)
        # self.format_requirements = Format.objects.create(
        #     name="Requirements",
        #     division=self.division_product)
        # self.format_ticket = Format.objects.create(
        #     name="Ticket",
        #     division=self.division_product)
        # self.format_test = Format.objects.create(
        #     name="Test Implementation",
        #     division=self.division_product)
        # self.format_test_bug_report = Format.objects.create(
        #     name="Test Bug Report",
        #     division=self.division_product)
        # self.format_implementation = Format.objects.create(
        #     name="Implementation",
        #     division=self.division_product)
        #
        # self.division_customer = Division.objects.create('Customer Support')
        # self.format_use = Format.objects.create(
        #     name="Use",
        #     division=self.division_customer)
        # self.format_query = Format.objects.create(
        #     name="Query",
        #     division=self.division_customer)
        # self.format_pattern = Format.objects.create(
        #     name="Pattern",
        #     division=self.division_customer)
        # self.format_bug_report = Format.objects.create(
        #     name="Bug Report",
        #     division=self.division_customer)
        # self.format_feature_request = Format.objects.create(
        #     name="Feature Request",
        #     division=self.division_customer)
        #
        # self.division_operations = Division.objects.create('Operations')
        #
        #
        # self.deliverable = Chart.objects.create(name='RaceGame')
        # self.facet_admin = Facet.objects.create(
        #     name="Admin Interface",
        #     deliverable=chart)
        # self.facet_user_interface = Facet.objects.create(
        #     name="User Interface",
        #     deliverable=chart)
        #




        # process = [
        #     "Customer Use",
        #     "Customer Query",
        #     "Customer Usage Pattern",
        #     "Concept",
        #     "Requirement",
        #     "Ticket",
        #     "Implementation"
        # ]
        # aspects = [
        #     "User Interface",
        #     "Admin Interface",
        #     "Analytics Interface"
        # ]


        # self.process = [
        #     ([("Marketing",), ("Customer",)], ("Product", "Concepts", "Product"))
        # ]
        #
        # self.information_types = []
        #
        # information_product = self.add_information_type(name="Product")
        # information_customer = self.add_information_type(name="Customer")
        # information_marketing = self.add_information_type(name="Marketing")
        #
        # self.add_information_type(name="Concepts", parent=information_product)
        # self.add_information_type(name="Concepts", parent=information_product)

    # def add_information_type(self, *args, **kwargs):
        # instance = InformationType(*args, **kwargs)
        # instance.clean()
        # instance.save()
        # self.information_types.append(instance)
        # return instance
