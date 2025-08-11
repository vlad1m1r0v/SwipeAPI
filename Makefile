server:
	uvicorn server:server --host 0.0.0.0 --port 8000 --workers 4
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
certificates:
	@echo "Deleting old certificates directory (if it exists)..."
	@rm -rf certs
	@echo "Creating certificates directory..."
	@mkdir -p certs
	@echo "Generating private key..."
	@openssl genrsa -out certs/jwt-private.pem 2048
	@echo "Generating public key..."
	@openssl rsa -in certs/jwt-private.pem -pubout -out certs/jwt-public.pem
	@echo "Certificates created successfully in the 'certs' directory."
