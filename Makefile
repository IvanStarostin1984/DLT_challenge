VENV?=.venv
PYTHON=$(VENV)/bin/python

.PHONY: lint lint-python lint-markdown test

lint: lint-python lint-markdown

lint-python:
	$(VENV)/bin/black .
	$(VENV)/bin/ruff check .

lint-markdown:
	npx --yes markdownlint-cli '**/*.md'

test:
	$(VENV)/bin/pytest
