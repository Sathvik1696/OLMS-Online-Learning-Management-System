from django.shortcuts import render

def index(request):
    return render(request, 'frontend_app/index.html')

def login_view(request):
    return render(request, 'frontend_app/login.html')

def register_view(request):
    return render(request, 'frontend_app/register.html')

from enrollments.models import Enrollment
from reviews.models import Review
from courses.models import Course, Module, Lecture

def courses_view(request):
    # Fetch real courses from the database
    courses = Course.objects.filter(is_published=True).order_by('-created_at')
    context = {
        'courses': courses
    }
    return render(request, 'frontend_app/courses.html', context)

def dashboard_view(request):
    # Fetch all published courses for the dashboard to simulate "enrolled" courses
    courses = Course.objects.filter(is_published=True).order_by('-created_at')[:4]
    
    context = {
        'courses_count': Course.objects.filter(is_published=True).count(),
        'enrolled_courses': courses
    }
    return render(request, 'frontend_app/dashboard.html', context)

def enrollments_view(request):
    # Fetch enrollments (simplification: fetching all for now)
    enrollments = Enrollment.objects.all().order_by('-enrolled_at')
    # To display course info, we'd ideally JOIN, but for now we fetch courses
    courses = Course.objects.all()
    course_map = {c.id: c for c in courses}
    
    # Attach course objects to enrollments for easy templating
    for e in enrollments:
        e.course_obj = course_map.get(e.course)
        
    context = {'enrollments': enrollments}
    return render(request, 'frontend_app/enrollments.html', context)

def reviews_view(request):
    reviews = Review.objects.all().order_by('-created_at')
    courses = Course.objects.all()
    course_map = {c.id: c for c in courses}
    
    for r in reviews:
        r.course_obj = course_map.get(r.course)
        
    context = {'reviews': reviews}
    return render(request, 'frontend_app/reviews.html', context)

def course_detail_view(request, course_id):
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        course = None
        
    modules = Module.objects.filter(course=course_id).order_by('created_at')
    lectures = Lecture.objects.all() # Fetch all and filter via dict
    
    # Group lectures by module
    module_lectures = {}
    for m in modules:
        module_lectures[m.id] = []
    for l in lectures:
        if l.module in module_lectures:
            module_lectures[l.module].append(l)
            
    # Attach to modules for easy templating
    for m in modules:
        m.lectures = module_lectures.get(m.id, [])
        
    context = {
        'course': course,
        'modules': modules
    }
    return render(request, 'frontend_app/course_detail.html', context)

def course_detail_fallback(request):
    """
    Fallback view for when a user manually types course_detail.html into the browser
    instead of navigating through the dynamic links. It tries to show the first available course.
    """
    first_course = Course.objects.filter(is_published=True).first()
    if first_course:
        return course_detail_view(request, first_course.id)
    else:
        # If no courses exist at all, just render the template with empty context
        return render(request, 'frontend_app/course_detail.html', {})
