import unittest
import zmq
import threading
import time


def send_command(command):
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")

    # Send the command
    socket.send_json(command)

    # Receive the response
    response = socket.recv_json()
    return response


def client_thread(command, results, index):
    response = send_command(command)
    results[index] = response  # Store the response in the results list


class TestZMQServer(unittest.TestCase):

    def test_concurrent_requests(self):
        commands = [
            {"type": "math", "operation": "add", "a": 5, "b": 3},
            {"type": "math", "operation": "subtract", "a": 10, "b": 4},
            {"type": "math", "operation": "multiply", "a": 6, "b": 7},
            {"type": "math", "operation": "divide", "a": 15, "b": 3},
            {"type": "os", "command": "echo Hello World"},
        ]

        expected_results = [
            {"status": "success", "result": 8},
            {"status": "success", "result": 6},
            {"status": "success", "result": 42},
            {"status": "success", "result": 5},
            {"status": "success", "result": "Hello World\n"},  # Adjust based on your environment
        ]

        threads = []
        results = [None] * len(commands)

        for index, command in enumerate(commands):
            thread = threading.Thread(target=client_thread, args=(command, results, index))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        for result, expected in zip(results, expected_results):
            self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
