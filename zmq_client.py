import zmq
import threading


def send_command(command):
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")

    # Send the command as a JSON object
    socket.send_json(command)

    # Receive the response
    response = socket.recv_json()
    print(f"Response: {response}")


def client_thread(command):
    send_command(command)


if __name__ == "__main__":
    commands = [
        {"type": "math", "operation": "add", "a": 5, "b": 3},
        {"type": "math", "operation": "subtract", "a": 10, "b": 4},
        {"type": "os", "command": "echo Hello World"},
        {"type": "math", "operation": "multiply", "a": 6, "b": 7},
        {"type": "os", "command": "ipconfig"},
    ]

    threads = []
    for command in commands:
        thread = threading.Thread(target=client_thread, args=(command,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
