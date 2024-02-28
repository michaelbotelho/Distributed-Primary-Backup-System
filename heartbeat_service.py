import grpc
import heartbeat_service_pb2
import heartbeat_service_pb2_grpc
import google.protobuf.empty_pb2

from concurrent import futures
from datetime import datetime 
from datetime import timedelta
import time


SERVICES = {}

class HeartbeatServerServicer(heartbeat_service_pb2_grpc.ViewServiceServicer): # ISSUE WITH HANDLING TIMER
     def Heartbeat(self, request, context):
        service_id = request.service_identifier
        SERVICES[service_id] = datetime.now().time()
        
        with open("logs/heartbeat.txt", "a") as f:
            f.write(f"{service_id} is alive. Latest heartbeat received at[{SERVICES[service_id]}]")
        
        # Start a counter for service_id and append alive message to log
        # If service_id sends heartbeat again within 5 sec
            #reset the timer for service_id
            #append alive message to log
        # Else
            #append down message to log
            
            while datetime.now().time() + timedelta(0,5) >= SERVICES[service_id]:
                pass
            
            if datetime.now().time() + timedelta(0,5) >= SERVICES[service_id]:
                f.write(f"{service_id} might be down. Latest heartbeat received at[{SERVICES[service_id]}]")
        

def serve():
    """
    Initializes and starts the gRPC server.

    Returns:
        grpc.Server: The initialized gRPC server.
    """
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
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