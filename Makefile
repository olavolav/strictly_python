.PHONY: test publish clean help format unit_test # linter type_check

test: format unit_test # linter type_check visual_check

help:
	@echo "Available commands:"
	@echo "test publish clean help format unit_test"

format:
	@echo "\n### Formatting"
	uv run ruff format

# linter:
#         @echo "##########"
#         @echo "# Linter #"
#         @echo "##########"
#         uv run ruff check
#         @echo

# type_check:
#         @echo "##############"
#         @echo "# Type check #"
#         @echo "##############"
#         uv run mypy --namespace-packages uniplot/**/*.py tests/**/*.py
#         @echo

unit_test:
	@echo "\n### Unit tests"
	uv run python3 -m pytest tests/

dist/:
	@echo "\n### Building"
	uv build

publish: clean dist/
	@echo "\n### Publishing"
	uv publish

clean:
	@echo "\n### Cleanup"
	rm -rf dist/%