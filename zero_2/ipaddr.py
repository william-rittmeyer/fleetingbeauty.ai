import socket

def get_raspberry_pi_ip():
    # Create a UDP socket to get the IP address of the default route
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect(("8.8.8.8", 80))
    ip_address = sock.getsockname()[0]
    sock.close()

    # Return the IP address
    return ip_address

# Call the function and print the result
print(get_raspberry_pi_ip())


