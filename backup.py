import grpc
import replication_pb2
import replication_pb2_grpc
import heartbeat_service_pb2
import heartbeat_service_pb2_grpc

from concurrent import futures
from datetime import datetime
from time import sleep


# Initialize a thread pool, one thread designated to heartbeats, two threads for incoming requests
EXECUTOR = futures.ThreadPoolExecutor(max_workers=3)

class PrimaryServerServicer(replication_pb2_grpc.SequenceServicer):
    def Write(self, request, context): 
        """
        Handles a write request by writing to a log file and sending an acknowledgment response.

        Args:
            request (replication_pb2.WriteRequest): The write request message.
            context (grpc.ServicerContext): The context for the RPC call.

        Returns:
            replication_pb2.WriteResponse: The acknowledgment response message.
        """
        try:
            # Receive write request
            key, value = request.key, request.value
            
            # Apply write to log file   
            with open("logs/backup.txt", "a") as f:
                f.write(key + " " + value + "\n")
                f.close()
                # Send ack (WriteResponse) back to primary
                return replication_pb2.WriteResponse(ack="true")   
            
        except Exception as e:
            print(f"Error performing Write. {e}")
            return replication_pb2.WriteResponse(ack="false")   


def heartbeat():
    """
    Sends a heartbeat every 5 seconds to ViewServer at port 50053
    """
    while True:
        with grpc.insecure_channel('localhost:50053') as channel:
            stub = heartbeat_service_pb2_grpc.ViewServiceStub(channel)
            # Send heartbeat to ViewServer
            stub.Heartbeat(heartbeat_service_pb2.HeartbeatRequest(service_identifier="Backup"))

        sleep(5)
        
        
def serve():
    """
    Initializes and starts the gRPC server.

    Returns:
        grpc.Server: The initialized gRPC server.
    """
    server = grpc.server(EXECUTOR)
    replication_pb2_grpc.add_SequenceServicer_to_server(PrimaryServerServicer(), server)
    server.add_insecure_port('[::]:50052')
    
    return server


if __name__ == '__main__':
    try:
        server = serve()
        server.start()
        print(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")} Server Started...')
        print(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")} Kill with keyboard interrupt (Ctrl+C)')
        EXECUTOR.submit(heartbeat())
        server.wait_for_termination()
        
    except KeyboardInterrupt:
        server.stop(0)
        exit(0)
    except:
        print(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")} An error occurred initiating the server')
        exit(0)