def connect():
    import socket
    import sys
    
    # Create a socket object
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Define server address and port
    server_address = ('localhost', 9999)
    
    try:
        # Connect to the server
        sock.connect(server_address)
        print(f"Connected to {server_address}")
        
        # Send a message
        message = "Hello, Server!"
        sock.sendall(message.encode())
        
        # Receive response
        data = sock.recv(1024)
        print(f"Received: {data.decode()}")
        
    except ConnectionRefusedError:
        print(f"Failed to connect to {server_address}")
        sys.exit(1)
    finally:
        # Close the socket
        sock.close()