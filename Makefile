VENV = venv

setup: pyproject.toml
	[ -d $(VENV) ] && rm -rf $(VENV) \
	&& python -m venv $(VENV) \
	&& source $(VENV)/bin/activate \
	&& pip install poetry==1.8.3 \
	&& poetry install --no-root
