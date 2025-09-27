install:
	poetry install

project:
	poetry run project

build:
	poetry build

publish:
	poetry publish --dry-run

package-install:
	python -m pip install --force-reinstall dist/*.whl

lint:
	poetry run ruff check .

clean:
	rm -rf dist build *.egg-info

.PHONY: install project build publish package-install lint clean