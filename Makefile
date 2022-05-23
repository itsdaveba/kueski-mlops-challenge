.PHONY: production
production:
	python -m pip install --upgrade pip setuptools wheel
	python -m pip install .[prod] --no-cache-dir