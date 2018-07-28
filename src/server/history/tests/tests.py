from django.core.management import call_command
from django.contrib.contenttypes.fields import GenericRelation
from django.test import TestCase, override_settings
from history.apps import register_models
from history.models import History
from history.tests.models import Person


class HistoryTestCase(TestCase):
    def setUp(self):
        pass

    @override_settings(
        INSTALLED_APPS=[
            'django.contrib.contenttypes',
            'history',
            'history.tests'
        ],
        HISTORY_MODELS=[])
    def test_person_history_absent(self):
        call_command('migrate', 'tests')
        register_models()

        self.person = Person.objects.create(
            first_name="Bob",
            last_name="Jane",
            number_of_pets=0)

        self.assertEqual(History.objects.count(), 0)

    @override_settings(
        INSTALLED_APPS=[
            'django.contrib.contenttypes',
            'history',
            'history.tests'
        ],
        HISTORY_MODELS=['tests.Person'])
    def test_person_history_present(self):
        call_command('migrate', 'tests')
        register_models()

        self.person = Person.objects.create(
            first_name="Bob",
            last_name="Jane",
            number_of_pets=0)

        self.assertEqual(History.objects.count(), 1)

        history = History.objects.previous(self.person)

        for field in self.person._meta.get_fields():
            if not field.primary_key and not isinstance(field, GenericRelation):
                fields = history.serialized_data['fields']
                self.assertIn(field.name, fields)

        # Changes is empty for "create"
        self.assertEqual(history.changes(), [])

        self.person.first_name = "Jane"
        self.person.last_name = "Bob"
        self.person.save()

        history = History.objects.previous(self.person)

        changes = dict(history.changes())
        self.assertIn('modified', changes)
        del changes['modified']

        self.assertEqual(changes, {
            'first_name': ['Jane', 'Bob'],
            'last_name': ['Bob', 'Jane']
        })
        self.assertEqual(History.objects.count(), 2)

        # Calling Manager or QuerySet update method does not trigger the
        # post_save event, therefore no addition to history is expected
        Person.objects.update(first_name="Bob")
        self.assertEqual(History.objects.count(), 2)
