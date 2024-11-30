import datetime
import zmq
import zmq.asyncio
import asyncio
import subprocess
from config.customlogs import make_log, tictoc


# Decorator to log the execution time of a function
@tictoc
async def handle_math(command):
    # Extract the operation from the command
    operation = command['operation']
    # Perform the appropriate math operation
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

    # Return the result of the operation
    return {'status': 'success', 'result': result}


# Decorator to log the execution time of a function
@tictoc
async def handle_os(command):
    # Attempt to execute the OS command
    try:
        result = subprocess.check_output(command['command'], shell=True, text=True)
        return {'status': 'success', 'result': result}
    except subprocess.CalledProcessError:
        return {'status': 'error', 'message': 'Invalid os command'}


# Decorator to log the execution time of a function
@tictoc
async def process_command(command):
    # Process the command based on its type
    try:
        if command['type'] == 'os':
            return await handle_os(command)  # Handle OS command
        elif command['type'] == 'math':
            return await handle_math(command)  # Handle math command
        else:
            return {'status': 'error', 'message': 'Invalid command type'}
    except Exception as e:
        # Log any exceptions that occur and return an error message
        make_log("error", e)
        return {'status': 'error', 'message': str(e)}


async def process_command_and_send_response(socket, command):
    # Process the command and send the response back to the client
    response = await process_command(command)
    await socket.send_json(response)


async def start_zmq_server():
    # Create a ZeroMQ context and a REP (reply) socket
    context = zmq.asyncio.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")  # Bind the socket to a TCP address

    print("Server is running")  # Indicate that the server is ready
    while True:
        # Wait for a command from a client
        data = await socket.recv_json()
        print(f"{datetime.datetime.now()} :::: Received command: {data}")
        make_log("info", f"request for command {data}")

        # Create a task to process the command concurrently
        asyncio.create_task(process_command_and_send_response(socket, data))


if __name__ == "__main__":
    # Set the event loop policy for Windows compatibility
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    # Start the ZMQ server
    asyncio.run(start_zmq_server())
