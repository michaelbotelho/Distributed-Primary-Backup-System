# Distributed-Primary-Backup-System
 A Distributed system follwing a Primary-Backup model using a View server with Heartbeats to maintain avalibility. This project is a concept/practice and leverages Google's gRPC Framework.  

## Preview
https://github.com/michaelbotelho/Distributed-Primary-Backup-System/assets/55448553/debeb934-785f-4962-85aa-60fe87364e6e

## Tech Stack
 * <a href='https://grpc.io/' target="_blank"><img alt='gRPC' src='https://img.shields.io/badge/gRPC-100000?style=for-the-badge&logo=gRPC&logoColor=244C5A&labelColor=244C5A&color=244C5A'/></a>


# Getting Started
## Installation
 1. Install Python 3.7 or newer (https://www.python.org/downloads/)
 2. Ensure pip is installed ```pip --version```
 3. Navigate to the installed folder
 4. Create a virtual environment ```python3 -m venv [venv_name]```
 5. Activate the environment ```[venv_name]\Scripts\activate.bat```
 6. Install requirements ```pip install -r requirements.txt```

## Usage
 - Run a view server ```python3 heartbeat_service.py```
 - Run a server ```python3 primary.py```
 - Run a backup server ```python3 backup.py```
 - Run a client ```python3 client.py```
 - Follow prompts in terminal
