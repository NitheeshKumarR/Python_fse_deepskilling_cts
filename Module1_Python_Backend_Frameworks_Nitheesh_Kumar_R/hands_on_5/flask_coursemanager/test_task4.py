import pytest
from app import create_app

app = create_app()
app.config['TESTING'] = True
client = app.test_client()

def test_get_courses_empty():
    response = client.get('/api/courses/')
    assert response.status_code == 200
    assert response.json['data'] == []

def test_create_course_missing_fields():
    response = client.post('/api/courses/', json={'name': 'Flask 101'})
    assert response.status_code == 400
    assert 'Missing required field' in response.json['message']

def test_create_course_success():
    response = client.post('/api/courses/', json={
        'name': 'Flask 101', 'code': 'CS102', 'credits': 3
    })
    assert response.status_code == 201
    assert response.json['data']['name'] == 'Flask 101'
    assert response.json['data']['id'] == 1

def test_get_course_success():
    response = client.get('/api/courses/1')
    assert response.status_code == 200
    assert response.json['data']['code'] == 'CS102'

def test_get_course_not_found():
    response = client.get('/api/courses/99')
    assert response.status_code == 404
    assert 'Course not found' in response.json['message']

def test_update_course_success():
    response = client.put('/api/courses/1', json={'credits': 4})
    assert response.status_code == 200
    assert response.json['data']['credits'] == 4

def test_delete_course_success():
    response = client.delete('/api/courses/1')
    assert response.status_code == 200
    
    response = client.get('/api/courses/1')
    assert response.status_code == 404

def test_404_error_handler():
    response = client.get('/api/invalid_url')
    assert response.status_code == 404
    assert response.json['status'] == 'error'
    assert response.json['message'] == 'Resource not found'

if __name__ == '__main__':
    test_get_courses_empty()
    test_create_course_missing_fields()
    test_create_course_success()
    test_get_course_success()
    test_get_course_not_found()
    test_update_course_success()
    test_delete_course_success()
    test_404_error_handler()
    print("All tests passed successfully!")
