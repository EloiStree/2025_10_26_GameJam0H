import socket
import time

def send_ping():
    broadcast_ip = "127.0.0.1"
    broadcast_port = 4615
    
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                sock.sendto(b"PING", (broadcast_ip, broadcast_port))
                print(f"Broadcasted PING to {broadcast_ip}:{broadcast_port}")
        except Exception as e:
            print(f"Error broadcasting PING: {e}")
        
        time.sleep(5)

if __name__ == "__main__":
    send_ping()