from enum import auto

from django.conf import settings
from django.db import models

from aldjemy.meta import AldjemyMeta

from common.models import (
    Choices, States, TimeStampedUUIDModel, NameSlugTimeStampedUUIDModel,
    UUIDModel)
from common.language import join_and


class Ownership(models.Model):
    """
    Instances of the inherited model belongs to `organization`.
    """
    organization = models.ForeignKey(settings.ROLE_MODEL_ORGANIZATION_MODEL,
                                     on_delete='CASCADE')

    class Meta:
        abstract = True


class Deliverable(Ownership, NameSlugTimeStampedUUIDModel,
                  metaclass=AldjemyMeta):
    """
    The thing a group of employees are producing together.
    """


class Group(Ownership, NameSlugTimeStampedUUIDModel, metaclass=AldjemyMeta):
    """
    Each role belong to a group.
    """


class Format(NameSlugTimeStampedUUIDModel, metaclass=AldjemyMeta):
    """
    A format of an output of a responsibility.
    It can be a document, code, questions, even usage generating analytics
    data.
    """
    description = models.TextField(null=False, max_length=1024)
    deliverable = models.ForeignKey('Deliverable', related_name='formats',
                                    on_delete='CASCADE')

    @property
    def organization(self):
        return self.deliverable.organization


class Facet(NameSlugTimeStampedUUIDModel, metaclass=AldjemyMeta):
    """
    One face of the product, or product's data.
    For example, a product may have the following facets:
    1. User Interface
    2. Admin Interface
    3. Analytics Interface
    """
    deliverable = models.ForeignKey('Deliverable',
                                    related_name='facets', on_delete='CASCADE')

    @property
    def organization(self):
        return self.deliverable.organization


class ContentTypeManager(models.Manager):
    """
    Set default select_related.
    Reduces 90% of queries on the Responsibility Admin Change Form page.
    """
    def get_queryset(self):
        return super().get_queryset().select_related(
            'deliverable',
            'deliverable__organization',
            'group',
            'facet',
            'format')


class ContentType(TimeStampedUUIDModel, metaclass=AldjemyMeta):
    """
    A content produced by an employee in the course of the company producing
    a product.
    For example:
    1. "RaceGame:Product:User Interface<Requirements Document>"
       A requirements document describing a feature to be constructed for
       the user interface of RaceGame.
    2. "RaceGame:Product:User Interface<Build Ticket>"
       A JIRA ticket describing work required to construct a feature for
       RaceGame.
    """
    deliverable = models.ForeignKey('Deliverable',
                                    related_name='content_types',
                                    on_delete='CASCADE')
    group = models.ForeignKey('Group', on_delete='CASCADE')
    facet = models.ForeignKey('Facet', on_delete='CASCADE')
    format = models.ForeignKey('Format', on_delete='CASCADE')

    objects = ContentTypeManager()

    class Meta:
        base_manager_name = 'objects'

    def __str__(self):
        return ":".join([str(self.deliverable), str(self.group),
                         ("{}<{}>").format(self.facet, self.format)])

    @property
    def organization(self):
        return self.deliverable.organization

    def prose(self, plural=False):
        """
        Returns an english representation of this content type.
        For example:
        "PRODUCT's concept of RaceGame's support interface"
        """
        return "{group}'s {format}{plural} of {deliverable}'s {facet}".format(
            group=str(self.group).upper(),
            plural="(s)" if plural else "",
            format=str(self.format).lower(),
            deliverable=str(self.deliverable),
            facet=str(self.facet).lower())


class Assignment(TimeStampedUUIDModel, metaclass=AldjemyMeta):
    class Status(States):
        """
        Describes how the responsibility was assigned.
        1. formal: In an explict email or in job description.
        2. ad_hoc: Implictly expected as part of day to day work.
        3. adjunct: Not assigned to or expected, but performed due to business
                    need, possibly in an sub-optimal manner.
        """
        formal = auto()
        ad_hoc = auto()
        adjunct = auto()

    STATUS_HELP_TEXT = {
        Status.formal: (
            "A formal responsibility. "
            "For example, specified in job description."),
        Status.ad_hoc: (
            "An ad hoc responsibility. "
            "A responsibility routinely performed, and is expected"
            " for the role, but not formally expressed."),
        Status.adjunct: (
            "An adjunct responsibility. "
            "e.g. a task routinely done due to requirements "
            "of the business, but was not and is not expected for"
            "the role to perform."),
    }

    role = models.ForeignKey('Role', on_delete='CASCADE')
    responsibility = models.ForeignKey('Responsibility',
                                       on_delete='CASCADE')
    status = Status.Field(default=Status.formal)


