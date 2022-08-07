-include .env
export

lint:
	@flake8 service
	@mypy service

run:
	@python -m service
