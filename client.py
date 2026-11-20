"""Simple TCP client that sends messages to a local echo server."""

import socket

HOST = "127.0.0.1"
PORT = 5000
BUFFER_SIZE = 1024


def main():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.settimeout(5)
            print(f"Connecting to {HOST}:{PORT}...", flush=True)
            client_socket.connect((HOST, PORT))
            print("Connected to server!", flush=True)

            while True:
                message = input("Enter a message (or 'quit' to exit): ")
                # Newline marks the end of each message in this simple protocol.
                client_socket.sendall((message + "\n").encode("utf-8"))
                response = client_socket.recv(BUFFER_SIZE)
                if not response:
                    print("Server closed the connection.", flush=True)
                    break
                print(f"Server response: {response.decode('utf-8', errors='replace').strip()}", flush=True)
                if message.lower() == "quit":
                    print("Disconnected cleanly.", flush=True)
                    break

    except ConnectionRefusedError:
        print("Connection failed: server is not running or is refusing connections.", flush=True)
    except socket.timeout:
        print("Connection timed out or server did not respond.", flush=True)
    except (ConnectionResetError, BrokenPipeError):
        print("Connection was unexpectedly closed.", flush=True)
    except OSError as error:
        print(f"Client socket error: {error}", flush=True)
    except (KeyboardInterrupt, EOFError):
        print("\nClient stopped by user.", flush=True)
    finally:
        print("Client shut down.", flush=True)


if __name__ == "__main__":
    main()
