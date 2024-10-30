import socket
import ssl

def start_vpn_server(host='127.0.0.1', port=8080):
    # Create SSL context and load certificate and key
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    try:
        context.load_cert_chain(certfile="server.crt", keyfile="server.key")
    except FileNotFoundError:
        print("Error: SSL certificate or key not found.")
        return

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((host, port))
        sock.listen(5)
        print(f"VPN server listening on {host}:{port}")

        with context.wrap_socket(sock, server_side=True) as ssock:
            while True:
                try:
                    conn, addr = ssock.accept()
                    print(f"Connected by {addr}")
                    data = conn.recv(1024)
                    if data:
                        print("Received:", data.decode())
                        conn.sendall(b"Data received securely by VPN server.")
                except Exception as e:
                    print(f"Error during client communication: {e}")
                finally:
                    conn.close()

def connect_to_vpn_server(host='127.0.0.1', port=8080):
    context = ssl.create_default_context()
    context.check_hostname = True  # Enforce hostname check for production
    context.verify_mode = ssl.CERT_REQUIRED  # Require certificate verification
    # Load a trusted CA certificate (e.g., context.load_verify_locations('path/to/ca-bundle.crt'))

    try:
        with socket.create_connection((host, port)) as sock:
            with context.wrap_socket(sock, server_hostname=host) as ssock:
                ssock.sendall(b"Hello, VPN Server!")
                data = ssock.recv(1024)
                print("Received:", data.decode())
    except Exception as e:
        print(f"Error connecting to server: {e}")

