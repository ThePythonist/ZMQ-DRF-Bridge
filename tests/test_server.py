import unittest
import zmq
import threading


class TestZMQServer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Set up the ZeroMQ context and socket for the tests
        cls.context = zmq.Context()
        cls.socket = cls.context.socket(zmq.REQ)  # Create a REQ (request) socket
        cls.socket.connect("tcp://localhost:5555")  # Connect to the ZMQ server
        cls.lock = threading.Lock()  # Create a lock for thread safety

    @classmethod
    def tearDownClass(cls):
        # Clean up the socket and context after tests
        cls.socket.close()  # Close the socket
        cls.context.term()  # Terminate the context

    def send_command(self, command):
        # Send a command to the server and receive the response
        with self.lock:  # Ensure thread safety when accessing the socket
            self.socket.send_json(command)  # Send the command as JSON
            return self.socket.recv_json()  # Receive the response as JSON

    def client_thread(self, command, results, index):
        # A helper method to run a command in a thread
        response = self.send_command(command)  # Send the command and get the response
        results[index] = response  # Store the response in the results list at the given index

    def test_concurrent_requests(self):
        # Define a list of commands to test
        commands = [
            {"type": "math", "operation": "add", "a": 5, "b": 3},
            {"type": "math", "operation": "subtract", "a": 10, "b": 4},
            {"type": "math", "operation": "multiply", "a": 6, "b": 7},
            {"type": "math", "operation": "divide", "a": 15, "b": 3},
            {"type": "os", "command": "echo Hello World"},
            {"type": "os", "command": "ipconfig"},
            {"type": "os", "command": "arp -a"},
        ]

        # Expected results corresponding to the commands
        expected_results = [
            {"status": "success", "result": 8},
            {"status": "success", "result": 6},
            {"status": "success", "result": 42},
            {"status": "success", "result": 5},
            {"status": "success", "result": "Hello World\n"},  # Adjust based on your environment
        ]

        threads = []  # List to hold thread references
        results = [None] * len(commands)  # List to store results

        # Start a thread for each command
        for index, command in enumerate(commands):
            thread = threading.Thread(target=self.client_thread, args=(command, results, index))
            threads.append(thread)  # Add the thread to the list
            thread.start()  # Start the thread

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        # Verify that the results match the expected results
        for result, expected in zip(results, expected_results):
            self.assertEqual(result, expected)  # Check if each result matches the expected value


if __name__ == "__main__":
    unittest.main()  # Run the unit tests
