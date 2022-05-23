venv:
	python -m venv venv
	venv/scripts/python -m pip install --upgrade pip setuptools wheel
	venv/scripts/python -m pip install -e .[dev]