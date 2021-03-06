# Generated by Django 2.0.7 on 2018-07-31 13:57

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('object_id', models.UUIDField(editable=False)),
                ('is_created', models.BooleanField(default=False)),
                ('delta', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('serialized_data', django.contrib.postgres.fields.jsonb.JSONField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name_plural': 'histories',
                'ordering': ['-id'],
                'base_manager_name': 'objects',
            },
        ),
        migrations.CreateModel(
            name='MigrationState',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('app_migrations', django.contrib.postgres.fields.jsonb.JSONField()),
                ('applied_migrations', django.contrib.postgres.fields.jsonb.JSONField(unique=True)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='history',
            name='migration_state',
            field=models.ForeignKey(on_delete='CASCADE', to='history.MigrationState'),
        ),
    ]
