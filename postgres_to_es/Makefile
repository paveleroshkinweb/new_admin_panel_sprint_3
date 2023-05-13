SHELL := /bin/bash

.PHONY: all build dev lint mypy

all:
	# intentionally left empty to prevent accidental run of first recipe

build:
	docker-compose -f docker-compose.dev.yaml build --no-cache

dev:
	docker-compose -f docker-compose.dev.yaml up

lint:
	python3 -m flake8 --config=$(PWD)/tools/.flake8 src

mypy:
	python3 -m mypy src
