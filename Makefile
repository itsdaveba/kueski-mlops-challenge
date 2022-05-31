SHELL := /bin/bash

.ONESHELL:
venv:
	python3 -m venv venv
	source venv/bin/activate
	python -m pip install --upgrade pip setuptools wheel
	python -m pip install -e .[dev]

.PHONY: style
style:
	black .
	flake8
	isort .