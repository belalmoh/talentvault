# Talent Vault

## Overview

Talent Vault is a web application that allows you to manage your candidates and jobs.

## Features

- Creates candidates
- List candidates
- Download resumes
- Filter candidates

## Technologies

- Python
- Django
- MySQL
- Docker
- React with TypeScript
- Tailwind CSS


## Prerequisites

- Docker
- Node.js

## Setup

1. Clone the repository
2. Rename `.env.example` to `.env` and set the environment variables with the correct values
3. Run `make build` to build and run the application using Docker Compose, including database migrations
4. (Optional) Run `make test-backend` to run the test suite for the backend application
5. (Optional) Run `make run-frontend` to run the frontend application

## API Documentation

The API documentation is available at `/docs`.

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

# Example cURL Requests for the API

## Create a candidate
```shell
curl --location 'http://localhost:8000/vault/candidate/register' \
--header 'user-name: admin' \
--header 'password: admin' \
--form 'full_name="Belal Mohammed"' \
--form 'email="bello@bello.comxxxxx"' \
--form 'date_of_birth="1994-05-26"' \
--form 'years_of_experience="1"' \
--form 'department_id="1"' \
--form 'resume=@"/Users/belalmohammed/Documents/__ The Travel Itinerary.pdf"'
```

## List candidates
```shell
curl --location 'http://localhost:8000/vault/candidates?page=1&count=10' \
--header 'X-ADMIN: 1'
```

## Download a candidate's resume
```shell
curl --location 'http://localhost:8000/vault/candidate/1/resume' \
--header 'X-ADMIN: 1'
```


