import socket


def check_connectivity(timeout=3):

    try:
        socket.setdefaulttimeout(timeout)
        socket.create_connection(("8.8.8.8", 53))
        return True
    
    except OSError:
        return False
