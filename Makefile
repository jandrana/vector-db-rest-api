DOCKER_COMPOSE := $(shell python -c "import subprocess; print('docker compose' if subprocess.call(['docker', 'compose', 'version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0 else 'docker-compose')")

.PHONY: help setup install run up up-api down clean

help:
	@echo "======================================================================"
	@echo "                       VECTOR SEARCH API + N8N"
	@echo "======================================================================"
	@echo "              Detected Docker Command: $(DOCKER_COMPOSE)"
	@echo "======================================================================"
	@echo " SETUP:"
	@echo "   make setup   : Create .env and vector_db.jsonl files"
	@echo " LOCAL DEV (API ONLY):"
	@echo "   make install   : Install Python dependencies locally"
	@echo "   make run       : Run API locally (http://localhost:8000)"
	@echo " "
	@echo " DOCKER COMPOSE (API + N8N):"
	@echo "   make up        : Build and run API + N8N"
	@echo "   make up-api    : Build and run API (without n8n)"
	@echo "   make down      : Stop all containers"
	@echo "   make clean     : Stop container, delete container, delete image"
	@echo "======================================================================"

setup:
	@python -c "import os; f='vector_db.jsonl'; (not os.path.exists(f)) and [open(f, 'a').close(), print(f + ' file created.')]"
	@python -c "import os; import shutil; f='.env'; (not os.path.exists(f)) and [shutil.copy('.env.example', f), print(f + ' file created. Please configure the API keys.')]"
	@echo "Setup complete."

install:
	pip install --no-cache-dir --upgrade -r requirements.txt
	@echo "Dependencies installed"

run:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
	@echo "Application running on http://localhost:8000"

up: setup
	@echo "Starting API and n8n..."
	$(DOCKER_COMPOSE) up -d --build
	@echo "======================================================"
	@echo "API available at http://localhost:8000/docs"
	@echo "n8n available at http://localhost:5678"
	@echo "======================================================"

up-api: setup
	@echo "Starting API (without n8n)..."
	$(DOCKER_COMPOSE) up -d --build api
	@echo "======================================================"
	@echo "API available at http://localhost:8000/docs"
	@echo "n8n is disabled"
	@echo "======================================================"

down:
	$(DOCKER_COMPOSE) down
	@echo "Services stopped"

clean:
	@echo "Cleaning up Docker environment..."
	$(DOCKER_COMPOSE) down -v --rmi all --remove-orphans
