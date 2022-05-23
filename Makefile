venv:
	python -m venv venv
	source venv/bin/activate
	python -m pip install --upgrade pip setuptools wheel
	python -m pip install -e .[dev]