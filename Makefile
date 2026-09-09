.PHONY: setup start stop seed reset logs frontend backend

## Copy env and start all services
setup:
	cp -n .env.example .env || true
	docker-compose up -d --build

## Start all services (no build)
start:
	docker-compose up -d

## Stop all services
stop:
	docker-compose down

## Seed the database with historical F1 data
seed:
	docker-compose exec backend python /data/seed_data.py

## Full reset — destroy volumes and reseed
reset:
	docker-compose down -v
	docker-compose up -d --build
	sleep 5
	$(MAKE) seed

## Tail all service logs
logs:
	docker-compose logs -f

## Run only the frontend locally (no Docker)
frontend:
	cd frontend && npm run dev

## Run only the backend locally (no Docker)
backend:
	cd backend && uvicorn main:app --reload --host 0.0.0.0 --port 8000

## Install frontend dependencies
install-frontend:
	cd frontend && npm install

## Install backend dependencies
install-backend:
	cd backend && pip install -r requirements.txt
