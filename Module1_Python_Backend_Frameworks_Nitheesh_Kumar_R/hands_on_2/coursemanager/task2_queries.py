import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coursemanager.settings')
django.setup()

from django.contrib.auth.models import User
from courses.models import Department, Course, Student, Enrollment
from django.db.models import Count, F

# Create superuser
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@college.edu', 'Admin@123')
    print("Superuser created")

# Create initial data
cs, _ = Department.objects.get_or_create(name='Computer Science', defaults={'head_of_dept': 'Dr. Alan Turing', 'budget': 50000})
math, _ = Department.objects.get_or_create(name='Mathematics', defaults={'head_of_dept': 'Dr. John Nash', 'budget': 30000})

c1, _ = Course.objects.get_or_create(name='Intro to Programming', code='CS101', defaults={'credits': 3, 'department': cs})
c2, _ = Course.objects.get_or_create(name='Data Structures', code='CS201', defaults={'credits': 4, 'department': cs})
c3, _ = Course.objects.get_or_create(name='Calculus I', code='MATH101', defaults={'credits': 4, 'department': math})
c4, _ = Course.objects.get_or_create(name='Linear Algebra', code='MATH201', defaults={'credits': 3, 'department': math})

s1, _ = Student.objects.get_or_create(email='alice@college.edu', defaults={'first_name': 'Alice', 'last_name': 'Smith', 'department': cs, 'enrollment_year': 2023})
s2, _ = Student.objects.get_or_create(email='bob@college.edu', defaults={'first_name': 'Bob', 'last_name': 'Jones', 'department': cs, 'enrollment_year': 2023})
s3, _ = Student.objects.get_or_create(email='charlie@college.edu', defaults={'first_name': 'Charlie', 'last_name': 'Brown', 'department': math, 'enrollment_year': 2022})
s4, _ = Student.objects.get_or_create(email='diana@college.edu', defaults={'first_name': 'Diana', 'last_name': 'Prince', 'department': math, 'enrollment_year': 2022})
s5, _ = Student.objects.get_or_create(email='eve@college.edu', defaults={'first_name': 'Eve', 'last_name': 'White', 'department': cs, 'enrollment_year': 2024})

# Enrollments for testing admin constraint
Enrollment.objects.get_or_create(student=s1, course=c1, defaults={'grade': 'A'})
Enrollment.objects.get_or_create(student=s1, course=c2, defaults={'grade': 'B'})
Enrollment.objects.get_or_create(student=s2, course=c1, defaults={'grade': 'A'})
Enrollment.objects.get_or_create(student=s3, course=c3, defaults={'grade': 'C'})


# Queries
print("17. Query all courses in a specific department:")
cs_courses = Course.objects.filter(department__name='Computer Science')
print(cs_courses)

print("\n18. Count the number of courses per department:")
dept_counts = Department.objects.annotate(course_count=Count('course'))
for d in dept_counts:
    print(f"{d.name}: {d.course_count} courses")

print("\n19. select_related for students and departments:")
students = Student.objects.select_related('department').all()
for s in students:
    print(f"{s.first_name} {s.last_name} - {s.department.name}")

print("\n20. Update budget of all departments by 10%:")
Department.objects.update(budget=F('budget') * 1.1)
print("Updated budgets:")
for d in Department.objects.all():
    print(f"{d.name}: {d.budget}")
