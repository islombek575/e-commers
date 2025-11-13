mig:
	python3 manage.py makemigrations
	python3 manage.py migrate

run:
	python3 manage.py runserver

user:
	python3 manage.py createsuperuser


lang:
	django-admin makemessages -l uz -l en

compile:
	django-admin compilemessages -i .venv

loaddata:
	python3 manage.py loaddata users merchant shop categories products productversion productimage like comments


