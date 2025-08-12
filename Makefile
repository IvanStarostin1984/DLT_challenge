VENV?=.venv
PYTHON=$(VENV)/bin/python
# extra flags for pytest, e.g. make test PYTEST_ARGS="--offline"
PYTEST_ARGS?=$(ARGS)

.PHONY: lint lint-markdown test

lint: lint-markdown
	$(VENV)/bin/pre-commit run --all-files

lint-markdown:
	npx --yes markdownlint-cli '**/*.md'

test:
	$(VENV)/bin/pytest $(PYTEST_ARGS)
