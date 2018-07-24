import uuid
from django.db import models

from common.enum import AutoName
from django_extensions.db.fields import AutoSlugField
from django_extensions.db.models import TimeStampedModel
from django_fsm import FSMField


class UUIDModel(models.Model):
    """
    Use this base model class to use a UUID primary key.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class TimeStampedUUIDModel(TimeStampedModel, UUIDModel):
    """
    Use this base model class to use a UUID primary key, and add `created` and
    `updated` fields that will be automatically updated at appropriate times
    with the current datetime.
    """
    class Meta:
        abstract = True


class NameSlugModel(models.Model):
    """
    Use this model to add a name/slug field to a model.
    """
    name = models.CharField(null=False, max_length=64)
    slug = AutoSlugField(populate_from=['name'])

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class NameSlugTimeStampedUUIDModel(NameSlugModel, TimeStampedUUIDModel):
    """
    This base class gives the inherited model to a uuid primary key, `created`,
    `updated` fields, and a `name` and `slug` field.
    """
    class Meta:
        abstract = True


class EnumField(models.CharField):
    """
    A CharField where it's value is a `enum.AutoName` enum value, choices will
    by default be generated from values of the enum.

    Usage:
    ```
    class MyModel(models.Model):
        my_field = EnumField(enum=your_enum_class)
    ```

    Documentation for implementing custom model fields is available at:
    https://docs.djangoproject.com/en/2.0/howto/custom-model-fields/
    """
    def __init__(self, *args, **kwargs):
        """
        Initialize the field. `enum` is a required argument of kwargs.

        By implementing our enum argument, which takes a custom class, in a
        defensive manner, we avoid the need to implement a deconstruct method
        for this EnumField class.

        Relevant information about implementing the `deconstruct` method.
        https://stackoverflow.com/q/34558397
        """
        self._enum = kwargs.pop('enum', None)

        if self._enum:
            self._enum_lookup = {v.value: v for v in self._enum}

        kwargs['choices'] = kwargs.pop('choices', [
            (value, value.value) for value in self._enum
        ] if self._enum else [])

        super().__init__(*args, **kwargs)

    def get_prep_value(self, value):
        """
        Return the postgresql varchar representation. given an instance of
        `self._enum` or a python string.
        """
        if value is None or isinstance(value, str):
            return value

        if self._enum and isinstance(value, self._enum):
            return value.value

        raise TypeError(
            'Cannot prepare non-%s value to persist.',
            self._enum.__class__)

    def get_db_prep_value(self, value, connection, prepared=False):
        """
        Return the postgresql varchar representation. given an instance of
        `self._enum` or a python string.
        """
        value = super().get_db_prep_value(value, connection, prepared)

        if value is None or isinstance(value, str):
            return value

        if isinstance(value, self._enum):
            return value.value

        raise TypeError(
            'Cannot prepare non-%s value to persist into database.',
            self._enum.__class__)

    def from_db_value(self, value, expression, connection):
        """
        Return the `self._enum` instance representation given a postgresql
        varchar representation.
        """
        if value is None:
            return value

        return self._enum_lookup.get(value, value)

    def to_python(self, value):
        """
        Return the `self._enum` instance representation given a postgresql
        varchar representation.
        """
        if value is None or isinstance(value, self._enum):
            return value

        return self._enum_lookup.get(value, value)

    def run_validators(self, value):
        return super().run_validators(str(value))


class Choices(AutoName):
    """
    Use this Enum base class to create a typical Django choices CharField.

    Usage:

    ```
    from enum import auto

    class Operator(Choices):
        transform = auto()
        reduce = auto()
        sort = auto()
        filter = auto()
        combine = auto()

    class MyModel(models.Model):
        operator = Operator.Field()
    ```

    This is similar to:

    ```

    class MyModel(models.Model):
        OPERATOR_CHOICES = [
            ('transform', 'transform'),
            ('reduce', 'reduce'),
            ('sort', 'sort'),
            ('filter', 'filter'),
            ('combine', 'combine')
        ]
        operator = models.CharField(choices=OPERATOR_CHOICES, max_length=64,
                                    null=False, blank=False)
    ```

    The main difference is, `instance.operator` returns an instance of Operator
    in the first case, and `instance.operator` returns a string in the second
    case.
    """

    def __str__(self):
        return self.value

    @classmethod
    def choices(cls):
        return [(value, value.value) for value in cls]

    @classmethod
    def Field(cls, **kwargs):
        return EnumField(
            enum=cls,
            choices=cls.choices(),
            null=kwargs.pop('null', False),
            blank=kwargs.pop('blank', False),
            max_length=kwargs.pop('max_length', 64),
            **kwargs)


class States(Choices):
    """
    Use this Enum base class to create a typical FSMField, with `choices`
    defaulting to values of the inheriting Enum class.

    FSM stands for "Finite State Machine", and is useful for modelling state
    transitions.
    """

    def __str__(self):
        return self.value

    @classmethod
    def Field(cls, **kwargs):
        return FSMField(
            choices=cls.choices(),
            null=kwargs.pop('null', False),
            blank=kwargs.pop('blank', False),
            **kwargs)