class RoleManager(models.Manager):
    """
    Set default select_related.
    """
    def get_queryset(self):
        return super().get_queryset().select_related(
            'group').prefetch_related('responsibilities', 'users')


class Role(NameSlugTimeStampedUUIDModel, metaclass=AldjemyMeta):
    responsibilities = models.ManyToManyField('Responsibility',
                                              through='Assignment'
                                              )
    users = models.ManyToManyField(settings.AUTH_USER_MODEL)
    group = models.ForeignKey('role_model.Group',
                              related_name='roles',
                              on_delete='CASCADE')

    objects = RoleManager()

    class Meta:
        base_manager_name = 'objects'

    @property
    def organization(self):
        return self.group.organization

    def __str__(self):
        return "{} (\n  {})".format(
            super().__str__(), "\n  ".join([
                str(responsibility)
                for responsibility in self.responsibilities.all()]))


class ResponsibilityManager(models.Manager):
    """
    Set default select_related.
    Really speeds up pages where we generate a description for a list of
    responsibilities.
    """
    def get_queryset(self):
        return super().get_queryset() \
            .select_related(
                'organization',
                'output_type',
                'output_type__deliverable',
                'output_type__group',
                'output_type__facet',
                'output_type__format') \
            .prefetch_related(
                'input_types',
                'input_types__deliverable',
                'input_types__group',
                'input_types__facet',
                'input_types__format')


class ResponsibilityInputType(UUIDModel, metaclass=AldjemyMeta):
    content_type = models.ForeignKey('ContentType', on_delete='CASCADE')
    responsibility = models.ForeignKey('Responsibility',
                                       on_delete='CASCADE')


class Responsibility(Ownership, TimeStampedUUIDModel, metaclass=AldjemyMeta):
    class Operator(Choices):
        transform = auto()
        reduce = auto()
        sort = auto()
        filter = auto()
        combine = auto()

    OPERATOR_TYPE_SIGNATURE = {
        Operator.transform: (1, 2),
        Operator.reduce: (1, 2),
        Operator.sort: (1, 2),
        Operator.filter: (1, 2),
        Operator.combine: (2, None),
    }

    OPERATOR_TYPE_PROSE_FORMAT = {
        Operator.transform: "Produce a {output_type} from a {input_type}.",
        Operator.reduce: "Produce a single {output_type} from multiple "
                         "instances of {input_types}.",
        Operator.sort: "Sort {input_types} from most to least important.",
        Operator.filter: "Discard instances of {input_types} that are "
                         "irrelevant",
        Operator.combine: "Combine {input_type} into a {output_type}.",
    }

    operator = Operator.Field()
    input_types = models.ManyToManyField('role_model.ContentType',
                                         related_name='outputs',
                                         through='ResponsibilityInputType')
    output_type = models.ForeignKey('role_model.ContentType',
                                    related_name='inputs',
                                    on_delete='CASCADE')

    objects = ResponsibilityManager()

    class Meta:
        verbose_name_plural = 'responsibilities'
        base_manager_name = 'objects'

    def clean(self):
        valid_number_of_input_types = Responsibility.OPERATOR_TYPE_SIGNATURE[
            self.operator]
        print(valid_number_of_input_types)

    def prose(self):
        """
        Return English representation of this instance.
        For example:

        1. Produce a PRODUCT's build ticket of RaceGame's user interface from a
           PRODUCT's requirements document of RaceGame's user interface.

        2. Produce a PRODUCT's test product of RaceGame's user interface from a
           PRODUCT's build ticket of RaceGame's user interface.
        """
        return Responsibility.OPERATOR_TYPE_PROSE_FORMAT[self.operator].format(
            input_type=join_and(
                (value.prose(plural=False)
                    for value in self.input_types.all()), plural=False),
            input_types=join_and(
                (value.prose(plural=True)
                    for value in self.input_types.all()), plural=True),
            output_type=self.output_type.prose())

    def __str__(self):
        """
        Return string representation of this instance.
        For example:
        transform (RaceGame:Product:User Interface<Requirements Document> →
        RaceGame:Product:User Interface<Build Ticket>)
        """
        return '{} ({} → {})'.format(
            str(self.operator.value),
            ', '.join([str(value) for value in self.input_types.all()]),
            str(self.output_type))




# Copying classes to module level to ensure availability for migration files.
# TODO: Consider moving these classes out of the outer class.
Operator = Responsibility.Operator
Status = Assignment.Status
