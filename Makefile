install:
	poetry install

lint:
	poetry run flake8 page_loader/

test:
	poetry run pytest --cov-report=xml --cov=page_loader tests/
