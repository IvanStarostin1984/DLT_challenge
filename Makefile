VENV?=.venv
PYTHON=$(VENV)/bin/python
# extra flags for pytest, e.g. make test PYTEST_ARGS="--offline"
PYTEST_ARGS?=$(ARGS)

.PHONY: lint lint-python lint-markdown test

lint: lint-python lint-markdown

lint-python:
	$(VENV)/bin/pre-commit run --files $(shell git ls-files '*.py')

lint-markdown:
	npx --yes markdownlint-cli '**/*.md'

test:
	$(VENV)/bin/pytest $(PYTEST_ARGS)
