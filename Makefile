# This Makefile is designed to speed up initial project development.
# It ought to be replaced by something more suitable for a team as the project
# setup is complete.

path = src/server
activate = source venv/bin/activate
cd = cd $(path)
manage = $(activate) && $(cd) && python manage.py
database_name = role_model

define python_create_superuser
"from crm.models import User; \
User.objects.create_superuser(\
	username='eric@dataapi.blog',\
	password='a',\
	first_name='Eric',\
	last_name='Man')"
endef
export python_create_superuser

run:
		$(manage) runserver

open:
		open http://localhost:8000/admin/login/

test:
		$(manage) test common role_model crm history.tests

lint:
		$(activate) && flake8 $(path)

shell:
		$(manage) shell_plus

psql:
		psql -d $(database_name)

venv:
		pyvenv-3.7 venv

requirements: venv
		$(activate) && pip install -r src/server/requirements.txt

migrate:
		$(manage) migrate

makemigrations:
		$(manage) makemigrations

install: requirements reset makemigrations migrate

reset:
		echo 'DROP DATABASE $(database_name); CREATE DATABASE $(database_name);' | psql

superuser:
		$(manage) shell -c $(python_create_superuser)


test_data: reset migrate superuser
		$(manage) test_data_role_model

recreate: test_data run
