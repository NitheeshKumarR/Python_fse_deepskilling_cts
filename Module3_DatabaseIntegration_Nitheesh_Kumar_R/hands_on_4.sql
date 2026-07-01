-- Task 1: Baseline Performance
EXPLAIN
SELECT s.first_name,
       s.last_name,
       c.course_name
FROM enrollments e
JOIN students s
    ON s.student_id = e.student_id
JOIN courses c
    ON c.course_id = e.course_id
WHERE s.enrollment_year = 2022;

/*

"QUERY PLAN"
"Nested Loop  (cost=12.16..42.16 rows=9 width=554)"
"  ->  Hash Join  (cost=12.01..40.40 rows=9 width=240)"
"        Hash Cond: (e.student_id = s.student_id)"
"        ->  Seq Scan on enrollments e  (cost=0.00..24.50 rows=1450 width=8)"
"        ->  Hash  (cost=12.00..12.00 rows=1 width=240)"
"              ->  Seq Scan on students s  (cost=0.00..12.00 rows=1 width=240)"
"                    Filter: (enrollment_year = 2022)"
"  ->  Index Scan using courses_pkey on courses c  (cost=0.14..0.20 rows=1 width=322)"
"        Index Cond: (course_id = e.course_id)"

Observation:
- students uses Seq Scan
- enrollments uses Seq Scan
- courses uses Seq Scan
- Estimated cost: (copy from EXPLAIN output)
*/



--Task 2: Add Indexes and Compare Plans

CREATE INDEX idx_students_enrollment_year
ON students(enrollment_year);

CREATE UNIQUE INDEX idx_enrollments_student_course
ON enrollments(student_id, course_id);

CREATE INDEX idx_courses_course_code
ON courses(course_code);

CREATE INDEX idx_enrollments_null_grade
ON enrollments(student_id)
WHERE grade IS NULL;


EXPLAIN
SELECT s.first_name,
       s.last_name,
       c.course_name
FROM enrollments e
JOIN students s
ON s.student_id = e.student_id
JOIN courses c
ON c.course_id = e.course_id
WHERE s.enrollment_year = 2022;

/*
After creating indexes:

PostgreSQL still uses Seq Scan because the tables contain only
8 students, 12 enrollments and 5 courses.

For larger tables the planner would likely use an Index Scan on
students.enrollment_year.
*/
