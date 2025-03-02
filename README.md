# Talent Vault

## Overview

Talent Vault is a web application that allows you to manage your candidates and jobs.

## Features

- Creates candidates
- List candidates
- Download resumes
- Search candidates
- Filter candidates
- Sort candidates

## Technologies

- Python
- Django
- Django Rest Framework
- PostgreSQL
- Docker
- React
- Tailwind CSS

## Setup

1. Clone the repository
2. Run `make build` to build and run the application using Docker Compose, including database migrations
4. (Optional) Run `make test-backend` to run the test suite for the backend application


# Makefile Commands
```shell
    make build # Builds and runs the application using Docker Compose, including database migrations
    
    make run # Runs the application containers without rebuilding
    
    make run-backend # Runs only the backend container without rebuilding
    
    make run-db # Runs only the database container without rebuilding
    
    make stop # Stops all running containers
    
    make clean # Stops containers and removes associated volumes
    
    make backend-terminal # Opens an interactive terminal in the backend container
    
    make db-terminal # Opens an interactive terminal in the database container
    
    make test-backend # Runs the test suite for the backend application
```