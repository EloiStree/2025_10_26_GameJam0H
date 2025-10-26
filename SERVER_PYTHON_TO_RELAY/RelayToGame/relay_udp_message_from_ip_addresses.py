#!/usr/bin/env python3
import socket
import struct

HOST = "0.0.0.0"   # listen on all interfaces (use "::" for IPv6)
PORT = 7000
BUFFER_SIZE = 65535  # max UDP packet size to read
TAG_INDEX =255000

TO_RELAY_SERVER_IP = "127.0.0.1"
TO_RELAY_SERVER_PORT = 3615

socket_to_relay = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket_to_relay.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

bool_use_print = True

def debug_print(message: str):
    """Print debug messages if enabled."""
    if bool_use_print:
        print(message)

def index_integer_date_to_bytes( index_int32: int, value_int32: int, date_ulong: int):
        """Pack two 32-bit ints and one 64-bit unsigned long into bytes."""
        return struct.pack("<iiQ", index_int32, value_int32, int(date_ulong))


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # allow quick reuse of the address after restart (optional)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((HOST, PORT))
    debug_print(f"Listening for UDP on {HOST}:{PORT} ... (Ctrl-C to stop)")

    try:
        while True:
            data, addr = sock.recvfrom(BUFFER_SIZE)  # data is bytes, addr is (ip, port)
            src_ip, src_port = addr
            num_bytes = len(data)
            # print ip:port and number of bytes
            debug_print(f"{src_ip}:{src_port} — {num_bytes} bytes")
            if num_bytes == 16:
                try:
                    index, value, date = struct.unpack("<iiQ", data)
                    debug_print(f"  index: {index}, value: {value}, date: {date}")
                    last_part_of_ipv4 = (date >> 32) & 0xFFFFFFFF
                    src_ip_array = src_ip.split('.')
                    if len(src_ip_array) == 4:
                        player_index = int(src_ip_array[3]) + TAG_INDEX
                        packed_data = index_integer_date_to_bytes(player_index, value, date)
                        socket_to_relay.sendto(packed_data, (TO_RELAY_SERVER_IP, TO_RELAY_SERVER_PORT))

                except struct.error as e:
                    debug_print(f"  Failed to unpack 16 bytes: {e}")

            # if you want to also print the payload (careful with binary data)
            # print("payload:", data)
    except KeyboardInterrupt:
        debug_print("\nStopping listener.")
    finally:
        sock.close()

if __name__ == "__main__":
    main()
