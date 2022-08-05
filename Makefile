-include .env
export

lint:
	@flake8 service
	@mypy service
