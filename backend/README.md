# Visa Checklist

A Django REST API for tracking visa requirements, document checklists, and travel readiness for international destinations. This project is built with a focus on Nigerian travellers who need clear visa guidance and organized document tracking.

## Overview

Visa Checklist stores country-specific visa types, document requirements, and user-managed checklists. It exposes a REST API for both public visa data browsing and authenticated checklist management.

## Key Features

- Country and visa type catalog
- Document requirement records for each visa
- JWT-based user registration and login
- Personal visa checklist creation and tracking
- API documentation via Swagger and Redoc
- Data seeding command for visa data population

## Project Structure

- `config/` — Django settings, URL routing, ASGI/WGI entrypoints
- `apps/accounts/` — authentication, registration, JWT login/logout
- `apps/visas/` — models and API for countries, visa types, and documents
- `apps/checklists/` — user checklists, checklist items, and permissions
- `apps/visas/management/commands/populate_visas.py` — seed command
- `pyproject.toml` — dependency definitions

## Requirements

- Python 3.12+
- PostgreSQL or other supported Django database
- `uv` dependency manager
- Virtual environment (`.venv` recommended)

## Setup

### 1. Activate the virtual environment

```powershell
cd c:\Users\Administrator\Documents\visa_checklist
.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
.venv\Scripts\python.exe -m pip install --upgrade pip uv
.venv\Scripts\python.exe -m uv sync
```

### 3. Configure environment variables

Create a `.env` file in the project root with your database settings. Example:

```env
DB_NAME=visa_checklist
DB_USER=postgres
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=5432
```

### 4. Run database migrations

```powershell
.venv\Scripts\python.exe manage.py migrate
```

### 5. Populate visa data

```powershell
.venv\Scripts\python.exe manage.py populate_visas
```

### 6. Start the development server

```powershell
.venv\Scripts\python.exe -m uv run uvicorn config.asgi:application --reload
```

## API Endpoints

### Authentication

- `POST /api/accounts/register/`
- `POST /api/accounts/login/`
- `POST /api/accounts/logout/`
- `POST /api/token/`
- `POST /api/token/refresh/`

### Visa Catalog

- `GET /api/visas/countries/`
- `GET /api/visas/countries/{id}/`
- `GET /api/visas/visas/`
- `GET /api/visas/visas/{id}/`
- `GET /api/visas/documents/`
- `GET /api/visas/documents/{id}/`

### Checklist Management

- `GET /api/checklists/user-checklists/`
- `POST /api/checklists/user-checklists/`
- `GET /api/checklists/user-checklists/{id}/`
- `PATCH /api/checklists/user-checklists/{id}/`
- `DELETE /api/checklists/user-checklists/{id}/`
- `GET /api/checklists/checklist-items/`
- `PATCH /api/checklists/checklist-items/{id}/`

### Documentation

- `GET /api/schema/`
- `GET /api/schema/swagger-ui/`
- `GET /api/schema/redoc/`

## Seed Data

The command `manage.py populate_visas` loads visa country, visa type, and document requirement data into the database. This command was tested successfully and is designed to be rerun safely after migrations.

## Notes

- Anonymous users can view visa catalog data.
- Checklist creation and editing require JWT authentication.
- Always run `manage.py migrate` before populating data.
- `uv` manages Python dependencies and also runs the development server in this project.

## Will the code work as expected?

Yes. The project runs correctly with a proper virtual environment, database configuration, and migrations applied. The `populate_visas` command has been tested and populates the database successfully.

## License

This repository is provided as-is for development and learning purposes.
