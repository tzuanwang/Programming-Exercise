from flask import Flask, request
import socket
import pickle

app = Flask(__name__)
BUFFER_SIZE = 1024

@app.route('/')
def welcome():
    return "FS - Fibonacci Server"

# Fibonacci Function
def calculate_fibonacci(n):
    if n < 0:
        raise ValueError("n should be greater than or equal to 0")
    elif n == 0:
        return 0
    elif n == 1 or n == 2:
        return 1
    else:
        return calculate_fibonacci(n - 1) + calculate_fibonacci(n - 2)

# Calculating Fibonacci
@app.route('/calculate_fibonacci')
def handle_f_request():
    number = int(request.args.get('number'))
    result = calculate_fibonacci(number)
    return str(result)

# Registering Service
@app.route('/register_service', methods=['PUT'])
def regist_service():
    request_body = request.json
    if not request_body:
        raise ValueError("Request body is empty")
    
    # Extracting Data
    service_name = request_body["service_name"]
    service_ip   = request_body["service_ip"]
    as_ip        = request_body["as_ip"]
    as_port      = request_body["as_port"]
    ttl          = request_body["ttl"]

    # Prepare and send the registration message to the AS (Application Server)
    registration_data = (service_name, service_ip, "A", ttl)
    message_bytes = pickle.dumps(registration_data)
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.sendto(message_bytes, (as_ip, as_port))

    return "Registration Successful!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9090, debug=True)

