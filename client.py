import grpc 
import replication_pb2
import replication_pb2_grpc


def run():
    """
    Executes a gRPC request and send it to a server.
    """
    try:
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = replication_pb2_grpc.SequenceStub(channel)
            
            # Prompt user for input before calling Write
            key = input("Please enter the key (q to quit): ")
            if key == "q":
                exit(1) 
            value = input("Please enter the value: ")
            
            # Log write to client.txt
            with open("logs/client.txt", "a") as f:
                f.write(key + " " + value + "\n")
                f.close()
            
            # Send write request to primary server
            response = stub.Write(replication_pb2.WriteRequest(key=key,value=value))
            
        # Loop program        
        run()
        
    except:
        exit(1)
          

if __name__ == '__main__':
    try:
        run()
            
    except:
        exit(0)