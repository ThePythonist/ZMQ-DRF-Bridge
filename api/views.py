from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import zmq
from .customlogs import make_log, tictoc


class CommandView(APIView):
    # log the runtime
    @tictoc
    def post(self, request):
        command = request.data
        context = zmq.Context()
        socket = context.socket(zmq.REQ)
        socket.connect("tcp://localhost:5555")

        # Forward the incoming request to zmq
        socket.send_json(command)

        # Ask for the reply
        response = socket.recv_json()

        # Ensure the response is formatted correctly
        if response:
            return Response(response, status=status.HTTP_200_OK)
        else:
            error = "No response from server"
            make_log("error", error)
            return Response({"error": error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
