
install:
	poetry install

lint:
	poetry run flake8 loader.py
	
test:
	poetry run pytest --cov=page_loader tests/ --cov-report=xml