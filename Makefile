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
	make makemigration && make migrate
cru:
	python manage.py createsuperuser --username=admin --email=admin@gmail.com
run-asgi:
	uvicorn config.asgi:application --host 0.0.0.0 --port 1298 --reload
clear:
	find . -path "*/migrations/*.py" -not -name "__init__.py" -delete && find . -path "*/migrations/*.pyc"  -delete
no-db:
	rm -rf db.sqlite3
re-django:
	pip3 uninstall Django -y && pip3 install Django
re-mig:
	make no-db && make clear && make re-django && make mig && make cru && make run
run-wsgi:
	python3 manage.py runserver 0.0.0.0:1298
startapp:
	python manage.py startapp $(name) && mv $(name) apps/$(name)
clear-linux:
	find . -path "*/migrations/*.py" -not -name "__init__.py" -delete && find . -path "*/migrations/*.pyc"  -delete
clear-windows:
	# .py fayllarni o'chiradi (__init__.py dan tashqari)
	Get-ChildItem -Recurse -File -Path "*/migrations/*.py" | Where-Object { $_.Name -ne "__init__.py" } | Remove-Item -Force

	# .pyc fayllarni o'chiradi
	Get-ChildItem -Recurse -File -Path "*/migrations/*.pyc" | Remove-Item -Force
tunnel:
	jprq http 1298 -s platform
collect:
	python manage.py collectstatic --noinput