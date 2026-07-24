import requests
import time
import subprocess
import os
import sys

def main():
    print("Starting microservices...")
    
    # Start course service
    course_proc = subprocess.Popen([sys.executable, "app.py"], cwd="course_service")
    # Start student service
    student_proc = subprocess.Popen([sys.executable, "app.py"], cwd="student_service")
    # Start gateway
    gateway_proc = subprocess.Popen([sys.executable, "app.py"], cwd="gateway")
    
    time.sleep(3) # Wait for servers to spin up
    
    try:
        print("\n--- Testing Gateway routing to Course Service ---")
        resp = requests.get("http://localhost:5000/api/courses/")
        print(f"Status Code: {resp.status_code}")
        print(f"Response: {resp.json()}")
        assert resp.status_code == 200

        print("\n--- Testing Inter-service call (Student -> Course) ---")
        # Alice enrolling in CS101 (course_id 1)
        resp = requests.post("http://localhost:5000/api/students/1/enroll", json={"course_id": 1})
        print(f"Status Code: {resp.status_code}")
        print(f"Response: {resp.json()}")
        assert resp.status_code == 201

        print("\n--- Testing Course Service failure scenario (503) ---")
        course_proc.terminate() # Kill course service
        course_proc.wait()
        
        # Try enrolling again
        resp = requests.post("http://localhost:5000/api/students/1/enroll", json={"course_id": 2})
        print(f"Status Code: {resp.status_code}")
        print(f"Response: {resp.json()}")
        assert resp.status_code == 503

        print("\nAll tests passed successfully! Architecture works as expected.")
    finally:
        # Cleanup processes
        course_proc.terminate()
        student_proc.terminate()
        gateway_proc.terminate()

if __name__ == "__main__":
    main()
