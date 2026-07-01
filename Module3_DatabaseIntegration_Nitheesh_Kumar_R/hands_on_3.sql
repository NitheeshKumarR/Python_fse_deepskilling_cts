--Task 1: Subqueries
-- Find all students who are enrolled in more courses than the average number of enrollments per student.
select s.student_id, CONCAT(s.first_name,' ',s.last_name) as full_name, count(e.student_id) as numberOfCourses
from students s right join enrollments e on s.student_id = e.student_id 
group by s.student_id,s.first_name,s.last_name
having count(e.student_id) > (select count(*)* 1.0/count(distinct student_id) from enrollments);

-- List courses in which all enrolled students have received a grade of 'A'.
SELECT c.course_id,c.course_name
FROM courses c
WHERE NOT EXISTS
(
    SELECT *
    FROM enrollments e
    WHERE e.course_id = c.course_id
      AND e.grade <> 'A'
);


-- Find the professor with the highest salary in each department using a correlated subquery
SELECT p.professor_id,p.prof_name,p.department_id,p.salary
FROM professors p
WHERE p.salary =
(
    SELECT MAX(p2.salary)
    FROM professors p2
    WHERE p2.department_id = p.department_id
);


-- Using a subquery in the FROM clause (derived table), calculate the per-department average salary and then filter to departments where that average exceeds 85,000.
SELECT d.department_id,
       d.dept_name,
       t.avg_salary
FROM departments d
JOIN
(
    SELECT department_id,
           AVG(salary) AS avg_salary
    FROM professors
    GROUP BY department_id
) AS t
ON d.department_id = t.department_id
WHERE t.avg_salary > 85000;


--Task 2: Creating and Using Views
-- Create a view vw_student_enrollment_summary showing each student's full name, department, number of courses enrolled in, and GPA (average grade converted: A=4, B=3, C=2, D=1, F=0).
CREATE VIEW vw_student_enrollment_summary AS
SELECT
    s.student_id,
    CONCAT(s.first_name, ' ', s.last_name) AS full_name,
    d.dept_name AS department,
    COUNT(e.course_id) AS number_of_courses,
    AVG(
        CASE e.grade
            WHEN 'A' THEN 4
            WHEN 'B' THEN 3
            WHEN 'C' THEN 2
            WHEN 'D' THEN 1
            WHEN 'F' THEN 0
        END
    ) AS GPA
FROM students s
JOIN departments d
ON s.department_id = d.department_id
LEFT JOIN enrollments e
ON s.student_id = e.student_id
GROUP BY s.student_id, s.first_name, s.last_name, d.dept_name;

--Create a view vw_course_stats showing course_name, course_code, total_enrollments, and avg_gpa for each course.
CREATE VIEW vw_course_stats AS
SELECT
    c.course_name,
    c.course_code,
    COUNT(e.student_id) AS total_enrollments,
    AVG(
        CASE e.grade
            WHEN 'A' THEN 4
            WHEN 'B' THEN 3
            WHEN 'C' THEN 2
            WHEN 'D' THEN 1
            WHEN 'F' THEN 0
        END
    ) AS avg_gpa
FROM courses c
LEFT JOIN enrollments e
ON c.course_id = e.course_id
GROUP BY c.course_id, c.course_name, c.course_code;

-- Query vw_student_enrollment_summary to find students with GPA above 3.0.
SELECT *
FROM vw_student_enrollment_summary
WHERE GPA > 3.0;

--Attempt to UPDATE a row through vw_student_enrollment_summary and note what happens. Research and document in your comments why multi-table views are generally not updatable.
UPDATE vw_student_enrollment_summary
SET GPA = 4
WHERE student_id = 1;
--ERROR: The target table of the UPDATE is not updatable.

-- DROP both views and recreate vw_student_enrollment_summary as a view WITH CHECK OPTION (use a single-table subset view for this step)
DROP VIEW vw_student_enrollment_summary;
DROP VIEW vw_course_stats;



-- Task 3: Stored Procedures and Transactions

-- 44. Write a function fn_enroll_student that accepts student_id,
-- course_id, and enrollment_date, checks for duplicate enrollment,
-- and inserts the record.

CREATE OR REPLACE FUNCTION fn_enroll_student(
    p_student_id INT,
    p_course_id INT,
    p_enrollment_date DATE
)
RETURNS VOID
LANGUAGE plpgsql
AS $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM enrollments
        WHERE student_id = p_student_id
          AND course_id = p_course_id
    ) THEN
        RAISE EXCEPTION 'Student is already enrolled in this course.';
    END IF;

    INSERT INTO enrollments(student_id, course_id, enrollment_date)
    VALUES (p_student_id, p_course_id, p_enrollment_date);
END;
$$;

-- Test
SELECT fn_enroll_student(1, 3, '2025-10-01');


-- 45. Write a function fn_transfer_student that moves a student
-- from one department to another and logs the transfer.

CREATE TABLE department_transfer_log(
    log_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    student_id INT,
    old_department INT,
    new_department INT,
    transfer_date TIMESTAMP
);

CREATE OR REPLACE FUNCTION fn_transfer_student(
    p_student_id INT,
    p_new_department INT
)
RETURNS VOID
LANGUAGE plpgsql
AS $$
DECLARE
    v_old_department INT;
BEGIN
    SELECT department_id
    INTO v_old_department
    FROM students
    WHERE student_id = p_student_id;

    UPDATE students
    SET department_id = p_new_department
    WHERE student_id = p_student_id;

    INSERT INTO department_transfer_log
    (student_id, old_department, new_department, transfer_date)
    VALUES
    (p_student_id, v_old_department, p_new_department, CURRENT_TIMESTAMP);
END;
$$;

-- Execute inside a transaction
BEGIN;

SELECT fn_transfer_student(1, 3);

COMMIT;


-- 46. Test transaction rollback by introducing an error

BEGIN;

SELECT fn_transfer_student(1, 999);

COMMIT;

-- If an error occurs, execute:
ROLLBACK;

-- Verify student department
SELECT *
FROM students
WHERE student_id = 1;


-- 47. Use SAVEPOINT

BEGIN;

INSERT INTO enrollments(student_id, course_id, enrollment_date)
VALUES (1, 101, CURRENT_DATE);

SAVEPOINT sp1;

-- This should fail if course_id 999 does not exist
INSERT INTO enrollments(student_id, course_id, enrollment_date)
VALUES (1, 999, CURRENT_DATE);

ROLLBACK TO SAVEPOINT sp1;

COMMIT;

-- Verify
SELECT *
FROM enrollments
WHERE student_id = 1;