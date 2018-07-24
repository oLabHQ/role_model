# Generated by Django 2.0.7 on 2018-07-24 10:14

import common.models
import crm.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=common.models.EnumField(choices=[(crm.models.UserType('site_inactive'), 'site_inactive'), (crm.models.UserType('site_superuser'), 'site_superuser'), (crm.models.UserType('site_support'), 'site_support'), (crm.models.UserType('organization_inactive'), 'organization_inactive'), (crm.models.UserType('organization_administrator'), 'organization_administrator'), (crm.models.UserType('organization_member'), 'organization_member')], max_length=64),
        ),
    ]
