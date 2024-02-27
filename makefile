compile:
	python -m grpc_tools.protoc -I. --python_out=. --pyi_out=. --grpc_python_out=. heartbeat_service.proto
	python -m grpc_tools.protoc -I. --python_out=. --pyi_out=. --grpc_python_out=. replication.proto