.PHONY: up down logs migrate shell-api shell-web test-api lint

up:
	docker compose up -d --build

down:
	docker compose down

logs:
	docker compose logs -f

migrate:
	docker compose exec api alembic upgrade head

shell-api:
	docker compose exec api bash

shell-web:
	docker compose exec web sh

test-api:
	cd apps/api && pytest

lint:
	pnpm lint
