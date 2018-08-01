from django.core.management.base import BaseCommand
from django.db import transaction

from role_model.models import (
    Assignment,
    ContentType,
    Deliverable,
    Facet,
    Format,
    Group,
    Operator,
    Responsibility,
    Role)
from crm.models import Organization


class Command(BaseCommand):
    """
    Set up local development data for role_model app. Expects a blank database.

    Since this is more like scaffolding, be wary of being too eager to
    implement methods to refactor this code; There might be more optimal
    function calling patterns discovered in the future when implementing
    the business logic, more suitable to our use cases.
    """
    help = 'Set up test data for role_model app.'

    FORMATS = [
        ('Concept', 'Concept of new features'),
        ('Proposal', 'Proposal of new features'),
        ('Requirements Document', 'Specific product requirements'),
        ('Build Ticket', 'Ticket containing approach of implementation'),
        ('Test Product', 'Implemented software deployed to test server'),
        ('Test', 'A test of the test product'),
        ('Deployed Product', 'A deployed product'),
        ('Use', 'Use of the product'),
        ('Query', 'A query about the product'),
        ('Response', 'A response to the customer'),
        ('Use Pattern', 'A pattern of queries'),
        ('Bug Report', 'A bug report'),
        ('Feature Request', 'A feature request'),
        ('A/B Experiment Proposal', 'An A/B Experiment Proposal'),
        ('A/B Experiment Review', 'An A/B Experiment Review'),
        ('A/B Experiment Setup', 'An A/B Experiment Setup'),
        ('A/B Experiment Requirements', 'An A/B Experiment Requirements'),
        ('Directive', 'An instruction to prioritise implementation of a '
                      'feature'),
        ('Response', 'A response to a customer'),
    ]

    GROUPS = [
        'User',
        'Support',
        'Product',
        'Marketing',
        'Operations',
        'Support Interface',
        'User Interface',
    ]

    FACETS = [
        'User Interface',
        'Support Interface'
    ]

    CONTENT_TYPES = [
        ('User', 'User Interface', 'Use'),
        ('User', 'User Interface', 'Query'),
        ('User', 'User Interface', 'Use Pattern'),
        ('Support', 'User Interface', 'Response'),
        ('Support', 'User Interface', 'Bug Report'),
        ('Support', 'User Interface', 'Feature Request'),
        ('Product', 'User Interface', 'Concept'),
        ('Product', 'User Interface', 'Proposal'),
        ('Product', 'User Interface', 'Requirements Document'),
        ('Product', 'User Interface', 'Directive'),
        ('Product', 'User Interface', 'Build Ticket'),
        ('Product', 'User Interface', 'Test Product'),
        ('Product', 'User Interface', 'Test'),
        ('Product', 'User Interface', 'Deployed Product'),
        ('Marketing', 'User Interface', 'A/B Experiment Proposal'),
        ('Marketing', 'User Interface', 'A/B Experiment Review'),
        ('Marketing', 'User Interface', 'A/B Experiment Setup'),
        ('Marketing', 'User Interface', 'A/B Experiment Requirements'),
        ('Support', 'Support Interface', 'Use'),
        ('Support', 'Support Interface', 'Query'),
        ('Support', 'Support Interface', 'Use Pattern'),
        ('Product', 'Support Interface', 'Proposal'),
        ('Operations', 'Support Interface', 'Bug Report'),
        ('Operations', 'Support Interface', 'Feature Request'),
        ('Product', 'Support Interface', 'Concept'),
        ('Product', 'Support Interface', 'Requirements Document'),
        ('Product', 'Support Interface', 'Build Ticket'),
        ('Product', 'Support Interface', 'Test Product'),
        ('Product', 'Support Interface', 'Test'),
        ('Product', 'Support Interface', 'Deployed Product'),
    ]

    ROLES = [
        ('Marketing', 'Growth Hacker'),
        ('Marketing', 'Chief Marketing Officer'),
        ('Operations', 'Chief Operating Officer'),
        ('Product', 'Software Engineer'),
        ('Product', 'Test Engineer'),
        ('Product', 'UX Designer'),
        ('Product', 'Chief Technology Officer'),
        ('Product', 'Product Owner'),
        ('Product', 'Systems Analyst'),
        ('Support', 'Customer Support'),
        ('User', 'Customer'),
    ]

    RESPONSIBILITIES = [
        (Operator.filter, ('Customer',),
            ('User', 'User Interface', 'Query'), [
                ('User', 'User Interface', 'Use')
            ]),
        (Operator.filter, ('Customer Support',),
            ('Support', 'Support Interface', 'Query'), [
                ('Support', 'Support Interface', 'Use')
            ]),
        (Operator.transform, ('Customer',),
            ('User', 'User Interface', 'Use'), [
                ('Product', 'Support Interface', 'Deployed Product'),
            ]),
        (Operator.transform, ('Customer Support',),
            ('Support', 'Support Interface', 'Use'), [
                ('Product', 'Support Interface', 'Deployed Product'),
            ]),
        (Operator.transform, ('Customer Support',),
            ('Support', 'User Interface', 'Response'), [
                ('User', 'User Interface', 'Query'),
                ('Product', 'Support Interface', 'Deployed Product'),
            ]),
        (Operator.combine, ('Customer Support',),
            ('Support', 'User Interface', 'Response'), [
                ('User', 'User Interface', 'Query'),
                ('Product', 'Support Interface', 'Deployed Product'),
            ]),
        (Operator.reduce, ('Customer Support',),
            ('User', 'User Interface', 'Use Pattern'), [
                ('User', 'User Interface', 'Query')
            ]),
        (Operator.reduce, ('Customer Support',),
            ('Support', 'User Interface', 'Bug Report'), [
                ('User', 'User Interface', 'Query')
            ]),
        (Operator.reduce, ('Chief Operating Officer',),
            ('Support', 'Support Interface', 'Use Pattern'), [
                ('Support', 'Support Interface', 'Query')
            ]),
        (Operator.reduce, ('Chief Operating Officer',),
            ('Operations', 'Support Interface', 'Bug Report'), [
                ('Support', 'Support Interface', 'Query')
            ]),
        (Operator.reduce, ('Chief Operating Officer',),
            ('Operations', 'Support Interface', 'Feature Request'), [
                ('Support', 'Support Interface', 'Query')
            ]),
        (Operator.reduce, ('Customer Support',),
            ('Support', 'User Interface', 'Feature Request'), [
                ('User', 'User Interface', 'Query')
            ]),
        (Operator.reduce, ('Product Owner',),
            ('User', 'User Interface', 'Use Pattern'), [
                ('User', 'User Interface', 'Use')
            ]),
        (Operator.reduce, ('Chief Operating Officer',),
            ('Support', 'Support Interface', 'Use Pattern'), [
                ('Support', 'Support Interface', 'Use')
            ]),
        (Operator.combine, ('Product Owner',),
            ('Product', 'User Interface', 'Concept'), [
                ('Support', 'User Interface', 'Feature Request'),
                ('User', 'User Interface', 'Use Pattern')
            ]),
        (Operator.transform, ('Product Owner',),
            ('Product', 'User Interface', 'Directive'), [
                ('Product', 'User Interface', 'Requirements Document')
            ]),
        (Operator.transform, ('UX Designer',),
            ('Product', 'User Interface', 'Requirements Document'), [
                ('Product', 'User Interface', 'Concept')
            ]),
        (Operator.transform, ('Chief Technology Officer',),
            ('Product', 'User Interface', 'Build Ticket'), [
                ('Product', 'User Interface', 'Directive')
            ]),
        (Operator.transform, ('Chief Technology Officer',),
            ('Product', 'User Interface', 'Build Ticket'), [
                ('Product', 'User Interface', 'Requirements Document')
            ]),
        (Operator.transform, ('Chief Technology Officer',),
            ('Product', 'Support Interface', 'Build Ticket'), [
                ('Product', 'Support Interface', 'Requirements Document')
            ]),
        (Operator.sort, ('Product Owner',),
            ('Support', 'User Interface', 'Bug Report'), [
                ('Support', 'User Interface', 'Bug Report')
            ]),
        (Operator.transform, ('Chief Technology Officer',),
            ('Product', 'User Interface', 'Build Ticket'), [
                ('Support', 'User Interface', 'Bug Report')
            ]),
        (Operator.transform, ('Software Engineer',),
            ('Product', 'Support Interface', 'Proposal'), [
                ('Operations', 'Support Interface', 'Bug Report')
            ]),
        (Operator.transform, ('Software Engineer',),
            ('Product', 'User Interface', 'Test Product'), [
                ('Product', 'User Interface', 'Build Ticket')
            ]),
        (Operator.transform, ('Software Engineer',),
            ('Product', 'Support Interface', 'Test Product'), [
                ('Product', 'Support Interface', 'Build Ticket')
            ]),
        (Operator.transform, ('Test Engineer',),
            ('Product', 'User Interface', 'Test'), [
                ('Product', 'User Interface', 'Test Product')
            ]),
        (Operator.transform, ('Test Engineer',),
            ('Product', 'Support Interface', 'Test'), [
                ('Product', 'Support Interface', 'Test Product')
            ]),
        (Operator.filter, ('Test Engineer',),
            ('Product', 'User Interface', 'Build Ticket'), [
                ('Product', 'User Interface', 'Test')
            ]),
        (Operator.filter, ('Test Engineer',),
            ('Product', 'Support Interface', 'Build Ticket'), [
                ('Product', 'Support Interface', 'Test')
            ]),
        (Operator.combine, ('Test Engineer',),
            ('Product', 'User Interface', 'Deployed Product'), [
                ('Product', 'User Interface', 'Test'),
                ('Product', 'User Interface', 'Test Product'),
            ]),
        (Operator.combine, ('Test Engineer',),
            ('Product', 'Support Interface', 'Deployed Product'), [
                ('Product', 'Support Interface', 'Test'),
                ('Product', 'Support Interface', 'Test Product'),
            ]),
        (Operator.combine, ('Growth Hacker',),
            ('Marketing', 'User Interface', 'A/B Experiment Proposal'), [
                ('Support', 'User Interface', 'Feature Request'),
                ('User', 'User Interface', 'Use')
            ]),
        (Operator.transform, ('Chief Marketing Officer',),
            ('Marketing', 'User Interface', 'A/B Experiment Review'), [
                ('Marketing', 'User Interface', 'A/B Experiment Proposal')
            ]),
        (Operator.transform, ('Growth Hacker',),
            ('Marketing', 'User Interface', 'A/B Experiment Setup'), [
                ('Marketing', 'User Interface', 'A/B Experiment Review')
            ]),
        (Operator.transform, ('Growth Hacker',),
            ('Marketing', 'User Interface', 'A/B Experiment Requirements'), [
                ('Marketing', 'User Interface', 'A/B Experiment Setup')
            ]),
        (Operator.transform, ('Chief Technology Officer',),
            ('Product', 'User Interface', 'Requirements Document'), [
                ('Marketing', 'User Interface', 'A/B Experiment Requirements')
            ]),
        (Operator.transform, ('Chief Technology Officer',),
            ('Product', 'Support Interface', 'Build Ticket'), [
                ('Operations', 'Support Interface', 'Bug Report')
            ]),
        (Operator.combine, ('Systems Analyst',),
            ('Product', 'Support Interface', 'Concept'), [
                ('Operations', 'Support Interface', 'Feature Request'),
                ('Operations', 'Support Interface', 'Bug Report'),
            ]),
        (Operator.combine, ('Systems Analyst',),
            ('Product', 'Support Interface', 'Requirements Document'), [
                ('Product', 'Support Interface', 'Concept'),
                ('Support', 'Support Interface', 'Use Pattern'),
            ]),
    ]

    def add_arguments(self, parser):
        pass

    def create_deliverable(self, name='RaceGame'):
        self.deliverable = Deliverable.objects.create(
            name='RaceGame',
            organization=self.organization)

    def create_organization(self, name='iOSLtd'):
        self.organization = Organization.objects.create(name='iOSLtd')

    def create_formats(self):
        self.formats = {}
        with transaction.atomic():
            for name, description in self.FORMATS:
                self.formats[name] = Format.objects.create(
                    name=name,
                    description=description,
                    deliverable=self.deliverable)

    def create_groups(self):
        self.groups = {}
        with transaction.atomic():
            for name in self.GROUPS:
                self.groups[name] = Group.objects.create(
                    name=name,
                    organization=self.organization)

    def create_facets(self):
        self.facets = {}
        with transaction.atomic():
            for name in self.FACETS:
                self.facets[name] = Facet.objects.create(
                    name=name,
                    deliverable=self.deliverable)

    def create_content_types(self):
        self.content_types = {}
        with transaction.atomic():
            for group, facet, format in self.CONTENT_TYPES:
                self.content_types[(group, facet, format)] = \
                    ContentType.objects.create(
                        group=self.groups[group],
                        facet=self.facets[facet],
                        format=self.formats[format],
                        deliverable=self.deliverable)

    def create_roles(self):
        self.roles = {}
        with transaction.atomic():
            for group, name in self.ROLES:
                self.roles[name] = Role.objects.create(
                    name=name,
                    group=self.groups[group])

    def create_responsibilities(self):
        self.responsibilities = {}
        with transaction.atomic():
            for operator, roles, output_type, input_types in \
                    self.RESPONSIBILITIES:
                self.responsibilities[roles, output_type] = \
                    Responsibility.objects.create(
                        output_type=self.content_types[output_type],
                        operator=operator,
                        organization=self.organization)
                for name in roles:
                    Assignment.objects.create(
                        role=self.roles[name],
                        responsibility=self.responsibilities[roles, output_type]
                    )

                for input_type in input_types:
                    self.responsibilities[roles, output_type]. \
                        input_types.through.objects.create(
                            content_type=self.content_types[input_type],
                            responsibility=
                                self.responsibilities[roles, output_type]
                        )

    def handle(self, *args, **options):
        print('Setting up test data.')
        with transaction.atomic():
            self.create_organization()
            self.create_deliverable()
            self.create_groups()
            self.create_facets()
            self.create_formats()
            self.create_content_types()
            self.create_roles()
            self.create_responsibilities()
