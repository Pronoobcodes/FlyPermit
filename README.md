# Visa Checklist

A Django REST API for tracking visa requirements and document checklists for international travel, with a focus on the unique challenges faced by Nigerian travelers.

## Project Purpose

Many Nigerians face complex visa rules, inconsistent embassy requirements, and a lack of centralized guidance when planning international travel. This project captures visa categories, country-specific documentation, and user-managed checklists so travelers can prepare, stay organized, and reduce application delays.

## What this project does

- Stores visa categories for countries and travel purposes.
- Stores document requirements for each visa type.
- Provides authenticated user accounts with JWT login and registration.
- Creates user-specific visa checklists so travelers can track documents they already have and those still needed.
- Exposes API schema documentation via Swagger and Redoc.

## Why it helps Nigerian travelers

Traveling from Nigeria often means navigating:

- multiple embassy requirements that change frequently
- unclear supporting document expectations
- long visa processing windows and expensive application fees
- difficulty tracking progress through document collection and submission

This project provides a digital checklist and visa-type catalog so travelers can make preparation more transparent and manageable.

## Key features

- User registration and JWT authentication
- Read-only visa country, visa type, and document requirement APIs
- Personal visa checklists with item tracking
- Convenient documentation endpoints for API exploration
- Designed for easy extension with new countries and visa rule updates

## Project structure

- `config/` - Django project settings, URL routing, ASGI/WGI entrypoints
- `apps/accounts/` - user model, registration/login/logout, serializers, URLs
- `apps/visas/` - country, visa type, and document requirement models and read-only API views
- `apps/checklists/` - user checklists, checklist items, permissions, and service helpers
- `pyproject.toml` / `uv.lock` - dependency management with `uv`

## API endpoints

Authentication:

- `POST /api/accounts/register/` - create a new user
- `POST /api/accounts/login/` - obtain JWT access and refresh tokens
- `POST /api/accounts/logout/` - logout the current user

Visa catalog:

- `GET /api/visas/countries/`
- `GET /api/visas/countries/{id}/`
- `GET /api/visas/visas/`
- `GET /api/visas/visas/{id}/`
- `GET /api/visas/documents/`
- `GET /api/visas/documents/{id}/`

Checklist management:

- `GET /api/checklists/user-checklists/`
- `POST /api/checklists/user-checklists/`
- `GET /api/checklists/user-checklists/{id}/`
- `PATCH /api/checklists/user-checklists/{id}/`
- `DELETE /api/checklists/user-checklists/{id}/`
- `GET /api/checklists/checklist-items/`
- `PATCH /api/checklists/checklist-items/{id}/`

Documentation:

- `GET /api/schema/`
- `GET /api/schema/swagger-ui/`
- `GET /api/schema/redoc/`

## Getting started

1. Clone the repository.
2. Create or activate the project virtual environment.
3. Install and sync dependencies with `uv`.

```powershell
cd c:\Users\Administrator\Documents\visa_checklist
.venv\Scripts\python.exe -m pip install uv
.venv\Scripts\python.exe -m uv sync
```

4. Create a `.env` file with database configuration. Example:

```env
DB_NAME=visa_checklist
DB_USER=postgres
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=5432
```

5. Run Django migrations:

```powershell
.venv\Scripts\python.exe manage.py migrate
```

6. Start the application with Uvicorn:

```powershell
.venv\Scripts\python.exe -m uv run uvicorn config.asgi:application --reload
```

## Authentication notes

Visa catalog endpoints are available to anonymous users so travelers can browse countries, visa types, and document requirements without logging in.

Checklist creation and updates require a valid JWT access token. Include the token in requests with:

```http
Authorization: Bearer <access_token>
```

## Extending the app

- Add new `Country`, `VisaType`, and `DocumentRequirement` records through Django admin or seed scripts.
- Extend the API with write actions if needed.
- Add more checklist fields such as embassy appointment dates, fee tracking, or application status.

## Why this matters

This service is built to support Nigerian travelers by turning scattered visa requirements into one organized digital checklist. The goal is to help reduce uncertainty, prevent missing documents, and make travel preparation easier for people who need clear, reliable guidance.

## License

This repository is provided as-is for development and learning purposes.
