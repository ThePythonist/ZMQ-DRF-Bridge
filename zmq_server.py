import zmq
import subprocess
from api.customlogs import make_log, tictoc


@tictoc
def handle_math(command):
    operation = command['operation']
    if operation == 'add':
        result = command['a'] + command['b']
    elif operation == 'subtract':
        result = command['a'] - command['b']
    elif operation == 'multiply':
        result = command['a'] * command['b']
    elif operation == 'divide':
        result = command['a'] / command['b']
    else:
        return {'status': 'error', 'message': 'Invalid math operation'}

    return {'status': 'success', 'result': result}


@tictoc
def handle_os(command):
    try:
        result = subprocess.check_output(command['command'], shell=True, text=True)
        return {'status': 'success', 'result': result}
    except subprocess.CalledProcessError:
        return {'status': 'error', 'message': 'Invalid os command'}


@tictoc
def process_command(command):
    try:
        if command['type'] == 'os':
            return handle_os(command)
        elif command['type'] == 'math':
            return handle_math(command)
        else:
            return {'status': 'error', 'message': 'Invalid command type'}

    except Exception as e:
        make_log("error", e)
        return {'status': 'error', 'message': str(e)}


def start_zmq_server():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")

    print("Server is running")
    while True:
        data = socket.recv_json()
        print(f"Received command: {data}")
        response = process_command(data)
        socket.send_json(response)


start_zmq_server()
