--TASK 1

-- Inserting the sample data from the Common Schema section into all five tables
-- departments
INSERT INTO departments (dept_name, hod_name, budget) VALUES
  ('Computer Science', 'Dr. Ramesh Kumar', 850000.00),
  ('Electronics', 'Dr. Priya Nair', 620000.00),
  ('Mechanical', 'Dr. Suresh Iyer', 540000.00),
  ('Civil', 'Dr. Ananya Sharma', 430000.00);
  
  -- students
INSERT INTO students (first_name, last_name, email, date_of_birth, department_id, 
enrollment_year) VALUES
  ('Arjun',  'Mehta',    'arjun.mehta@college.edu',    '2003-04-12', 1, 2022),
  ('Priya',  'Suresh',   'priya.suresh@college.edu',   '2003-07-25', 1, 2022),
  ('Rohan',  'Verma',    'rohan.verma@college.edu',    '2002-11-08', 2, 2021),
  ('Sneha',  'Patel',    'sneha.patel@college.edu',    '2004-01-30', 3, 2023),
  ('Vikram', 'Das',      'vikram.das@college.edu',     '2003-09-14', 1, 2022),
  ('Kavya',  'Menon',    'kavya.menon@college.edu',    '2002-05-17', 2, 2021),
  ('Aditya', 'Singh',    'aditya.singh@college.edu',   '2004-03-22', 4, 2023),
  ('Deepika','Rao',      'deepika.rao@college.edu',    '2003-08-09', 1, 2022);
  
  -- courses
INSERT INTO courses (course_name, course_code, credits, department_id) VALUES
  ('Data Structures & Algorithms', 'CS101', 4, 1),
  ('Database Management Systems',  'CS102', 3, 1),
  ('Object Oriented Programming',  'CS103', 4, 1),
  ('Circuit Theory',               'EC101', 3, 2),
  ('Thermodynamics',               'ME101', 3, 3);
  
  -- enrollments
INSERT INTO enrollments (student_id, course_id, enrollment_date, grade) VALUES
  (1, 1, '2022-07-01', 'A'), (1, 2, '2022-07-01', 'B'),
  (2, 1, '2022-07-01', 'B'), (2, 3, '2022-07-01', 'A'),
  (3, 4, '2021-07-01', 'A'), (4, 5, '2023-07-01', NULL),
  (5, 1, '2022-07-01', 'C'), (5, 2, '2022-07-01', 'A'),
  (6, 4, '2021-07-01', 'B'), (7, 5, '2023-07-01', NULL),
  (8, 1, '2022-07-01', 'A'), (8, 3, '2022-07-01', 'B');

  -- professors
INSERT INTO professors (prof_name, email, department_id, salary) VALUES
  ('Dr. Anand Krishnan',  'anand.k@college.edu',   1, 95000.00),
  ('Dr. Meena Pillai',    'meena.p@college.edu',   1, 88000.00),
  ('Dr. Sunil Rajan',     'sunil.r@college.edu',   2, 82000.00),
  ('Dr. Latha Gopal',     'latha.g@college.edu',   3, 79000.00),
  ('Dr. Kartik Bose',     'kartik.b@college.edu',  4, 76000.00);

--Inserting two additional students into the students table.
SELECT COUNT(*) FROM students;
INSERT INTO students (first_name, last_name, email, date_of_birth, department_id, 
enrollment_year) VALUES
  ('Nitheesh',  'Kumar',    'nitheesh.kumar@college.edu',    '2003-12-01', 1, 2022),
  ('Ashwin',  'Kumar',   'ashwin.kumar@college.edu',   '2003-08-21', 2, 2021);
SELECT COUNT(*) FROM students;

--Updating the grade of student_id = 5 for course_id = 1 from 'C' to 'B'.
UPDATE enrollments SET grade='B' WHERE student_id=5 AND course_id=1;

--Delete enrollments where grade IS NULL (students who never received a grade).
SELECT COUNT(*) FROM enrollments;
DELETE FROM enrollments WHERE grade IS NULL;
SELECT COUNT(*) FROM enrollments;



--TASK 2

--Retrieve all students enrolled in 2022, ordered by last_name alphabetically.
SELECT * FROM students WHERE enrollment_year=2022 ORDER BY last_name;

--Find all courses with more than 3 credits, sorted by credits descending.
SELECT * FROM courses WHERE credits>3 ORDER BY credits DESC;

--List all professors whose salary is between 80,000 and 95,000.
SELECT * FROM professors WHERE salary BETWEEN 80000 AND 95000;

--Find all students whose email ends with '@college.edu' using the LIKE operator.
SELECT * FROM students WHERE email LIKE '%@college.edu';

-- Count the total number of students per enrollment_year.
SELECT enrollment_year, COUNT(enrollment_year) FROM students GROUP BY enrollment_year;



--TASK 3

-- List each student's full name (first_name + ' ' + last_name) alongside the name of their department. (JOIN students and departments.)
SELECT CONCAT(first_name,' ',last_name) as full_name, dept_name FROM students JOIN departments USING (department_id);

-- Show each enrollment along with the student's name and the course name. (3-table JOIN: enrollments, students, courses.)
SELECT e.enrollment_id, 
e.student_id, 
CONCAT(s.first_name,' ',s.last_name) as student_name, 
e.course_id, 
c.course_name, 
e.enrollment_date, 
e.grade 
FROM enrollments as e JOIN students as s  ON e.student_id=s.student_id
JOIN courses as c ON e.course_id=c.course_id;

--Find all students who are NOT enrolled in any course using a LEFT JOIN and WHERE ... IS NULL pattern.
SELECT * FROM students LEFT JOIN enrollments USING (student_id)
WHERE enrollment_id IS NULL;

-- Display every course along with the number of students enrolled in it. Courses with zero enrolments must still appear. 
--(LEFT JOIN courses with enrollments, GROUP BY course.)
SELECT course_id, course_name, COUNT(enrollment_id) as student_count 
FROM courses LEFT JOIN enrollments USING (course_id) 
GROUP BY course_id,course_name;

--List each department along with its professors and their salaries. Include departments that have no professors yet.
SELECT dept_name, prof_name, salary
FROM departments LEFT JOIN professors USING(department_id);



--TASK 4

-- Calculate the total number of enrollments per course. Display course_name and enrollment_count.
SELECT course_name, COUNT(enrollment_id) as enrollment_count
FROM courses LEFT JOIN enrollments USING(course_id)
GROUP BY course_id,course_name;

-- Find the average salary of professors per department. Round to 2 decimal places
SELECT dept_name, ROUND(AVG(salary),2) as average_salary
FROM departments LEFT JOIN professors USING (department_id)
GROUP BY department_id,dept_name;

--Find all departments where the total budget exceeds 600,000.
SELECT * FROM departments 
WHERE budget>600000;

--Show the grade distribution for course CS101: count of each grade (A, B, C, D, F).
SELECT e.grade, COUNT(*) AS grade_count
FROM enrollments e JOIN courses c ON e.course_id = c.course_id
WHERE c.course_code = 'CS101'
GROUP BY e.grade;

-- Using HAVING, list departments where more than 2 students are enrolled across all courses in that department
SELECT d.dept_name, COUNT(e.enrollment_id) AS student_count
FROM departments d JOIN courses c ON d.department_id = c.department_id
JOIN enrollments e ON c.course_id = e.course_id
GROUP BY d.department_id, d.dept_name
HAVING COUNT(e.enrollment_id) > 2;