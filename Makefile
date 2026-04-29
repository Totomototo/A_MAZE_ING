PYTHON_SYS = python3
VENV = .venv
CONFIG_FILE = config.txt

install:
	$(PYTHON_SYS) -m venv $(VENV)
	$(VENV)/bin/pip install --upgrade pip setuptools wheel
	$(VENV)/bin/pip install -r requirements.txt
	@echo "  source $(VENV)/bin/activate"

run:
	$(VENV)/bin/python a_maze_ing.py $(CONFIG_FILE)

debug:
	$(VENV)/bin/python -m pdb a_maze_ing.py $(CONFIG_FILE)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .mypy_cache .pytest_cache
	rm -rf build dist *.egg-info src/*.egg-info

lint:
	$(VENV)/bin/flake8 .
	$(VENV)/bin/mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	$(VENV)/bin/flake8 .
	$(VENV)/bin/mypy . --strict

build:
	$(VENV)/bin/python -m build

package-install:
	$(VENV)/bin/pip install dist/mazegen-1.0.0-py3-none-any.whl