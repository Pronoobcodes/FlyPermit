# FlyPermit — Visa Checklist Platform

[FlyPermit](https://vercel.app) is a modern, responsive web application designed to simplify the visa application process. It provides users with dynamically generated, step-by-step document checklists tailored to specific destinations and visa types. By utilizing secure, stateless authentication and an intuitive dashboard, users can easily track their application progress and ensure they never miss a critical requirement.

---

## 🛠 Tech Stack

**Backend (REST API):**
- **Framework:** Django 5.x & Django REST Framework (DRF)
- **Database:** SQLite (default for development)
- **Authentication:** SimpleJWT (JSON Web Tokens) with rotating refresh tokens and token blacklisting
- **API Documentation:** drf-spectacular (Swagger UI / ReDoc)

**Frontend (Web Application):**
- **Framework:** Next.js 15 (App Router)
- **Deployment & Hosting:** Live on [Vercel](https://vercel.app)
- **Styling:** Tailwind CSS (Vanilla CSS variables for robust theming)
- **State Management:** Zustand
- **HTTP Client:** Axios
- **Icons:** Lucide React

---

## ✨ Key Features

- **Secure Authentication:** Utilizes a secure Next.js API route proxy to handle JWTs via `httpOnly` cookies, preventing client-side XSS vulnerabilities.
- **Dynamic Checklists:** Step-by-step visa selection flow (Country -> Visa Type).
- **Progress Tracking:** Interactive dashboards with visual progress bars and real-time completion percentage calculations.
- **Modern UI/UX:** Responsive layouts built from scratch with custom Tailwind CSS components for a premium look and feel.
- **Optimized Backend:** N+1 query eradication via `select_related` / `prefetch_related` and SQL-level annotations for aggregate stats.

---

## 🚀 Getting Started

Follow the steps below to run both the backend and frontend development servers on your local machine, or view the live site on [Vercel](https://vercel.app).

### Prerequisites
- Python 3.10+
- Node.js 18+ & npm (or yarn/pnpm)

---

### 1. Backend Setup
Open a terminal and navigate to the `backend` directory:
```bash
cd backend
```

**Create and activate a virtual environment:**
```bash
python -m venv venv
# On Windows: venv\Scripts\activate
# On macOS/Linux: source venv/bin/activate
```

**Install dependencies:**
```bash
pip install -r requirements.txt
```

**Set up environment variables:**
Create a `.env` file in the `backend` root (next to `manage.py`) with the following:
```env
SECRET_KEY=your_super_secret_django_key_here
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```

**Run migrations and start the server:**
```bash
python manage.py migrate
python manage.py runserver
```
*The backend API will be available at `http://127.0.0`*
*API Swagger Documentation: `http://127.0.0api/schema/swagger-ui/`*

---

### 2. Frontend Setup
Open a new terminal window and navigate to the `frontend` directory:
```bash
cd frontend
```

**Install dependencies:**
```bash
npm install
```

**Run the development server:**
```bash
npm run dev
```
*The local frontend application will be available at `http://localhost:3000/`*
*The production build is deployed at [FlyPermit on Vercel](https://vercel.app)*

---

## 🏗 Architecture Overview

**Authentication Flow:**
To maximize security, the frontend client *never* accesses the JWT tokens directly.

1. When a user logs in via the client, the request is sent to a Next.js server-side route handler (`/api/accounts/login/`).
2. The Next.js handler proxies the request to the Django backend.
3. Django returns the `access` and `refresh` tokens to Next.js.
4. Next.js sets these tokens as secure, `httpOnly` cookies on the user's browser.
5. For all subsequent requests, Axios hits the Next.js proxy (`/api/*`), which intercepts the request, extracts the cookies, attaches the `Bearer` token, and proxies the request to Django. It automatically handles token refresh if an `access_token` is expired.

---

## 📝 License

This project is for demonstration and MVP purposes.

