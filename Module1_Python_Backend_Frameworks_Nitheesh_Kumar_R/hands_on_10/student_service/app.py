from flask import Flask, request, jsonify
import requests
from models import db, Student, Enrollment

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

COURSE_SERVICE_URL = "http://localhost:5001"

with app.app_context():
    db.create_all()
    if not Student.query.first():
        s1 = Student(first_name="Alice", last_name="Smith", email="alice@test.com")
        db.session.add(s1)
        db.session.commit()

@app.route('/api/students/', methods=['GET'])
def get_students():
    students = Student.query.all()
    return jsonify([s.to_dict() for s in students]), 200

@app.route('/api/students/<int:student_id>/enroll', methods=['POST'])
def enroll_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify({"error": "Student not found"}), 404

    data = request.get_json()
    course_id = data.get('course_id')
    
    if not course_id:
        return jsonify({"error": "course_id is required"}), 400

    # Synchronous Inter-service call to Course Service
    try:
        response = requests.get(f"{COURSE_SERVICE_URL}/api/courses/{course_id}")
        if response.status_code == 404:
            return jsonify({"error": "Course does not exist in Course Service"}), 404
        response.raise_for_status()
    except requests.exceptions.ConnectionError:
        return jsonify({"error": "Course Service is unavailable"}), 503
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error communicating with Course Service: {str(e)}"}), 500

    new_enrollment = Enrollment(student_id=student.id, course_id=course_id)
    db.session.add(new_enrollment)
    db.session.commit()

    return jsonify(new_enrollment.to_dict()), 201

if __name__ == '__main__':
    app.run(port=5002)
