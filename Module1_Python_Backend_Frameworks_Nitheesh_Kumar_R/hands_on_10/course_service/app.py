from flask import Flask, request, jsonify
from models import db, Course, Department

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///courses.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()
    # Seed data if empty
    if not Department.query.first():
        d1 = Department(name="Computer Science")
        d2 = Department(name="Mathematics")
        db.session.add_all([d1, d2])
        db.session.commit()
        
        c1 = Course(name="Intro to Programming", code="CS101", credits=3, department_id=d1.id)
        c2 = Course(name="Calculus I", code="MATH101", credits=4, department_id=d2.id)
        db.session.add_all([c1, c2])
        db.session.commit()

@app.route('/api/courses/', methods=['GET'])
def get_courses():
    courses = Course.query.all()
    return jsonify([c.to_dict() for c in courses]), 200

@app.route('/api/courses/<int:course_id>', methods=['GET'])
def get_course(course_id):
    course = Course.query.get(course_id)
    if not course:
        return jsonify({"error": "Course not found"}), 404
    return jsonify(course.to_dict()), 200

@app.route('/api/courses/', methods=['POST'])
def create_course():
    data = request.get_json()
    new_course = Course(
        name=data['name'],
        code=data['code'],
        credits=data['credits'],
        department_id=data['department_id']
    )
    db.session.add(new_course)
    db.session.commit()
    return jsonify(new_course.to_dict()), 201

if __name__ == '__main__':
    app.run(port=5001)
