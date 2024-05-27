VENV = venv

setup: pyproject.toml
	[ -d $(VENV) ] && rm -rf $(VENV) \
	[ -d "poetry.lock" ] && rm -rf "poetry.lock" \
	&& python -m venv $(VENV) \
	&& source $(VENV)/bin/activate \
	&& pip install poetry==1.8.3 \
	&& poetry install --no-root

test: $(VENV)/bin/activate
	$(VENV)/bin/pytest


setup-db: docker/psql-dev-docker-compose
	docker-compose -f docker/psql-dev-docker-compose up -d


alembic-commit:
# get input message:
	@read -p "Enter commit message: " message;
	$(VENV)/bin/alembic revision --autogenerate -m "$$message"

alembic-push:
	$(VENV)/bin/alembic upgrade head
