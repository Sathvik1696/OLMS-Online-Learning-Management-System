from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('index.html', views.index, name='index_fallback'),
    path('login.html', views.login_view, name='login'),
    path('login/', views.login_view, name='login_slash'),
    path('register.html', views.register_view, name='register'),
    path('register/', views.register_view, name='register_slash'),
    path('courses.html', views.courses_view, name='courses'),
    path('courses/', views.courses_view, name='courses_slash'),
    path('dashboard.html', views.dashboard_view, name='dashboard'),
    path('dashboard/', views.dashboard_view, name='dashboard_slash'),
    
    # New Pages
    path('enrollments/', views.enrollments_view, name='enrollments'),
    path('reviews/', views.reviews_view, name='reviews'),
    path('course/<int:course_id>/', views.course_detail_view, name='course_detail'),
    path('course_detail.html', views.course_detail_fallback, name='course_detail_fallback'),
    path('enrollments.html', views.enrollments_view, name='enrollments_fallback'),
    path('reviews.html', views.reviews_view, name='reviews_fallback'),
]
