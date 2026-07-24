from flask import Blueprint, request, jsonify

courses_bp = Blueprint('courses', __name__, url_prefix='/api/courses')

courses_db = []
course_id_counter = 1

def make_response_json(data, status_code):
    return jsonify({'status': 'success', 'data': data}), status_code

@courses_bp.route('/', methods=['GET'])
def get_courses():
    return make_response_json(courses_db, 200)

@courses_bp.route('/', methods=['POST'])
def create_course():
    global course_id_counter
    data = request.get_json()
    if not data:
        return jsonify({'status': 'error', 'message': 'Invalid JSON'}), 400
    
    required_fields = ['name', 'code', 'credits']
    for field in required_fields:
        if field not in data:
            return jsonify({'status': 'error', 'message': f'Missing required field: {field}'}), 400
            
    new_course = {
        'id': course_id_counter,
        'name': data['name'],
        'code': data['code'],
        'credits': data['credits']
    }
    course_id_counter += 1
    courses_db.append(new_course)
    
    return make_response_json(new_course, 201)

@courses_bp.route('/<int:course_id>', methods=['GET'])
def get_course(course_id):
    course = next((c for c in courses_db if c['id'] == course_id), None)
    if not course:
        return jsonify({'status': 'error', 'message': 'Course not found'}), 404
    return make_response_json(course, 200)

@courses_bp.route('/<int:course_id>', methods=['PUT'])
def update_course(course_id):
    data = request.get_json()
    if not data:
        return jsonify({'status': 'error', 'message': 'Invalid JSON'}), 400

    course = next((c for c in courses_db if c['id'] == course_id), None)
    if not course:
        return jsonify({'status': 'error', 'message': 'Course not found'}), 404
        
    course['name'] = data.get('name', course['name'])
    course['code'] = data.get('code', course['code'])
    course['credits'] = data.get('credits', course['credits'])
    
    return make_response_json(course, 200)

@courses_bp.route('/<int:course_id>', methods=['DELETE'])
def delete_course(course_id):
    global courses_db
    course = next((c for c in courses_db if c['id'] == course_id), None)
    if not course:
        return jsonify({'status': 'error', 'message': 'Course not found'}), 404
        
    courses_db = [c for c in courses_db if c['id'] != course_id]
    return make_response_json({'message': 'Course deleted'}, 200)
