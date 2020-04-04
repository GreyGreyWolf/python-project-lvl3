install:
	poetry install

build:
	poetry build

publish:
	poetry config repositories.dist https://test.pypi.org/legacy/
	poetry publish -r dist -u GreyGreyWolf -p UnderTheDoom15981598

lint:
	poetry run flake8 page_loader/

bump:
	poetry version patch

test:
	poetry run python -m pytest -vv

cov_test_to_xml:
	poetry run pytest --cov=page_loader tests/ --cov-report=xml
