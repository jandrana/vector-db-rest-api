DOCKER_COMPOSE := $(shell python -c "import subprocess; print('docker compose' if subprocess.call(['docker', 'compose', 'version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0 else 'docker-compose')")

.PHONY: help setup install run up up-api down clean venv install-dev test update-deps

help:
	@echo "======================================================================"
	@echo "                       VECTOR SEARCH API + N8N"
	@echo "======================================================================"
	@echo "              Detected Docker Command: $(DOCKER_COMPOSE)"
	@echo "======================================================================"
	@echo " SETUP:"
	@echo "   make setup   : Create .env and vector_db.jsonl files"
	@echo " LOCAL DEV (API ONLY):"
	@echo "   make venv      : Create a Python virtual environment in .venv"
	@echo "   make install   : Install Python dependencies locally"
	@echo "   make install-dev : Install dev dependencies (uses .venv if available)"
	@echo "   make run       : Run API locally (http://localhost:8000)"
	@echo "   make test      : Run tests using pytest (uses .venv if available)"
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
	python -m pip install --no-cache-dir -r requirements.txt
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

venv:
	@python -m venv .venv
	@echo "Virtual environment created at .venv"
	@echo "Activate it using:"
	@echo "  Windows PowerShell: .\\.venv\Scripts\Activate.ps1"
	@echo "  Windows Bash: source .venv/Scripts/activate"
	@echo "  Linux/Mac: source .venv/bin/activate"
	@echo "Run 'make install-dev' to install dev dependencies."

install-dev:
	@echo "Installing dev dependencies..."
	@if [ -f .venv/Scripts/python.exe ]; then \
		.venv/Scripts/python.exe -m pip install --upgrade pip && .venv/Scripts/python.exe -m pip install -r requirements-dev.txt; \
	elif [ -f .venv/bin/python ]; then \
		.venv/bin/python -m pip install --upgrade pip && .venv/bin/python -m pip install -r requirements-dev.txt; \
	else \
		python -m pip install -r requirements-dev.txt; fi
	@pre-commit install -t pre-push || true
	@echo "Dev dependencies installed"

test:
	@echo "Running tests..."
	@if [ -f .venv/Scripts/python.exe ]; then \
		.venv/Scripts/python.exe -m pytest; \
	elif [ -f .venv/bin/python ]; then \
		.venv/bin/python -m pytest; \
	else \
		python -m pytest; fi
	@echo "Tests completed"

update-deps:
	@echo "Upgrading dev dependencies (use intentionally)..."
	@python -m pip install --no-cache-dir --upgrade -r requirements-dev.txt
	@echo "Dev dependencies upgraded"
