import unittest
import zmq
import threading


class TestZMQServer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.context = zmq.Context()
        cls.socket = cls.context.socket(zmq.REQ)
        cls.socket.connect("tcp://localhost:5555")
        cls.lock = threading.Lock()

    @classmethod
    def tearDownClass(cls):
        cls.socket.close()
        cls.context.term()

    def send_command(self, command):
        with self.lock:  # Ensure thread safety
            self.socket.send_json(command)
            return self.socket.recv_json()

    def client_thread(self, command, results, index):
        response = self.send_command(command)
        results[index] = response  # Store the response in the results list

    def test_concurrent_requests(self):
        commands = [
            {"type": "math", "operation": "add", "a": 5, "b": 3},
            {"type": "math", "operation": "subtract", "a": 10, "b": 4},
            {"type": "math", "operation": "multiply", "a": 6, "b": 7},
            {"type": "math", "operation": "divide", "a": 15, "b": 3},
            {"type": "os", "command": "echo Hello World"},
            {"type": "os", "command": "ipconfig"},
            {"type": "os", "command": "arp -a"},
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
            thread = threading.Thread(target=self.client_thread, args=(command, results, index))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        for result, expected in zip(results, expected_results):
            self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
