.PHONY: lint test

lint:
	@npx --yes markdownlint-cli '**/*.md'
	@git diff --check
	@git grep -n '<<<<<<<\|=======\|>>>>>>>' -- . ':!AGENTS.md' && exit 1 || echo 'No conflict markers'

test:
	@pytest -q || [ $$? -eq 5 ]
