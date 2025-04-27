# mini-rag

This is a minimal implementation of the RAG model for question answering

## Requirements

- Python 3.9 or later

### Install Python using MiniConda

1) Download and install MiniConda from [Here](#).
2) Create a new environment using the following command:
```bash
$ conda create -n mini-rag-app python=3.8
```
3) Activate the environment:
```bash
$ conda activate mini-rag-app
```

## Dependencies installation
To install the required dependencies, use the following command:

```bash
$ pip install -r requirements.txt
```

## Run the server
To run the application, use the following command:

```bash
$ uvicorn main:app --reload --host 0.0.0.0 --port 5000
```

- **`--reload`**: Enables auto-reloading of the server when you make changes to the code (useful for development).

- **`--host 0.0.0.0`**: Allows the server to be accessible from any IP address.

- **`--port 8000`**: Specifies the port on which the server will run. You can change this to any available port (e.g., 8000, 8080, etc.).

## Access the Application
Once the server is running, you can access the application by opening your browser and navigating to:

```cpp
http://<your-ip>:8000
```
If you are running the server locally, use `http://127.0.0.1:8000`.