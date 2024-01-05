SHELL = /bin/bash
env = source venv/bin/activate

python = venv/bin/python
manage := $(python) manage.py

activate:
	source venv/bin/activate

migrate:
	$(manage) makemigrations && $(manage) migrate

run:
	$(manage) runserver 0:8005

superuser:
	$(manage) createsuperuser

check:
	$(manage) check

migrations:
	$(manage) makemigrations

celery:
	$(env) && celery -A celery_conf worker

test:
	$(manage) test

shell:
	$(manage) shell

app:
	django-admin start app $app_name
