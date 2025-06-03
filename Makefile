server:
	python server.py
worker:
	celery -A worker.celery worker --loglevel=info
beat:
	celery -A worker.celery beat --loglevel=info
precommit:
	poetry run pre-commit run --all-files
