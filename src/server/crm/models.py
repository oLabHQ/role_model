from enum import auto

from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import models

from common.models import (
    NameSlugTimeStampedUUIDModel, TimeStampedUUIDModel, Choices)

from crm.validators import validate_mobile


class Organization(NameSlugTimeStampedUUIDModel):
    """
    use_email_id: Whether user's belonging to this customer organization
                  will use email to login or a generic username.
    """
    use_email_id = models.BooleanField(default=True)


class UserManager(BaseUserManager):
    def create_user(self, username=None, password=None, **kwargs):
        """
        Returns a new persisted user, given username and password.
        """
        user = self.model(**kwargs)
        user.username = username
        user.set_password(password)
        user.clean()
        user.save(using=self._db)
        return user

    def create_superuser(self, password=None, **kwargs):
        """
        Returns a new persisted superuser with the given email, date of
        birth and password.
        """
        if kwargs.get('organization', None):
            raise ValueError('organization not expected in kwargs for '
                             'User.objects.create_superuser')

        user = self.create_user(
            password=password,
            **kwargs
        )
        user.user_type = User.UserType.site_superuser
        user.save(using=self._db)
        return user


class User(PermissionsMixin, TimeStampedUUIDModel, AbstractBaseUser):
    class UserType(Choices):
        """
        site_*: Types of user for support people within our organization.
        site_inactive: The user is disabled and cannot login.
        site_superuser: The user is authorized to perform any action on admin
                        interface.
        site_support: The user has limited privileges to perform actions on the
                      admin interface for the purpose of supporting our
                      customers.
        """
        site_inactive = auto()
        site_superuser = auto()
        site_support = auto()

        """
        organization_*: Types of user designated to our customers.
        """
        organization_inactive = auto()
        organization_administrator = auto()
        organization_member = auto()

    site_user_types = [
        UserType.site_inactive,
        UserType.site_superuser,
        UserType.site_support
    ]

    organization_user_types = [
        UserType.organization_inactive,
        UserType.organization_administrator,
        UserType.organization_member
    ]

    first_name = models.CharField(verbose_name='first name', max_length=64)
    last_name = models.CharField(verbose_name='last name', max_length=64)

    username = models.CharField('username', max_length=255, unique=True)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        null=False,
        blank=True,
    )
    mobile = models.CharField(
        verbose_name='mobile',
        max_length=255,
        null=False,
        blank=True,
        validators=[validate_mobile])

    # Customer support for our website have no organization.
    organization = models.ForeignKey(
        'Organization',
        verbose_name='organization',
        null=True, blank=True,
        on_delete='CASCADE')

    user_type = UserType.Field()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    def clean(self):
        if not self.user_type:
            """
            Set default user type if absent.
            """
            self.user_type = User.UserType.organization_inactive \
                if self.organization else User.UserType.site_inactive

        if not self.organization or self.organization.use_email_id:
            """
            Set default username.
            Our site: use email.
            Our customer: use email or any string depending on configuration.
            """
            if not self.username:
                self.username = self.email

            try:
                validate_email(self.username)
            except ValidationError:
                raise
            else:
                if self.email:
                    self.username = self.email
                    validate_email(self.username)

    @property
    def is_site_user(self):
        """
        A site user has a site user type and *does not* have organization.
        """
        return self.user_type in self.site_user_types and not self.organization

    @property
    def is_organization_user(self):
        """
        A customer user has a organization user type and *does* have
        organization.
        """
        return self.user_type in self.organization_user_types \
            and self.organization

    @property
    def is_superuser(self):
        """
        Returns whether the user is a superuser, to interact with Django's
        auth and admin framework.
        """
        return self.is_site_user \
            and self.user_type == User.UserType.site_superuser

    @property
    def is_staff(self):
        """
        Returns whether the user is a staff. This property is required to
        interact with Django's auth and admin framework. A staff can login to
        admin interface.
        """
        return self.is_site_user

    @property
    def is_active(self):
        """
        Returns whether the user is an active user.
        Returns False if the user does not have a valid state.
        """
        if self.is_site_user:
            return self.user_type != User.UserType.site_inactive

        if self.is_organization_user:
            return self.user_type != User.UserType.organization_inactive

        return False


UserType = User.UserType
