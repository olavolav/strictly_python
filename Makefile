# EXAMPLES := $(wildcard examples/*.py)
.PHONY: test publish clean help format unit_test # linter type_check visual_check $(EXAMPLES) run_all_examples

test: format unit_test # linter type_check visual_check

# help:
#         @echo "Available commands:"
#         @echo "\ttest format linter type_check visual_check unit_test run_all_examples"

format:
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
	uv run python3 -m pytest tests/

dist/:
	uv build

publish: clean dist/
	uv publish

clean:
	rm -rf dist/%