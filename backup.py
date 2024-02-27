import grpc
import replication_pb2
import replication_pb2_grpc

from concurrent import futures
from datetime import datetime


DICT = {}

class PrimaryServerServicer(replication_pb2_grpc.SequenceServicer):
    def Write(self, request, context): 
        try:
            # Receive write request
            key, value = request.key, request.value
            
            # Apply write if key is unique in backup.txt   
            if not key in DICT:             #NOT PROPERLY HANDLING DUPLICATE ENTRIES
                # Add to log   
                with open("logs/backup.txt", "a") as f:
                    f.write(key + " " + value + "\n")
                    f.close()
                # Add to dictionary 
                DICT[key] = value
                
                # Send ack (WriteResponse) back to primary
                return replication_pb2.WriteResponse(ack="true")
            else:
                return replication_pb2.WriteResponse(ack="false")
            
        except Exception as e:
            print(f"Error performing Write. {e}")
            

def dict_init():
    """
    Instantiates dictionary with entries from the log.
    """
    with open("logs/backup.txt", "r") as f:
        for line in f:
            key, value = line.split()
            DICT[key] = value


def serve():
    """
    Initializes and starts the gRPC server.

    Returns:
        grpc.Server: The initialized gRPC server.
    """
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    replication_pb2_grpc.add_SequenceServicer_to_server(PrimaryServerServicer(), server)
    server.add_insecure_port('[::]:50052')
    return server


if __name__ == '__main__':
    try:
        dict_init() # Read in entries from backup.txt
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