import psycopg2
import time

# ==========================
# PostgreSQL Connection
# ==========================

conn = psycopg2.connect(
    host="localhost",
    database="college_db", 
    user="postgres",
    password="12345678",
    port="5432"
)

cursor = conn.cursor()

print("=" * 60)
print("TASK 3 - N+1 QUERY PROBLEM")
print("=" * 60)

# ======================================================
# Version 1 : N+1 Problem
# ======================================================

query_count = 0

start_time = time.time()

# Query 1
cursor.execute("""
SELECT enrollment_id, student_id, course_id, grade
FROM enrollments;
""")
query_count += 1

enrollments = cursor.fetchall()

n_plus_one_result = []

# One query per enrollment
for enrollment in enrollments:

    enrollment_id = enrollment[0]
    student_id = enrollment[1]
    course_id = enrollment[2]
    grade = enrollment[3]

    cursor.execute("""
    SELECT first_name, last_name
    FROM students
    WHERE student_id = %s;
    """, (student_id,))

    query_count += 1

    student = cursor.fetchone()

    n_plus_one_result.append(
        (
            enrollment_id,
            student[0],
            student[1],
            course_id,
            grade
        )
    )

end_time = time.time()

n_plus_one_time = end_time - start_time

print("\nVERSION 1 (N+1)")
print("-" * 40)
print(f"Queries Executed : {query_count}")
print(f"Execution Time   : {n_plus_one_time:.6f} seconds")

print("\nSample Records:")

for row in n_plus_one_result[:5]:
    print(row)

# ======================================================
# Version 2 : Optimized JOIN
# ======================================================

start_time = time.time()

cursor.execute("""
SELECT
    e.enrollment_id,
    s.first_name,
    s.last_name,
    c.course_name,
    e.grade
FROM enrollments e
JOIN students s
ON e.student_id = s.student_id
JOIN courses c
ON e.course_id = c.course_id;
""")

join_result = cursor.fetchall()

end_time = time.time()

join_time = end_time - start_time

print("\n")
print("=" * 60)

print("VERSION 2 (JOIN)")
print("-" * 40)
print("Queries Executed : 1")
print(f"Execution Time   : {join_time:.6f} seconds")

print("\nSample Records:")

for row in join_result[:5]:
    print(row)

print("\n")
print("=" * 60)

# ======================================================
# Comparison
# ======================================================

print("COMPARISON")
print("-" * 40)

print(f"N+1 Queries : {query_count}")
print("JOIN Queries: 1")

print(f"N+1 Time : {n_plus_one_time:.6f} sec")
print(f"JOIN Time: {join_time:.6f} sec")

print(f"Extra Queries Saved: {query_count - 1}")

print("\nObservation:")
print("The JOIN approach retrieves all required data in a")
print("single database query, avoiding the N+1 problem.")

print("\nFor 10,000 enrollments:")
print("N+1 Version : 10,001 queries")
print("JOIN Version: 1 query")
print("Extra Queries Issued by N+1: 10,000")

# ======================================================
# Verify Results
# ======================================================

print("\n")
print("=" * 60)

print("Verification")
print("-" * 40)

print(f"N+1 Rows Returned : {len(n_plus_one_result)}")
print(f"JOIN Rows Returned: {len(join_result)}")

if len(n_plus_one_result) == len(join_result):
    print("Both approaches returned the same number of records.")
else:
    print("Mismatch detected!")

cursor.close()
conn.close()

print("\nDatabase connection closed.")