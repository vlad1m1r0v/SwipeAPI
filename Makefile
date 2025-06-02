server:
	python server.py
worker:
	celery -A worker.celery worker --loglevel=info
precommit:
	poetry run pre-commit run --all-files
