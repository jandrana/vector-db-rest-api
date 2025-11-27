IMAGE = vector-search-api
CONTAINER = vector-db-container

.PHONY: help install run build up stop clean

help:
	@echo "Build locally:"
	@echo "1. make install:	Install dependencies"
	@echo "2. make run:		Run the application locally"
	@echo "		Access: 	http://localhost:8000"
	@echo "Build and run with Docker"
	@echo "1. make build:	Build the Docker image"
	@echo "2. make up:		Run the Docker container"
	@echo "		Access: 	http://localhost:8000"
	@echo "6. make stop:	Stop the Docker container"
	@echo "7. make clean:	Clean up the project"

install:
	pip install --no-cache-dir --upgrade -r requirements.txt
	@echo "Dependencies installed"

run:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
	@echo "Application running on http://localhost:8000"

build:
	docker build -t $(IMAGE) .
	@echo "Docker image built."

up:
	docker run --rm -p 8000:8000 --env-file .env --name $(CONTAINER) $(IMAGE)
	@echo "Docker container running on http://localhost:8000"

stop:
	docker stop $(CONTAINER)
	@echo "Docker container stopped"

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	@echo "Cache cleaned"
