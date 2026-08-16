.PHONY: install develop test build clean uninstall

install:
	pipx install .

develop:
	python3 -m pip install -e .

test:
	python3 -m pytest -v

build:
	python3 -m build

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.py[co]" -delete
	rm -rf .pytest_cache build dist *.egg-info

uninstall:
	pipx uninstall shellsync
