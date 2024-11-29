import zmq
import zmq.asyncio
import asyncio
import subprocess
from config.customlogs import make_log, tictoc


@tictoc
async def handle_math(command):
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
async def handle_os(command):
    try:
        result = subprocess.check_output(command['command'], shell=True, text=True)
        return {'status': 'success', 'result': result}
    except subprocess.CalledProcessError:
        return {'status': 'error', 'message': 'Invalid os command'}


@tictoc
async def process_command(command):
    try:
        if command['type'] == 'os':
            return await handle_os(command)
        elif command['type'] == 'math':
            return await handle_math(command)
        else:
            return {'status': 'error', 'message': 'Invalid command type'}

    except Exception as e:
        make_log("error", e)
        return {'status': 'error', 'message': str(e)}


async def start_zmq_server():
    context = zmq.asyncio.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")

    print("Server is running")
    while True:
        data = await socket.recv_json()
        print(f"Received command: {data}")
        make_log("info", f"request for command {data}")
        response = await process_command(data)
        await socket.send_json(response)


if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(start_zmq_server())
