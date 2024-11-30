# Dynamic Command Execution: A ZeroMQ and DRF Bridge

This project implements a ZeroMQ server that processes commands sent via a Django REST Framework API. The server can
handle both mathematical operations and OS commands.

## Design Decisions

- **ZeroMQ for Messaging**: ZeroMQ is used for its lightweight, asynchronous messaging capabilities, allowing for
  efficient communication between the API and the command processing logic.

- **Django REST Framework**: The API is built using Django REST Framework, providing a robust and flexible framework for
  creating RESTful APIs. This allows for easy serialization of requests and responses and built-in support for
  authentication and permissions.

- **Basic Authentication**: The API uses Basic Authentication to secure endpoints. Ensure to include valid credentials
  in your requests.

- **Separation of Concerns**: The project separates concerns by having distinct components for the API, command
  processing, and ZeroMQ handling. This modular design enhances maintainability and scalability.

- **Concurrency**: The ZeroMQ server processes commands asynchronously, which allows it to handle multiple requests
  concurrently. This is essential for performance in a multi-user environment.

- **Custom Permissions**: The project includes a custom permission class, `IsStaff`, which restricts access to dangerous
  commands. Only staff members are allowed to execute these commands.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Example Requests](#example-requests)
- [Unit Testing](#unit-testing)
- [Contributing](#contributing)
- [License](#license)

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ThePythonist/ZMQ-DRF-Bridge.git
   cd ZMQ-DRF-Bridge
   ```

2. **Set up a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations (if applicable):**
   ```bash
   python manage.py migrate
   ```

## Usage

1. **Start the ZMQ server:**
   Run the `zmq_server.py` file to start the ZeroMQ server.
   ```bash
   python zmq_server.py
   ```

2. **Start the Django development server:**
   In a separate terminal, start the Django server.
   ```bash
   python manage.py runserver
   ```

3. **Make a POST request to the API:**
   You can use Postman to send commands to the API.

## API Endpoints

- **POST /api/v1/command/**

  Sends a command to the ZeroMQ server.

## Custom Permissions

The project includes a custom permission class, `IsStaff`, which restricts access to potentially dangerous commands.
Only staff members are allowed to execute commands such as `shutdown`, `reboot`, and others defined in
the `dangerous_commands` list. This enhances security by ensuring that only authorized users can perform critical
operations.

## Example Requests

### Math Command

To perform a mathematical addition using Postman:

1. Open Postman and create a new **POST** request.
2. Enter the URL: `http://localhost:8000/api/v1/command/`.
3. In the **Authorization** tab, select **Basic Auth** and enter your credentials.
4. In the **Body** tab, select **raw** and set the format to **JSON**.
5. Enter the following JSON:
   ```json
   {
       "type": "math",
       "operation": "add",
       "a": 5,
       "b": 3
   }
   ```
6. Click **Send**.

**Expected Response:**

```json
{
  "status": "success",
  "result": 8
}
```

### OS Command

To execute an OS command (e.g., `echo`) using Postman:

1. Open Postman and create a new **POST** request.
2. Enter the URL: `http://localhost:8000/api/v1/command/`.
3. In the **Authorization** tab, select **Basic Auth** and enter your credentials.
4. In the **Body** tab, select **raw** and set the format to **JSON**.
5. Enter the following JSON:
   ```json
   {
       "type": "os",
       "command": "echo Hello World"
   }
   ```
6. Click **Send**.

**Expected Response:**

```json
{
  "status": "success",
  "result": "Hello World\n"
}
```

## Unit Testing

To run the unit tests for the ZeroMQ server, use the following command:

```bash
python -m unittest test_server.py
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.