IMAGE = vector-search-api
CONTAINER = vector-db-container

.PHONY: help install run build up stop clean

help:
	@echo "======================================================================"
	@echo "   VECTOR SEARCH API - COMMANDS"
	@echo "======================================================================"
	@echo "LOCAL DEV:"
	@echo "  make install   : Install Python dependencies"
	@echo "  make run       : Run the app locally (http://localhost:8000)"
	@echo ""
	@echo "DOCKER:"
	@echo "  make build     : Build the Docker image"
	@echo "  make up        : Run the container with persistence"
	@echo "  make stop      : Stop the running container"
	@echo "  make clean     : Stop container, delete container, delete image"
	@echo "======================================================================"

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
	@echo "Ensuring database file exists for persistence"
	@python -c "import os; open('vector_db.jsonl', 'a').close()"
	@echo "Starting Docker container..."
	docker run -p 8000:8000 -v "$(CURDIR)/vector_db.jsonl:/app/vector_db.jsonl" --env-file .env --name $(CONTAINER) $(IMAGE)
	@echo "You can access the API at http://localhost:8000/docs"

stop:
	docker stop $(CONTAINER)
	@echo "Docker container stopped"

clean:
	@echo "Cleaning up Docker environment..."
	docker stop $(CONTAINER)
	docker rm $(CONTAINER)
	docker rmi $(IMAGE)
	@echo "Cleaned up Docker environment (Image && Container removed)"
