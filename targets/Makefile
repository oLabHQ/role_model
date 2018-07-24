# This Makefile is designed to speed up initial project development.
# It ought to be replaced by something more suitable for a team as the project
# setup is complete.

path = ../src/server
activate = source ../venv/bin/activate
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

.PHONY: run open test lint shell psql dropdb

all: \
		makemigrations \
		superuser \
		test_data \
		lint \
		run

reset: \
		clean_db \
		deletemigrations \
		clean_migrations \
		makemigrations \
		superuser \
		test \
		test_data

clean_migrations:
		-rm makemigrations
		-rm migrate

clean_db: dropdb
		-rm createdb

clean_venv:
		rm -rf ../venv
		rm venv requirements install

clean: clean_venv clean_db
		-rm makemigrations
		-rm migrate
		rm superuser test_data

run: test_data
		$(manage) runserver

open:
		open http://localhost:8000/admin/login/

test: install
		$(manage) test common role_model crm history.tests

lint:
		$(activate) && flake8 $(path)

shell: install
		$(manage) shell_plus

psql:
		psql -d $(database_name)

venv:
		pyvenv-3.7 ../venv
		touch venv

requirements: venv
		$(activate) && pip install -r ../src/server/requirements.txt
		touch requirements

migrate: makemigrations
		$(manage) migrate
		touch migrate

deletemigrations:
		rm -rf ../src/server/*/migrations/

makemigrations: createdb requirements
		$(manage) makemigrations common crm history role_model server
		touch makemigrations

install: createdb migrate
		touch install

dropdb:
		-echo 'DROP DATABASE $(database_name); ' | psql

createdb:
		echo 'CREATE DATABASE $(database_name);' | psql
		touch createdb

superuser: install
		$(manage) shell -c $(python_create_superuser)
		touch superuser

test_data: install createdb migrate superuser
		$(manage) test_data_role_model
		touch test_data
