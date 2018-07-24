# Generated by Django 2.0.7 on 2018-07-24 15:59

import common.models
from django.conf import settings
from django.db import migrations, models
import django_extensions.db.fields
import django_fsm
import role_model.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('crm', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('status', django_fsm.FSMField(choices=[(role_model.models.Status('formal'), 'formal'), (role_model.models.Status('ad_hoc'), 'ad_hoc'), (role_model.models.Status('adjunct'), 'adjunct')], default=role_model.models.Status('formal'), max_length=50)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ContentType',
            fields=[
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
            ],
            options={
                'base_manager_name': 'objects',
            },
        ),
        migrations.CreateModel(
            name='Deliverable',
            fields=[
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64)),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from=['name'])),
                ('organization', models.ForeignKey(on_delete='CASCADE', to='crm.Organization')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Facet',
            fields=[
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64)),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from=['name'])),
                ('deliverable', models.ForeignKey(on_delete='CASCADE', related_name='facets', to='role_model.Deliverable')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Format',
            fields=[
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64)),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from=['name'])),
                ('description', models.TextField(max_length=1024)),
                ('deliverable', models.ForeignKey(on_delete='CASCADE', related_name='formats', to='role_model.Deliverable')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64)),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from=['name'])),
                ('organization', models.ForeignKey(on_delete='CASCADE', to='crm.Organization')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Responsibility',
            fields=[
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('operator', common.models.EnumField(choices=[(role_model.models.Operator('transform'), 'transform'), (role_model.models.Operator('reduce'), 'reduce'), (role_model.models.Operator('sort'), 'sort'), (role_model.models.Operator('filter'), 'filter'), (role_model.models.Operator('combine'), 'combine')], max_length=64)),
                ('input_types', models.ManyToManyField(related_name='outputs', to='role_model.ContentType')),
                ('organization', models.ForeignKey(on_delete='CASCADE', to='crm.Organization')),
                ('output_type', models.ForeignKey(on_delete='CASCADE', related_name='inputs', to='role_model.ContentType')),
            ],
            options={
                'verbose_name_plural': 'responsibilities',
                'base_manager_name': 'objects',
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64)),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from=['name'])),
                ('group', models.ForeignKey(on_delete='CASCADE', related_name='roles', to='role_model.Group')),
                ('responsibilities', models.ManyToManyField(to='role_model.Responsibility')),
                ('users', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'base_manager_name': 'objects',
            },
        ),
        migrations.AddField(
            model_name='contenttype',
            name='deliverable',
            field=models.ForeignKey(on_delete='CASCADE', related_name='content_types', to='role_model.Deliverable'),
        ),
        migrations.AddField(
            model_name='contenttype',
            name='facet',
            field=models.ForeignKey(on_delete='CASCADE', to='role_model.Facet'),
        ),
        migrations.AddField(
            model_name='contenttype',
            name='format',
            field=models.ForeignKey(on_delete='CASCADE', to='role_model.Format'),
        ),
        migrations.AddField(
            model_name='contenttype',
            name='group',
            field=models.ForeignKey(on_delete='CASCADE', to='role_model.Group'),
        ),
        migrations.AddField(
            model_name='assignment',
            name='responsibility',
            field=models.ForeignKey(on_delete='CASCADE', to='role_model.Responsibility'),
        ),
        migrations.AddField(
            model_name='assignment',
            name='role',
            field=models.ForeignKey(on_delete='CASCADE', to='role_model.Role'),
        ),
    ]
