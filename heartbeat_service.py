import grpc
import heartbeat_service_pb2
import heartbeat_service_pb2_grpc
import google.protobuf.empty_pb2

from concurrent import futures
from threading import Timer
from datetime import datetime 
from datetime import timedelta


# Initialize a thread pool with 2 threads per heartbeat call to concurrently log heartbeat and start a timer
EXECUTOR = futures.ThreadPoolExecutor(max_workers=4)
# Declare an empty dictionary to hold services sending heartbeats
SERVICES = {}

class HeartbeatServerServicer(heartbeat_service_pb2_grpc.ViewServiceServicer): 
    def Heartbeat(self, request, context):
        """
        Handles a heartbeat request by updating the service information and starting a timer for the next heartbeat.

        Args:
            request (heartbeat_service_pb2.HeartbeatRequest): The heartbeat request message.
            context (grpc.ServicerContext): The context for the RPC call.

        Returns:
            google.protobuf.empty_pb2.Empty: An empty response message.
        """
        # Log when heartbeat is received
        EXECUTOR.submit(updateService(request.service_identifier))
        # Time until next heartbeat
        EXECUTOR.submit(startTimer(request.service_identifier))
        
        return google.protobuf.empty_pb2.Empty()
         
    
        
def updateService(service_id):
    """
    Updates the service information in the SERVICES dictionary with the latest heartbeat time.

    Args:
        service_id (str): The identifier of the service sending the heartbeat.
    """
    SERVICES[service_id] = datetime.now()
    
    with open("logs/heartbeat.txt", "a") as f:
        f.write(f"{service_id} is alive. Latest heartbeat received at[{SERVICES[service_id]}]\n")


def timerFinished(service_id):
    """
    Checks if the service has not sent a heartbeat in 15 seconds and logs a message if needed.

    Args:
        service_id (str): The identifier of the service being monitored.
    """
    # When timer ends, Write message to log if service has not sent a heartbeat in 3 heartbeat cycles 
    # If service updates while timer is running, SERVICES[service_id] will be updated and message will not be logged
    if datetime.now() >= SERVICES[service_id] + timedelta(0,15):
        with open("logs/heartbeat.txt", "a") as f:
            f.write(f"{service_id} might be down. Latest heartbeat received at[{SERVICES[service_id]}]\n")       
    

def startTimer(service_id):
    """
    Starts a timer for monitoring the heartbeat of a service.

    Args:
        service_id (str): The identifier of the service to monitor.
    """
    timer = Timer(15, timerFinished, args=(service_id,))
    timer.start()

    

def serve():
    """
    Initializes and starts the gRPC server.

    Returns:
        grpc.Server: The initialized gRPC server.
    """
    server = grpc.server(EXECUTOR)
    heartbeat_service_pb2_grpc.add_ViewServiceServicer_to_server(HeartbeatServerServicer(), server)
    server.add_insecure_port('[::]:50053')
    return server



if __name__ == '__main__':
    try:
        server = serve()
        server.start()
        print(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")} Server Started...')
        print(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")} Kill with keyboard interrupt (Ctrl+C)')
        server.wait_for_termination()
        
    except KeyboardInterrupt:
        server.stop(0)
        exit(0)
    except:
        print(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")} An error occurred initiating the server')
        exit(0)