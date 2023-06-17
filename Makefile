lint:
	poetry run flake8 net_operations --show-source
venv:
	poetry shell
test:
	poetry run pytest -v
install:
	poetry install

