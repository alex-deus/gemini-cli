.PHONY: lint update-isort install

lint:  ## Run pre-commit on all files
	@pre-commit run --all-files

update-isort:  ## Update iSort config at pyproject.toml
	@seed-isort-config

install:  ## Install package and pre-commit hooks
	@pip install poetry
	@poetry install --no-root
	@pre-commit install
