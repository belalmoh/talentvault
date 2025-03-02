.PHONY: build run stop clean run-backend run-db backend-terminal db-terminal test-backend

# Build and run the application
build:
	cd docker && docker-compose --env-file ../.env up --build -d && docker-compose --env-file ../.env exec backend python manage.py makemigrations && docker-compose --env-file ../.env exec backend python manage.py migrate

# Run the application without rebuilding
run:
	cd docker && docker-compose --env-file ../.env up -d

# Run the backend container without rebuilding
run-backend:
	cd docker && docker-compose --env-file ../.env up -d backend

# Run the database container without rebuilding
run-db:
	cd docker && docker-compose --env-file ../.env up -d db

# Stop all containers
stop:
	cd docker && docker-compose --env-file ../.env down

# Clean up docker resources
clean:
	cd docker && docker-compose --env-file ../.env down -v

# Open a terminal in the backend container
backend-terminal:
	cd docker && docker-compose --env-file ../.env exec backend bash

# Open a terminal in the database container
db-terminal:
	cd docker && docker-compose --env-file ../.env exec db bash 

# Run tests in the backend container
test-backend:
	cd docker && docker-compose --env-file ../.env exec backend python manage.py test vault.tests

