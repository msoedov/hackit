build:
	docker-compose build

up: build
	docker-compose up -d
	docker attach apimozillascienceorg_web_1

test: build
	docker-compose run web sh -c "python /app/manage.py test"

migrate: build
	docker-compose run web python manage.py migrate

shell: build
	docker-compose run web python manage.py shell

cpenv:
	cp env.sample .env

createsuperuser:
	docker-compose run web python manage.py createsuperuser

cmigrate: build
	docker-compose run web ./manage.py makemigrations

clean:
	@echo "Cleaning *.pyc files and __pycache__ folders"
	@$(find . -name "*.pyc" -exec rm -f {} \; &>/dev/null)
	@$(find . -type d -name "__pycache__" -exec rm -rf {} \; &>/dev/null)
