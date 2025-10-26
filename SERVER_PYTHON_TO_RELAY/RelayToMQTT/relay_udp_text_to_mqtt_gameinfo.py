MQTT_BROKER = "192.168.0.136"
MQTT_PORT = 1883
MQTT_TOPIC_IMPORT_CODE = "read_only/code_to_run"
MQTT_TOPIC_RECOVERT_GAME_INFO = "read_only/game_information"

listen_game_computer_ip = "127.0.0.1"
listen_game_computer_port = 4615

import socket
import time
# pip install paho-mqtt --break-system-packages
import paho.mqtt.client as mqtt

BUFFER_SIZE = 65535  # max UDP packet size to read

def connect_mqtt():
    """Connect to MQTT broker with error handling"""
    try:
        mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
        mqtt_client.loop_start()  # Start background thread for MQTT
        return mqtt_client
    except Exception as e:
        print(f"MQTT connection error: {e}")
        return None

def ensure_mqtt_connection(mqtt_client):
    """Ensure MQTT connection is active, reconnect if needed"""
    if mqtt_client is None or not mqtt_client.is_connected():
        print("Reconnecting to MQTT...")
        if mqtt_client:
            mqtt_client.loop_stop()
            mqtt_client.disconnect()
        return connect_mqtt()
    return mqtt_client
                   
def listen_udp_and_relay():
    mqtt_client = None  # Initialize mqtt_client
    udp_socket = None
    
    while True:
        try:
            mqtt_client = ensure_mqtt_connection(mqtt_client)
            
            # Create UDP socket
            udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            udp_socket.bind((listen_game_computer_ip, listen_game_computer_port))
            
            print(f"Listening on UDP {listen_game_computer_ip}:{listen_game_computer_port}")
            
            while True:
                try:
                    # Receive UDP data
                    data, addr = udp_socket.recvfrom(BUFFER_SIZE)
                    
                    # Convert bytes to UTF-8 text
                    text_message = data.decode('utf-8')
                    
                    print(f"Received from {addr}: {text_message}")
                    
                    # Ensure MQTT connection and publish
                    mqtt_client = ensure_mqtt_connection(mqtt_client)
                    if mqtt_client:
                        mqtt_client.publish(MQTT_TOPIC_RECOVERT_GAME_INFO, text_message)

                except UnicodeDecodeError:
                    print(f"Failed to decode message from {addr}")
                except Exception as e:
                    print(f"Error receiving data: {e}")
                    break  # Break inner loop to reconnect
                    
        except Exception as e:
            print(f"Socket error: {e}. Reconnecting...")
            if udp_socket:
                try:
                    udp_socket.close()
                except:
                    pass
            # Wait a bit before reconnecting
            time.sleep(1)

if __name__ == "__main__":
    listen_udp_and_relay()
    