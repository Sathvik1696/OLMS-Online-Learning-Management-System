# OCMS AI Coding Agent Instructions

## Project Overview

**OLMS** (Online Learning Management System) is a Django REST Framework (DRF) backend API for managing online courses, user enrollments, and reviews. The project uses:
- **Framework**: Django 6.0.2 + Django REST Framework 3.16.1
- **Database**: PostgreSQL (configured in `olms/settings.py`)
- **Auth**: JWT tokens via `djangorestframework-simplejwt` (5.5.1)
- **Python**: Via virtual environment (`env/`)

## Architecture & Key Components

### App Structure (Django Apps)

OLMS follows the standard Django multi-app architecture. Each app has this pattern:
```
<app_name>/
  ├── models.py      # Database models
  ├── views.py       # Class-based API views (use generics from DRF)
  ├── serializer.py  # DRF serializers (naming differs from convention: uses .py not .s)
  ├── urls.py        # URL routing for the app
  ├── admin.py       # Django admin registration
  ├── apps.py        # App configuration
  ├── tests.py       # Unit tests
  └── migrations/    # Database migrations
```

**Current Apps** (in `settings.py` INSTALLED_APPS):
1. **accounts** - User authentication & profiles (IMPLEMENTED)
2. **courses** - Course management (STUB)
3. **enrollments** - Course enrollments (STUB)
4. **dashboard** - User dashboards (STUB)
5. **reviews** - Course reviews (STUB)

### Custom User Model (accounts app)

The project implements a custom `User` model extending Django's `AbstractUser`:

**Key traits**:
- Email-based authentication (removes `username` field)
- Three roles: STUDENT, INSTRUCTOR, ADMIN (stored in `role` CharField with choices)
- Custom manager: `CustomUserManager` with `create_user()` and `create_superuser()`
- Timestamps: `created_at`, `updated_at` (auto-managed)
- Username field set to `email` (USERNAME_FIELD = 'email')

**Location**: `accounts/models.py` - This is the auth foundation for the entire project.

### Authentication Flow

1. **Register**: POST `/api/auth/register/` → `RegisterView` (CreateAPIView)
   - Serializer: `RegisterSerializer` (takes email, full_name, password, role)
   - Creates user via `User.objects.create_user()` (custom manager hashes password)

2. **Login**: POST `/api/auth/login/` → `TokenObtainPairView` (DRF-simplejwt)
   - Returns access & refresh tokens (JWT)
   - No custom view needed—built into simplejwt

3. **Profile**: GET `/api/auth/profile/` → `ProfileView` (APIView)
   - Requires `IsAuthenticated` permission
   - Returns user data via `UserSerializer` (read-only fields)

**URL routing**: `olms/urls.py` includes `accounts.urls` under `/api/auth/` prefix

### Database Configuration

PostgreSQL is configured in `olms/settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'olms',
        'USER': 'postgres',
        'PASSWORD': 'Sathvik@1696',  # WARNING: Hardcoded—use env vars in production
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

**Note**: Database credentials are hardcoded in settings. Always use environment variables in production.

## Development Workflows

### Running the Server

From the `olms/` directory (where `manage.py` lives):
```bash
python manage.py runserver
```

This starts Django development server (default: http://localhost:8000/)

### Database Migrations

When modifying models:
```bash
# Create migrations from model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Reset everything (caution: destroys data)
python manage.py migrate <app_name> zero
```

**Note**: `accounts` app already has migrations (`migrations/0001_initial.py`). New apps (courses, enrollments, etc.) are stubs—create models first.

### Creating Superuser

```bash
python manage.py createsuperuser
```

Prompts for email, full_name, password. Accesses Django admin at `/admin/`.

### Running Tests

```bash
python manage.py test <app_name>
# or all:
python manage.py test
```

Tests use Django's `TestCase` class. Currently all test files are stubs (`# Create your tests here.`).

## Code Patterns & Conventions

### Views (accounts app as template)

Use **class-based views** from DRF:
- `generics.CreateAPIView` for POST (create) endpoints (e.g., RegisterView)
- `APIView` + `permission_classes` for custom logic (e.g., ProfileView)
- Always inherit from DRF's view classes, not Django's

Example pattern:
```python
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
```

### Serializers (accounts/serializer.py)

Naming convention: `serializer.py` (not `serializers.py`).

Patterns:
- Write-only fields (like password): `extra_kwargs = {'password': {'write_only': True}}`
- Override `create()` method to handle custom logic (e.g., hashing passwords)
- Read-only serializers: list only safe fields in `fields`

