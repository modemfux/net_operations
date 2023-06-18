lint:
	poetry run flake8 net_operations --show-source
venv:
	poetry shell
test:
	poetry run pytest -v
install:
	poetry install
test-coverage:
	poetry run pytest --cov=net_operations --cov-report xml
nat_report:
	poetry run nat_report
