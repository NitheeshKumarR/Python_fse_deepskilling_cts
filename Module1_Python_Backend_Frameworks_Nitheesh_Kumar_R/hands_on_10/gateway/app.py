from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

SERVICES = {
    'courses': 'http://localhost:5001',
    'students': 'http://localhost:5002'
}

@app.route('/api/<service_name>/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
@app.route('/api/<service_name>/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def gateway(service_name, path):
    if service_name not in SERVICES:
        return jsonify({"error": "Service not found in gateway configuration"}), 404

    target_url = f"{SERVICES[service_name]}/api/{service_name}/{path}"
    
    try:
        # Proxy the request to the target service
        resp = requests.request(
            method=request.method,
            url=target_url,
            headers={key: value for (key, value) in request.headers if key != 'Host'},
            data=request.get_data(),
            cookies=request.cookies,
            allow_redirects=False
        )
        return resp.content, resp.status_code, resp.headers.items()
    except requests.exceptions.ConnectionError:
        return jsonify({"error": f"{service_name.capitalize()} Service is currently unavailable"}), 503

if __name__ == '__main__':
    app.run(port=5000)
