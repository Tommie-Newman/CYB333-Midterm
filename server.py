"""Simple TCP echo server for local socket communication practice."""

import socket

HOST = "127.0.0.1"  # Listen only on this computer.
PORT = 5000
BUFFER_SIZE = 1024


def main():
    try:
        # Context managers automatically close sockets on exit.
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind((HOST, PORT))
            server_socket.listen(1)
            print(f"Server listening on {HOST}:{PORT}", flush=True)

            # Accept one client for this demonstration.
            connection, address = server_socket.accept()
            with connection:
                print(f"Client connected: {address}", flush=True)
                connection.settimeout(30)
                while True:
                    try:
                        data = connection.recv(BUFFER_SIZE)
                    except socket.timeout:
                        print("Client timed out; closing connection.", flush=True)
                        break
                    except ConnectionResetError:
                        print("Client connection was reset.", flush=True)
                        break

                    if not data:  # Empty bytes indicate a closed connection.
                        print("Client disconnected.", flush=True)
                        break

                    message = data.decode("utf-8", errors="replace").strip()
                    print(f"Client says: {message}", flush=True)
                    if message.lower() == "quit":
                        connection.sendall(b"Goodbye!\n")
                        print("Closing client connection gracefully.", flush=True)
                        break

                    response = f"Server received: {message}\n"
                    connection.sendall(response.encode("utf-8"))

    except OSError as error:
        print(f"Server socket error: {error}", flush=True)
    except KeyboardInterrupt:
        print("\nServer interrupted by user.", flush=True)
    finally:
        print("Server shut down.", flush=True)


if __name__ == "__main__":
    main()
