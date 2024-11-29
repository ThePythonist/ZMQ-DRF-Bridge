import zmq
import subprocess
from api.customlogs import make_log, tictoc


@tictoc
def process_command(command):
    try:
        if command['type'] == 'os':
            try:
                result = subprocess.check_output(command['command'], shell=True, text=True)
                return {'status': 'success', 'result': result}
            except subprocess.CalledProcessError:
                return {'status': 'error', 'message': 'Invalid command'}

        elif command['type'] == 'math':
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
        message = socket.recv_json()
        print(f"Received command: {message}")
        response = process_command(message)
        socket.send_json(response)


start_zmq_server()
