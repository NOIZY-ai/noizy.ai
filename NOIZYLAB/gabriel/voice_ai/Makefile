# 🛠️ GABRIEL MAKEFILE - 100% PERFECT
# GORUNFREE Protocol

.PHONY: help install test lint format clean docker-build docker-up docker-down migrate

help:
	@echo "GABRIEL - Available commands:"
	@echo "  make install      - Install dependencies"
	@echo "  make test         - Run tests"
	@echo "  make lint         - Run linters"
	@echo "  make format       - Format code"
	@echo "  make clean         - Clean cache and temp files"
	@echo "  make docker-build - Build Docker images"
	@echo "  make docker-up    - Start Docker services"
	@echo "  make docker-down  - Stop Docker services"
	@echo "  make migrate      - Run database migrations"

install:
	pip install -r infrastructure/requirements.txt
	pre-commit install

test:
	pytest --cov=. --cov-report=html --cov-report=term -v

lint:
	black --check .
	isort --check .
	pylint .
	mypy .
	ruff check .

format:
	black .
	isort .
	ruff check --fix .

clean:
	find . -type d -name __pycache__ -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -r {} +
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov
	rm -rf dist
	rm -rf build

docker-build:
	docker-compose build

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

migrate:
	alembic upgrade head

migrate-create:
	alembic revision --autogenerate -m "$(MESSAGE)"

run-api:
	uvicorn api.voice_ai_api_server_perfect:app --host 0.0.0.0 --port 8000 --reload

run-worker:
	celery -A infrastructure.queue.celery_tasks worker --loglevel=info

run-all: docker-up migrate run-api

