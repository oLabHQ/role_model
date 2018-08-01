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
        ROLE_BUSINESS_REGISTER = 'australian business register'

        GROUP_OPERATIONS = 'Operations'
        ROLE_NON_TECH_FOUNDER = 'non-technical co-founder'
        ROLE_SUPPORT = 'customer support'

        GROUP_PRODUCT = 'Product'
        ROLE_TECH_FOUNDER = 'technical co-founder'
        ROLE_DESIGN = 'UX designer'
        ROLE_ENGINEER = 'Software Engineer'
        ROLE_CUSTOMER = 'Customer'

        GROUP_ASSOCIATES = 'Associates'
        ROLE_FRIEND = 'friend'

        GROUP_MARKET = 'Market'
        ROLE_LEAD = 'lead'

        FACET_UI = 'User Interface'
        FACET_HR = 'Human Resource'
        FACET_PAPER = 'Paperwork'

        FORMAT_ROLE = 'Role Design'
        FORMAT_CONCEPT = 'Concept'
        FORMAT_REQUIREMENTS = 'Requiremments Document'
        FORMAT_IMPLEMENTATION_PLAN = 'Implementation Plan'
        FORMAT_TEST_PRODUCT = 'Test Product'
        FORMAT_TEST = 'Test'
        FORMAT_DEPLOYMENT = 'Deployment'
        FORMAT_DEPLOYED_PRODUCT = 'Deployed Product'
        FORMAT_USER_QUERY = 'User Query'
        FORMAT_USER_RESPONSE = 'Response'
        FORMAT_PRESENTATION = 'Presentation'
        FORMAT_APPLICATION = 'Application'
        FORMAT_OFFER = 'Offer'
        FORMAT_ACCEPT_OFFER = 'Accept Offer'
        FORMAT_INTEREST = 'Interest'
        FORMAT_LEGAL = 'Company Registration'
        FORMAT_EMAIL = 'Email'
        FORMAT_MEETING = 'Meeting'
        FORMAT_MEETING_INVITE = 'Meeting Invite'
        FORMAT_USE = 'Use'
        FORMAT_MARKET_ANALYSIS = 'Market Analysis'

        with transaction.atomic():
            self.organization = Organization.objects.create(
                name=settings.DEMO_ORGANIZATION_NAME)
            self.deliverable = Deliverable.objects.create(
                name=settings.DEMO_DELIVERABLE_NAME,
                organization=self.organization)

            self.add_role(ROLE_TECH_FOUNDER, GROUP_PRODUCT)
            self.add_responsibility('idea', [],
                (GROUP_PRODUCT, FACET_UI, FORMAT_CONCEPT))
            self.add_responsibility('present', [
                    (GROUP_PRODUCT, FACET_UI, FORMAT_CONCEPT)
                ],
                (GROUP_PRODUCT, FACET_UI, FORMAT_PRESENTATION))
            self.add_assignment(ROLE_TECH_FOUNDER, 'idea', 'present')
            self.add_role(ROLE_FRIEND, GROUP_ASSOCIATES)
            self.delete_assignment(ROLE_TECH_FOUNDER, 'idea', 'present')
            self.add_responsibility('listen', [
                    (GROUP_PRODUCT, FACET_UI, FORMAT_PRESENTATION)
                ],
                (GROUP_ASSOCIATES, FACET_UI, FORMAT_INTEREST))
            self.add_assignment(ROLE_FRIEND, 'listen')
            self.add_responsibility('offer', [
                    (GROUP_ASSOCIATES, FACET_UI, FORMAT_INTEREST)
                ],
                (GROUP_PRODUCT, FACET_UI, FORMAT_OFFER))
            self.add_assignment(ROLE_TECH_FOUNDER, 'offer')
            self.add_responsibility('accept_offer', [
                    (GROUP_PRODUCT, FACET_UI, FORMAT_OFFER)
                ],
                (GROUP_ASSOCIATES, FACET_UI, FORMAT_ACCEPT_OFFER))
            self.add_assignment(ROLE_FRIEND, 'accept_offer')
            self.add_responsibility('add_role', [
                    (GROUP_ASSOCIATES, FACET_UI, FORMAT_ACCEPT_OFFER)
                ],
                (GROUP_PRODUCT, FACET_HR, FORMAT_ROLE))
            self.add_assignment(ROLE_TECH_FOUNDER, 'add_role')
            self.delete_assignment(ROLE_TECH_FOUNDER, 'idea')
            self.delete_assignment(ROLE_TECH_FOUNDER, 'present')
            self.add_role(ROLE_NON_TECH_FOUNDER, GROUP_OPERATIONS)
            self.add_responsibility('paperwork', [
                    (GROUP_PRODUCT, FACET_HR, FORMAT_ROLE)
                ],
                (GROUP_OPERATIONS, FACET_PAPER, FORMAT_LEGAL))
            self.add_assignment(ROLE_NON_TECH_FOUNDER, 'paperwork')
            self.delete_role(ROLE_FRIEND)
            self.add_role(ROLE_BUSINESS_REGISTER, GROUP_GOVERNMENT)
            self.add_responsibility('government_receive_paperwork', [
                    (GROUP_OPERATIONS, FACET_PAPER, FORMAT_LEGAL)
                ],
                (GROUP_GOVERNMENT, FACET_PAPER, FORMAT_LEGAL))
            self.add_assignment(ROLE_BUSINESS_REGISTER,
                'government_receive_paperwork')
            self.add_responsibility('government_paperwork', [
                    (GROUP_GOVERNMENT, FACET_PAPER, FORMAT_LEGAL)
                ],
                (GROUP_GOVERNMENT, FACET_PAPER, FORMAT_LEGAL))
            self.add_assignment(ROLE_BUSINESS_REGISTER,
                'government_paperwork')

            self.add_role(ROLE_LEAD, GROUP_MARKET)
            self.add_responsibility('send_lead_email', [
                    (GROUP_PRODUCT, FACET_UI, FORMAT_CONCEPT)
                ],
                (GROUP_PRODUCT, FACET_UI, FORMAT_EMAIL))
            self.add_assignment(ROLE_TECH_FOUNDER, 'send_lead_email')
            self.add_assignment(ROLE_NON_TECH_FOUNDER, 'send_lead_email')

            self.add_responsibility('receive_lead_email', [
                    (GROUP_PRODUCT, FACET_UI, FORMAT_EMAIL)
                ],
                (GROUP_MARKET, FACET_UI, FORMAT_EMAIL))
            self.add_assignment(ROLE_LEAD, 'receive_lead_email')

            self.add_responsibility('receive_lead_email_response', [
                    (GROUP_MARKET, FACET_UI, FORMAT_EMAIL)
                ],
                (GROUP_PRODUCT, FACET_UI, FORMAT_MEETING_INVITE))
            self.add_assignment(ROLE_NON_TECH_FOUNDER,
                                'receive_lead_email_response')

            self.add_responsibility('accept_meeting', [
                    (GROUP_MARKET, FACET_UI, FORMAT_MEETING_INVITE)
                ],
                (GROUP_PRODUCT, FACET_UI, FORMAT_MEETING))
            self.add_assignment(ROLE_TECH_FOUNDER,
                                'accept_meeting')

            self.add_responsibility('refine_concepts', [
                    (GROUP_PRODUCT, FACET_UI, FORMAT_MEETING)
                ],
                (GROUP_PRODUCT, FACET_UI, FORMAT_CONCEPT))
            self.add_assignment(ROLE_TECH_FOUNDER,
                                'refine_concepts')
            self.add_assignment(ROLE_NON_TECH_FOUNDER,
                                'refine_concepts')

            self.add_responsibility('design_concepts', [
                    (GROUP_PRODUCT, FACET_UI, FORMAT_CONCEPT)
                ],
                (GROUP_PRODUCT, FACET_UI, FORMAT_REQUIREMENTS))

            self.add_role(ROLE_DESIGN, GROUP_PRODUCT)
            self.add_assignment(ROLE_DESIGN,
                                'design_concepts')

            self.delete_assignment(ROLE_NON_TECH_FOUNDER, 'refine_concepts')
            self.delete_assignment(ROLE_TECH_FOUNDER, 'refine_concepts')
            self.add_responsibility('build_plan', [
                    (GROUP_PRODUCT, FACET_UI, FORMAT_REQUIREMENTS)
                ],
                (GROUP_PRODUCT, FACET_UI, FORMAT_IMPLEMENTATION_PLAN))
            self.add_responsibility('write_code', [
                    (GROUP_PRODUCT, FACET_UI, FORMAT_IMPLEMENTATION_PLAN)
                ],
                (GROUP_PRODUCT, FACET_UI, FORMAT_TEST_PRODUCT))
            self.add_responsibility('pre_prod_test', [
                    (GROUP_PRODUCT, FACET_UI, FORMAT_TEST_PRODUCT)
                ],
                (GROUP_PRODUCT, FACET_UI, FORMAT_TEST))
            self.add_responsibility('prod_deployment', [
                    (GROUP_PRODUCT, FACET_UI, FORMAT_TEST)
                ],
                (GROUP_PRODUCT, FACET_UI, FORMAT_DEPLOYMENT))

            self.add_responsibility('deployed_product', [
                    (GROUP_PRODUCT, FACET_UI, FORMAT_DEPLOYMENT)
                ],
                (GROUP_PRODUCT, FACET_UI, FORMAT_DEPLOYED_PRODUCT))
            self.add_role(ROLE_ENGINEER, GROUP_PRODUCT)
            self.add_assignment(ROLE_ENGINEER, 'build_plan',
                                   'write_code', 'prod_deployment',
                                   'deployed_product', 'write_code',
                                   'pre_prod_test')


            self.add_responsibility('trial_product', [
                   (GROUP_PRODUCT, FACET_UI, FORMAT_DEPLOYED_PRODUCT)
               ],
               (GROUP_PRODUCT, FACET_UI, FORMAT_USER_QUERY))

            self.add_assignment(ROLE_LEAD, 'trial_product')

            self.add_role(ROLE_SUPPORT, GROUP_OPERATIONS)

            self.add_responsibility('response_to_user', [
                  (GROUP_PRODUCT, FACET_UI, FORMAT_USER_QUERY)
              ],
              (GROUP_PRODUCT, FACET_UI, FORMAT_USER_RESPONSE))

            self.add_assignment(ROLE_SUPPORT, 'response_to_user')

            self.add_responsibility('purchase_product', [
                 (GROUP_PRODUCT, FACET_UI, FORMAT_USER_RESPONSE)
             ],
             (GROUP_PRODUCT, FACET_UI, FORMAT_USE))

            self.add_responsibility('use_product', [
                  (GROUP_PRODUCT, FACET_UI, FORMAT_DEPLOYED_PRODUCT)
              ],
              (GROUP_PRODUCT, FACET_UI, FORMAT_USE))

            self.add_assignment(ROLE_LEAD, 'purchase_product')

            self.add_role(ROLE_CUSTOMER, GROUP_MARKET)
            self.add_assignment(ROLE_CUSTOMER, 'purchase_product',
                'use_product', 'trial_product')

            self.delete_role(ROLE_LEAD)
            self.add_responsibility('market_analysis', [
                  (GROUP_PRODUCT, FACET_UI, FORMAT_USE)
              ],
              (GROUP_PRODUCT, FACET_UI, FORMAT_MARKET_ANALYSIS))

            self.add_assignment(ROLE_NON_TECH_FOUNDER, 'market_analysis')





    def add_group(self, name):
        self.increment_date()
        self.groups[name] = Group.objects.create(
            name=name,
            organization=self.organization)
        return self.groups[name]

    def add_role(self, name, group):
        if group not in self.groups:
            self.add_group(group)

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
        if not group in self.groups:
            self.add_group(group)

        if not facet in self.facets:
            self.add_facet(facet)

        if not format in self.formats:
            self.add_format(format)

        self.increment_date()
        self.content_types[(group, facet, format)] = \
            ContentType.objects.create(
                group=self.groups[group],
                facet=self.facets[facet],
                format=self.formats[format],
                deliverable=self.deliverable)
        return self.content_types[(group, facet, format)]

    def add_responsibility(self, name, input_types, output_type):
        if output_type not in self.content_types:
            self.add_content_type(*output_type)

        for input_type in input_types:
            if input_type not in self.content_types:
                self.add_content_type(*input_type)

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

    def delete_assignment(self, role, *responsibilities):
        self.increment_date()
        for responsibility in responsibilities:
            Assignment.objects.get(
                role=self.roles[role],
                responsibility=self.responsibilities[responsibility]
            ).mark_as_deleted(save=True)

    def add_assignment(self, role, *responsibilities):
        self.increment_date()
        for responsibility in responsibilities:
            Assignment.objects.undelete_or_create(
                role=self.roles[role],
                responsibility=self.responsibilities[responsibility])
