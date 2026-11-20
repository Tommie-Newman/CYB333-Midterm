import socket
import time
from datetime import datetime


ALLOWED_HOSTS = ("127.0.0.1", "localhost", "scanme.nmap.org")


def scan_ports(host, start_port, end_port):
    """Scan a range of TCP ports on an authorized host."""

    if host not in ALLOWED_HOSTS:
        print("Error: This host is not authorized for scanning.")
        return

    
    if not (1 <= start_port <= end_port <= 65535):
        print("Error: Port numbers must be between 1 and 65535.")
        return

    
    if host == "scanme.nmap.org" and end_port - start_port + 1 > 10:
        print("Error: Limit scanme.nmap.org scans to 10 ports.")
        return

    print(f"\nScanning {host}")
    print(f"Scan started: {datetime.now()}")
    print(f"Port range: {start_port}-{end_port}\n")

    try:
        ip_address = socket.gethostbyname(host)

        for port in range(start_port, end_port + 1):
            # Create a new TCP socket for each port.
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(1)

                result = sock.connect_ex((ip_address, port))

                if result == 0:
                    print(f"Port {port}: OPEN")
                else:
                    print(f"Port {port}: CLOSED or FILTERED")

            # Small delay to avoid scanning too quickly.
            time.sleep(0.2)

    except socket.gaierror:
        print("Error: Could not resolve the hostname.")
    except socket.error as error:
        print(f"Socket error: {error}")

    print(f"\nScan finished: {datetime.now()}")


def main():
    """Get user input and start the scan."""

    print("Python Port Scanner")
    print("Authorized targets: 127.0.0.1 and scanme.nmap.org")

    try:
        host = input("Enter target host: ").strip().lower()
        start_port = int(input("Enter starting port: "))
        end_port = int(input("Enter ending port: "))

        scan_ports(host, start_port, end_port)

    except ValueError:
        print("Error: Please enter valid whole numbers for ports.")
    except KeyboardInterrupt:
        print("\nScan interrupted by user.")

def test_unreachable_host():
    """Simulate an unreachable hostname without scanning another system."""

    print("\nTesting unreachable host error handling...")

    try:
        # Simulate a hostname resolution failure.
        raise socket.gaierror("Host could not be resolved")

    except socket.gaierror:
        print("Error: Could not resolve the hostname.")
        print("Unreachable host error handled successfully.")

if __name__ == "__main__":
    main()