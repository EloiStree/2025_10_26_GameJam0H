import os
import struct
import wifi
import socketpool


class PushIntegerWithUDP:
    """Send integer data over UDP using CircuitPython on a Pico W."""

    def __init__(self):
        self.server_ip = os.getenv("UDP_INPUT_IID_SERVER_IP") or "192.168.1.254"
        self.server_port = int(os.getenv("UDP_INPUT_IID_SERVER_PORT") or 7000)
       
    def set_ip_and_port(self, server_ip: str, server_port: int):
        """Update destination IP and port."""
        self.server_ip = server_ip
        self.server_port = server_port

    def integer_to_bytes(self, value: int):
        """Pack a 32-bit integer into bytes."""
        return struct.pack("<i", value)

    def index_integer_to_bytes(self, index: int, value: int):
        """Pack two 32-bit integers into bytes."""
        return struct.pack("<ii", index, value)

    def index_integer_date_to_bytes(self, index_int32: int, value_int32: int, date_ulong: int):
        """Pack two 32-bit ints and one 64-bit unsigned long into bytes."""
        return struct.pack("<iiQ", index_int32, value_int32, int(date_ulong))

    def push_udp_iid(self, index_int32: int, value_int32: int, date_ulong: int):
        """Send structured data via UDP."""
       

        self.pool = socketpool.SocketPool(wifi.radio)
        self.udp_socket = self.pool.socket(socketpool.SocketPool.AF_INET, socketpool.SocketPool.SOCK_DGRAM)
        message = self.index_integer_date_to_bytes(index_int32, value_int32, date_ulong)
        self.udp_socket.sendto(message, (self.server_ip, self.server_port))
        self.udp_socket.close()
        
