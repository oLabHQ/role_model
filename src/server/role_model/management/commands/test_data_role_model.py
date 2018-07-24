from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from role_model.models import (
    Assignment,
    ContentType,
    Deliverable,
    Facet,
    Format,
    Group,
    Responsibility,
    Role)
from crm.models import Organization

class Command(BaseCommand):
    help = 'Set up test data for role_model app.'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        print("Setting up test data.")
        with transaction.atomic():
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

            # Assignment.objects.create(
            #     role=developer,
            #     responsibility=responsibility,
            #     status = Assignment.Status.formal)
            developer.responsibilities.add(responsibility)

            responsibility = Responsibility.objects.create(
                organization=self.organization,
                operator = Responsibility.Operator.transform,
                output_type = get_content_type("Product", "Test Product")
            )
            responsibility.input_types.set([
                get_content_type("Product", "Build Ticket")])

            # Assignment.objects.create(
            #     role=developer,
            #     responsibility=responsibility,
            #     status = Assignment.Status.formal)
            developer.responsibilities.add(responsibility)
            print(developer)
