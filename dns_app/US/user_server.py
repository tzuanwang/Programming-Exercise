import pickle
import requests
import socket
from flask import Flask, request

app = Flask(__name__)
BUFFER_SIZE = 2048

@app.route('/')
def welcome():
    return 'US - User Server'

@app.route('/calculate_fibonacci', methods=["GET"])
def fibonacci():

    # Get data from the request parameters
    user_host = request.args.get('user_host').replace('"', '')
    fs_port = int(request.args.get('fs_port'))
    fibonacci_number = int(request.args.get('fibonacci_number'))
    as_ip = request.args.get('as_ip').replace('"', '')
    as_port = int(request.args.get('as_port'))

    # Create a UDP socket
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Prepare and send a request to the AS (Application Server)
    request_data = ("A", user_host)
    udp_socket.sendto(pickle.dumps(request_data), (as_ip, as_port))

    # Receive and deserialize the response from the AS
    response, _ = udp_socket.recvfrom(BUFFER_SIZE)
    response = pickle.loads(response)
    as_hostname, fs_ip = response

    if not fs_ip:
        return "Couldn't retrieve fs_ip"

    # Make a request to the Fibonacci Server (FS)
    fs_response = requests.get(f"http://{fs_ip}:{fs_port}/calculate_fibonacci",
                               params={"fibonacci_number": fibonacci_number}).content

    return fs_response

# Run the Flask app
app.run(host='0.0.0.0', port=8080, debug=True)