```python
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'full_name', 'password', 'role']
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
```

### URL Routing

- Main URLs: `olms/urls.py` (project-level)
- App URLs: `<app_name>/urls.py` (app-level)
- Include app URLs in main via `path('api/auth/', include('accounts.urls'))`
- Use meaningful prefixes: `/api/auth/` for accounts, future: `/api/courses/`, etc.

Example (`accounts/urls.py`):
```python
from django.urls import path
from .views import RegisterView, ProfileView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', TokenObtainPairView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
    path('profile/', ProfileView.as_view()),
]
```

### Models

Patterns from `User` model:
- Always include `created_at = DateTimeField(auto_now_add=True)` and `updated_at = DateTimeField(auto_now=True)` for audit trails
- Use `choices` for enum-like fields (e.g., role)
- Define `__str__()` for readable admin/shell output
- For ForeignKey/ManyToMany, use related_name for reverse queries

## Critical Integration Points

### JWT Authentication (simplejwt)

Endpoints are secured with JWT. Clients must:
1. POST to `/api/auth/login/` with email & password → get access token
2. Include header: `Authorization: Bearer <access_token>` in subsequent requests
3. Use `/api/auth/refresh/` to refresh expired tokens (send refresh_token)

`ProfileView` demonstrates the pattern: `permission_classes = [permissions.IsAuthenticated]`

### Multi-Role System

The `User.role` field has three choices: STUDENT, INSTRUCTOR, ADMIN. This is the basis for future permission checks.

When adding views that require role-based access, use custom permissions:
```python
from rest_framework.permissions import BasePermission

class IsInstructor(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'INSTRUCTOR'
```

Then apply: `permission_classes = [permissions.IsAuthenticated, IsInstructor]`

## Common Workflows for AI Agents

### Adding a New API Endpoint

1. Define the model in `<app>/models.py`
2. Create migrations: `python manage.py makemigrations <app>`
3. Define serializer in `<app>/serializer.py`
4. Create view in `<app>/views.py` (use DRF generics)
5. Add URL route in `<app>/urls.py`
6. Include in `olms/urls.py` if needed
7. Test with: `python manage.py test <app>`

### Adding a Relationship Between Models

Example: Course → Enrollment → User

Models need ForeignKey or ManyToMany:
```python
# In courses/models.py
class Course(models.Model):
    title = models.CharField(max_length=255)
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='taught_courses')

# In enrollments/models.py
class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
```

Then run `makemigrations` and `migrate`.

### Testing Models & Serializers

Use `django.test.TestCase` (inherits from unittest.TestCase + database rollback):
```python
from django.test import TestCase
from .models import Course
from .serializer import CourseSerializer

class CourseTestCase(TestCase):
    def setUp(self):
        self.course = Course.objects.create(title='Python 101')
    
    def test_course_creation(self):
        self.assertEqual(self.course.title, 'Python 101')
```

## Dependencies & Virtual Environment

The project uses a local virtual environment (`env/`). Installed packages:
- Django 6.0.2
- Django REST Framework 3.16.1
- djangorestframework-simplejwt 5.5.1
- psycopg2-binary 2.9.11 (PostgreSQL adapter)
- asgiref 3.11.1
- sqlparse 0.5.5

To activate (Windows PowerShell):
```bash
./env/Scripts/Activate.ps1
```

To install new packages:
```bash
pip install <package_name>
```

## Important Notes & Warnings

1. **Hardcoded Credentials**: Database password is hardcoded in `settings.py`. Use environment variables in production.
2. **Secret Key**: `SECRET_KEY` is exposed in `settings.py`. Use env vars for production.
3. **DEBUG = True**: Only safe for development. Turn off in production.
4. **ALLOWED_HOSTS = []**: Empty in dev. Populate with domain(s) before deployment.
5. **Email-based Auth**: The custom User model uses `email` as the unique identifier—no traditional usernames.
6. **Serializer Naming**: This project uses `serializer.py` (singular) instead of `serializers.py`—follow this convention.

## Next Steps for Development

The following apps are stubs and need implementation:
- **courses**: Define Course model, create views for CRUD operations
- **enrollments**: Link User → Course, manage enrollment lifecycle
- **reviews**: Allow students to rate courses, add review endpoints
- **dashboard**: Aggregate data for student/instructor/admin dashboards

Each app should follow the same pattern: models → serializers → views → URLs.
