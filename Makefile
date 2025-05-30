server:
	python server.py
worker:
	celery -A worker.celery worker --loglevel=info
