# Backend Architecture of OCMS (Online Course Management System)

This document provides an overview of the backend components of the OCMS project, which is built using the Django framework. It details the data models and views that power the application.

## 1. Project Configuration (`olms/settings.py`)
*   **Database:** PostgreSQL is used as the relational database `olms` with user `postgres` and password `Sathvik@1696` on `localhost:5432`.
*   **Installed Apps:** The project is modular, containing several custom apps: `accounts`, `courses`, `enrollments`, `reviews`, `dashboard`, and `frontend_app`. It also integrates `rest_framework` for potential API development.
*   **Authentication:** The standard Django user model has been replaced by a custom model (`AUTH_USER_MODEL ='accounts.user'`).

## 2. Data Models (Database Schema)

The database schema is defined across different Django applications:

### `accounts.models.User`
*   Extends `AbstractUser`, removing the standard `username` field.
*   Uses `email` as the unique identifier (`USERNAME_FIELD = 'email'`).
*   Includes `full_name`.
*   Implments Role-Based Access Control (RBAC) with a `role` field: `STUDENT`, `INSTRUCTOR`, or `ADMIN`.
*   Uses a `CustomUserManager` to handle user and superuser creation logic.

### `courses.models`
*   **`Course`:** Represents a course offering.
    *   Fields: `title`, `description`, `price`, `level`.
    *   Relationships: Stores `instructor` and `category` as simple integers (IDs).
    *   State: `is_published` boolean flag.
*   **`Module`:** Represents a section within a course.
    *   Fields: `title`.
    *   Relationships: Linked to a course via `course` (integer ID).
*   **`Lecture`:** Represents individual lesson content.
    *   Fields: `title`, `content`.
    *   Relationships: Linked to a module via `module` (integer ID).

### `enrollments.models.Enrollment`
*   Tracks which student is taking which course.
*   Fields: `student` (ID), `course` (ID), `status` (default: "enrolled"), `enrolled_at`, `completed_at`.

### `reviews.models.Review`
*   Allows students to rate and comment on courses.
*   Fields: `student` (ID), `course` (ID), `rating` (integer), `comment` (text), `created_at`.

*Note: In the current schema, relationships between models (like `Course` to `Instructor`, or `Enrollment` to `Student`/`Course`) are stored as simple `integer` fields rather than Django ForeignKeys. This means the joins are handled manually in the views.*

## 3. View Logic (`frontend_app/views.py`)

The views act as the controllers, fetching data from the models and passing it to the HTML templates.

*   **Static Pages:** `index`, `login_view`, and `register_view` simply render their respective templates.
*   **`courses_view`:** Fetches all published courses (`is_published=True`), ordered by newest first, and passes them to `courses.html`.
*   **`dashboard_view`:** Simulates enrolled courses by fetching the 4 most recently published courses. It also passes the total count of published courses.
*   **`enrollments_view`:** Retrieves all enrollments. It manually performs a "join" by fetching all courses and mapping the course data to each enrollment object before passing it to the template.
*   **`reviews_view`:** Similar to enrollments, it fetches all reviews and manually attaches the corresponding course data to each review for display.
*   **`course_detail_view(request, course_id)`:**
    *   Fetches the specific `Course` by ID.
    *   Fetches all `Module`s associated with that course.
    *   Fetches *all* `Lecture`s, then manually groups them by their `module` ID in Python code.
    *   Attaches the grouped lectures to their respective modules and passes the structured data to `course_detail.html`.
*   **`course_detail_fallback`:** A safety view. If a user navigates generically to course details, it attempts to load the first published course instead of crashing.
