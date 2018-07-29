from datetime import timedelta

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from enum import Enum

import unittest.mock

from role_model.models import (
    Assignment,
    ContentType,
    Deliverable,
    Facet,
    Format,
    Group,
    Operator,
    Responsibility,
    ResponsibilityInputType,
    Role)
from crm.models import Organization


now = timezone.now()


class Command(BaseCommand):
    help = 'Set up initial data for demo app.'

    def increment_date(self):
        self.now_method.return_value = self.now_method.return_value + \
            timedelta(days=1)

    @unittest.mock.patch('django.utils.timezone.now')
    def handle(self, *args, **options):
        timezone.now.return_value = now - timedelta(days=365)
        self.now_method = timezone.now

        self.groups = {}
        self.formats = {}
        self.facets = {}
        self.responsibilities = {}
        self.content_types = {}
        self.roles = {}

        print('Deleting existing demo data.')

        Deliverable.objects.filter(
            name=settings.DEMO_DELIVERABLE_NAME).delete()
        Organization.objects.filter(
            name=settings.DEMO_ORGANIZATION_NAME).delete()

        print('Setting up initial demo data.')

        GROUP_GOVERNMENT = 'Government'
        GROUP_OPERATIONS = 'Operations'
        GROUP_PRODUCT = 'Product'
        GROUP_ASSOCIATES = 'Associates'
        ROLE_BUSINESS_REGISTER = 'australian business register'
        ROLE_TECH_FOUNDER = 'technical co-founder'
        ROLE_NON_TECH_FOUNDER = 'non-technical co-founder'
        ROLE_FRIEND = 'friend'
        FACET_UI = 'User Interface'
        FACET_HR = 'Human Resource'
        FACET_PAPER = 'Paperwork'

        FORMAT_ROLE = 'Role Design'
        FORMAT_CONCEPT = 'Concept'
        FORMAT_PRESENTATION = 'Presentation'
        FORMAT_APPLICATION = 'Application'
        FORMAT_OFFER = 'Offer'
        FORMAT_ACCEPT_OFFER = 'Accept Offer'
        FORMAT_INTEREST = 'Interest'
        FORMAT_LEGAL = 'Company Registration'

        with transaction.atomic():
            self.organization = Organization.objects.create(
                name=settings.DEMO_ORGANIZATION_NAME)
            self.deliverable = Deliverable.objects.create(
                name=settings.DEMO_DELIVERABLE_NAME,
                organization=self.organization)

            self.add_group(GROUP_PRODUCT)
            self.add_role(ROLE_TECH_FOUNDER, GROUP_PRODUCT)
            self.add_facet(FACET_UI)
            self.add_format(FORMAT_CONCEPT)
            self.add_content_type(GROUP_PRODUCT, FACET_UI, FORMAT_CONCEPT)
            self.add_responsibility('idea', [],
                (GROUP_PRODUCT, FACET_UI, FORMAT_CONCEPT))
            self.add_format(FORMAT_PRESENTATION)
            self.add_content_type(GROUP_PRODUCT, FACET_UI, FORMAT_PRESENTATION)
            self.add_responsibility('present', [
                    (GROUP_PRODUCT, FACET_UI, FORMAT_CONCEPT)
                ],
                (GROUP_PRODUCT, FACET_UI, FORMAT_PRESENTATION))
            self.add_assignment(ROLE_TECH_FOUNDER, 'idea', 'present')
            self.add_group(GROUP_ASSOCIATES)
            self.add_role(ROLE_FRIEND, GROUP_ASSOCIATES)
            self.add_format(FORMAT_APPLICATION)
            self.add_format(FORMAT_INTEREST)
            self.add_content_type(GROUP_ASSOCIATES, FACET_UI, FORMAT_INTEREST)
            self.add_responsibility('listen', [
                    (GROUP_PRODUCT, FACET_UI, FORMAT_PRESENTATION)
                ],
                (GROUP_ASSOCIATES, FACET_UI, FORMAT_INTEREST))
            self.add_assignment(ROLE_FRIEND, 'listen')
            self.add_format(FORMAT_OFFER)
            self.add_content_type(GROUP_PRODUCT, FACET_UI, FORMAT_OFFER)
            self.add_responsibility('offer', [
                    (GROUP_ASSOCIATES, FACET_UI, FORMAT_INTEREST)
                ],
                (GROUP_PRODUCT, FACET_UI, FORMAT_OFFER))
            self.add_assignment(ROLE_TECH_FOUNDER, 'offer')
            self.add_format(FORMAT_ACCEPT_OFFER)
            self.add_content_type(GROUP_ASSOCIATES, FACET_UI,
                                  FORMAT_ACCEPT_OFFER)
            self.add_responsibility('accept_offer', [
                    (GROUP_PRODUCT, FACET_UI, FORMAT_OFFER)
                ],
                (GROUP_ASSOCIATES, FACET_UI, FORMAT_ACCEPT_OFFER))
            self.add_assignment(ROLE_FRIEND, 'accept_offer')
            self.add_facet(FACET_HR)
            self.add_format(FORMAT_ROLE)
            self.add_content_type(GROUP_PRODUCT, FACET_HR, FORMAT_ROLE)
            self.add_responsibility('add_role', [
                    (GROUP_ASSOCIATES, FACET_UI, FORMAT_ACCEPT_OFFER)
                ],
                (GROUP_PRODUCT, FACET_HR, FORMAT_ROLE))
            self.add_assignment(ROLE_TECH_FOUNDER, 'add_role')
            self.add_group(GROUP_OPERATIONS)
            self.add_role(ROLE_NON_TECH_FOUNDER, GROUP_OPERATIONS)
            self.add_facet(FACET_PAPER)
            self.add_format(FORMAT_LEGAL)
            self.add_content_type(GROUP_OPERATIONS, FACET_PAPER, FORMAT_LEGAL)
            self.add_responsibility('paperwork', [
                    (GROUP_PRODUCT, FACET_HR, FORMAT_ROLE)
                ],
                (GROUP_OPERATIONS, FACET_PAPER, FORMAT_LEGAL))
            self.add_assignment(ROLE_NON_TECH_FOUNDER, 'paperwork')
            self.delete_role(ROLE_FRIEND)
            self.add_group(GROUP_GOVERNMENT)
            self.add_role(ROLE_BUSINESS_REGISTER, GROUP_GOVERNMENT)
            self.add_content_type(GROUP_GOVERNMENT, FACET_PAPER, FORMAT_LEGAL)
            self.add_responsibility('government_paperwork', [
                    (GROUP_OPERATIONS, FACET_PAPER, FORMAT_LEGAL)
                ],
                (GROUP_GOVERNMENT, FACET_PAPER, FORMAT_LEGAL))
            self.add_assignment(ROLE_BUSINESS_REGISTER, 'government_paperwork')

    def add_group(self, name):
        self.increment_date()
        self.groups[name] = Group.objects.create(
            name=name,
            organization=self.organization)
        return self.groups[name]

    def add_role(self, name, group):
        self.increment_date()
        self.roles[name] = Role.objects.create(
            name=name,
            group=self.groups[group])
        return self.roles[name]

    def delete_role(self, name):
        self.increment_date()
        self.roles[name].mark_as_deleted(save=True)

    def add_facet(self, name):
        self.increment_date()
        self.facets[name] = Facet.objects.create(
            name=name,
            deliverable=self.deliverable)
        return self.facets[name]

    def add_format(self, name):
        self.increment_date()
        self.formats[name] = Format.objects.create(
            name=name,
            deliverable=self.deliverable)
        return self.formats[name]

    def add_content_type(self, group, facet, format):
        self.increment_date()
        self.content_types[(group, facet, format)] = \
            ContentType.objects.create(
                group=self.groups[group],
                facet=self.facets[facet],
                format=self.formats[format],
                deliverable=self.deliverable)
        return self.content_types[(group, facet, format)]

    def add_responsibility(self, name, input_types, output_type):
        self.increment_date()
        self.responsibilities[name] = \
            Responsibility.objects.create(
                operator=Operator.transform,
                output_type=self.content_types[output_type],
                organization=self.organization)

        for input_type in input_types:
            ResponsibilityInputType.objects.create(
                content_type=self.content_types[input_type],
                responsibility=self.responsibilities[name])
        return self.responsibilities[name]

    def add_assignment(self, role, *responsibilities):
        self.increment_date()
        for responsibility in responsibilities:
            Assignment.objects.create(
                role=self.roles[role],
                responsibility=self.responsibilities[responsibility])
