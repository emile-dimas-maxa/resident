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
