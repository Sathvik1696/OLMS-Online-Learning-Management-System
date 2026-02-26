```markdown
# 🏫 OLMS — Online Learning Management System

**OLMS** is a full-stack Online Learning Management System built using **Django (REST API)** for the backend and **pure HTML, CSS & JavaScript** for the frontend.  
It supports user authentication (register, login, profile), JWT authentication, and RESTful API integration.

---

## 🚀 Features

### 🔐 Authentication
- User Registration
- JWT Login & Token Authentication
- View Profile

### 📡 API-First Architecture
- Django REST Framework (DRF)
- Clean API Endpoints

### 🧠 Frontend
- Pure HTML, CSS, and Vanilla JavaScript
- Responsive, smooth user experience
- Calls backend APIs via `fetch()`

---

## 🗂️ Project Structure

---

OLMS-Online-Learning-Management-System/
│
├── accounts/                # Auth app
│   ├── static/accounts/     # Frontend static files
│   │   ├── index.html       # UI entry point
│   │   ├── style.css        # Styles
│   │   └── app.js           # JS logic
│   ├── migrations/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── serializer.py
│
├── courses/                 # Courses app
├── enrollments/             # Enrollment app
├── reviews/                 # Reviews module
├── dashboard/               # Admin dashboard
│
├── olms/                    # Main project
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── .gitignore
├── requirements.txt
└── manage.py

---

---

## 🔗 API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/auth/register/` | POST | Create new user |
| `/api/auth/login/` | POST | Login (JWT Token) |
| `/api/auth/refresh/` | POST | Refresh JWT Token |
| `/api/auth/profile/` | GET | Get current user profile |

📍 The backend uses **JWT authentication** via DRF.

---

## 💻 Backend Tech

- Python 3.x
- Django 6.x
- Django REST Framework
- PostgreSQL

---

## 🧪 Frontend

The frontend is located in:

```

accounts/static/accounts/

````

It contains:

| File | Description |
|------|-------------|
| `index.html` | UI entry page |
| `style.css` | Basic styling |
| `app.js` | JavaScript logic to call API |

---

## ⚙️ Setup (Local)

### Backend

1. Clone the repo

```bash
git clone https://github.com/Sathvik1696/OLMS-Online-Learning-Management-System.git
cd OLMS-Online-Learning-Management-System
````

2. Create Python virtual environment

```bash
python -m venv venv
source venv/bin/activate      # Linux/macOS
venv\Scripts\activate         # Windows
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Setup database

Update `.env` or `settings.py` for PostgreSQL credentials.

5. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

6. Start server

```bash
python manage.py runserver
```

---

### Frontend

1. After backend is running → open in browser:

```
http://127.0.0.1:8000/static/accounts/index.html
```

2. The app will call your backend API automatically.

⚠️ Make sure **CORS is enabled** if you are accessing frontend from a different origin:

Add in `settings.py`:

```python
INSTALLED_APPS += [
    "corsheaders",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    ...
]

CORS_ALLOW_ALL_ORIGINS = True
```

---

## 🧠 Notes

✔   Uses JWT tokens for secure authentication
✔   Pure frontend (no React/Vue) for simplicity
✔   Modular Django apps
✔   Easy to extend (courses, reviews, dashboard)

---

## 🛡 Security

Before pushing production code:

* Move all sensitive credentials to `.env`
* Add `.env` to `.gitignore`
* DO NOT push secret keys to public repo

Example in `.env`:

```
SECRET_KEY=supersecret
DB_NAME=olms
DB_USER=postgres
DB_PASSWORD=yourpass
```

---

## 🎯 Next Steps (Possible Enhancements)

✔ Role-based access (student/admin)
✔ Token auto-refresh
✔ Pagination for lists
✔ Courses CRUD
✔ Dashboard UI improvements
✔ Email verification

---

## 🧑‍💻 Author

**Sathvik** – Fullstack Django Developer
📍 India

---

## ⭐ If You Found This Useful

Give the repository a ⭐️!
Share with your friends and fellow developers 🙂

```
