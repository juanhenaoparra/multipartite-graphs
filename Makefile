# Variables
DASHBOARD_FOLDER := dashboard
BACKEND_FOLDER := backend
VENV_NAME := venv
PYTHON := python3
PIP := $(VENV_NAME)/bin/pip
NPM := npm

# Default target
all: venv install

# Create virtual environment
venv:
	cd $(BACKEND_FOLDER) && $(PYTHON) -m venv $(VENV_NAME)

# Install dependencies
install: venv
	cd $(BACKEND_FOLDER) && $(PIP) install -r requirements.txt
	touch $(BACKEND_FOLDER)/app/config/.env
	$(MAKE) npm-install

npm-install:
	cd $(DASHBOARD_FOLDER) && $(NPM) install

run-frontend:
	cd $(DASHBOARD_FOLDER) && $(NPM) run dev

run-backend:
	cd $(BACKEND_FOLDER) && $(VENV_NAME)/bin/python main.py

# Clean up
clean:
	rm -rf $(BACKEND_FOLDER)/$(VENV_NAME)
	rm -rf $(DASHBOARD_FOLDER)/node_modules
