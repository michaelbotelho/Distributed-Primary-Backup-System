import grpc 
import replication_pb2
import replication_pb2_grpc


def run():
    """
    Executes a gRPC request and send it to a server.
    """
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = replication_pb2_grpc.SequenceStub(channel)
        
        response = stub.Write(replication_pb2.WriteRequest(key="1",value="hello"))
        print(response.ack)
        
        

if __name__ == '__main__':
    try:
        run()
    except:
        exit(0)