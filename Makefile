server:
	python server.py
worker:
	celery -A worker.celery worker --loglevel=info
beat:
	celery -A worker.celery beat --loglevel=info
precommit:
	poetry run pre-commit run --all-files
migration-create:
ifndef name
	$(error You must provide a migration name, e.g., make migration-create name="add_users_table")
endif
	poetry run alembic revision --autogenerate -m "$(name)"
migration-upgrade:
	poetry run alembic upgrade head
seed:
	python -m cli seed
clear:
	python -m cli clear
