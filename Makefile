init-env:
	python3 -m venv env
act-env:
	. env/bin/activate
i:
	pip install --upgrade pip && pip install -r requirements.txt
migration:
	python3 manage.py makemigrations
migrate:
	python3 manage.py migrate
mig:
	make migration && make migrate
cru:
	python3 manage.py createsuperuser --username=dalikuziev --email=dalikuziev@gmail.com
run-asgi:
	uvicorn config.asgi:application --host 0.0.0.0 --port 8000 --reload
clear:
	find . -path "*/migrations/*.py" -not -name "__init__.py" -delete && find . -path "*/migrations/*.pyc"  -delete
no-db:
	rm -rf db.sqlite3
re-django:
	pip3 uninstall Django -y && pip3 install Django
re-mig:
	make no-db && make clear && make re-django && make mig && make cru && make run-asgi
run-wsgi:
	python3 manage.py runserver 0.0.0.0:8000
startapp:
	python3 manage.py startapp $(name) && mv $(name) apps/$(name)
clear-linux:
	find . -path "*/migrations/*.py" -not -name "__init__.py" -delete && find . -path "*/migrations/*.pyc"  -delete
clear-windows:
	Get-ChildItem -Path "*\migrations\0*.py" | Remove-Item -Force
	Get-ChildItem -Path "*\migrations\*.pyc" | Remove-Item -Force
tunnel:
	jprq http 7 -s platform
collect:
	python3 manage.py collectstatic --noinput
open-bash:
	docker exec -it drf_api bash
