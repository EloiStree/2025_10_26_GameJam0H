import time
import wifi
import socketpool
import adafruit_minimqtt.adafruit_minimqtt as MQTT
from board_led import BoardLED
import sys


from player_main_code import received_game_information
from player_main_code import update_code
import os
import microcontroller

def push_game_information_to_player_code(text:str):
    # player code is in the folder player_code_folder/player_main_code.py
    received_game_information(text)


last_time_pushed = time.monotonic()
def push_execute_time_to_player_code():
    global last_time_pushed
    current_time = time.monotonic()
    delta_in_seconds = current_time - last_time_pushed
    last_time_pushed = current_time

    # player code is in the folder player_code_folder/player_main_code.py
    time_to_sleep_in = update_code(delta_in_seconds)
    time.sleep(time_to_sleep_in)
    

# ---------------------------
print("Hello World")
# Print system information
print(f"Platform: {sys.platform}")
print(f"Python version: {sys.version}")


# Wi-Fi credentials
WIFI_SSID = os.getenv('WIFI_SSID', 'OfflineCodeTournament2G')
WIFI_PASSWORD = os.getenv('WIFI_PASSWORD', '12345678')

# UDP server info
UDP_INPUT_IID_SERVER_IP = os.getenv('UDP_INPUT_IID_SERVER_IP', '192.168.0.136')
UDP_INPUT_IID_SERVER_PORT = int(os.getenv('UDP_INPUT_IID_SERVER_PORT', '7000'))

# MQTT broker info
MQTT_BROKER = os.getenv('MQTT_BROKER', '192.168.0.136')
MQTT_PORT = int(os.getenv('MQTT_PORT', '1883'))
MQTT_TOPIC_IMPORT_CODE = os.getenv('MQTT_TOPIC_IMPORT_CODE', 'read_only/code_to_run')
MQTT_TOPIC_RECOVERT_GAME_INFO = os.getenv('MQTT_TOPIC_RECOVERT_GAME_INFO', 'read_only/game_information')
MQTT_YOUR_CLIENT_NAME = os.getenv('MQTT_YOUR_CLIENT_NAME', 'PICO_W2')

# Update variables for WiFi connection
SSID = WIFI_SSID
PASSWORD = WIFI_PASSWORD


device_unique_id = microcontroller.cpu.uid
MQTT_YOUR_CLIENT_NAME_WITH_IP = device_unique_id.hex() + "_" + MQTT_YOUR_CLIENT_NAME

led = BoardLED()


def turn_led_on():
    global led
    led.on()

def turn_led_off():
    global led
    led.off()

def check_pi_on_with_board_led():
    global led

    # Example 1: Turn on the LED
    led.on()
    time.sleep(1)

    # Example 2: Turn it off
    led.off()
    time.sleep(1)

    # Example 3: Blink it 5 times, with custom timing, ending ON
    led.blink(5, stay_on_time=0.2, stay_off_time=0.3, final_state="on")

    # Example 4: Leave it off at the end
    led.blink(3, stay_on_time=0.5, stay_off_time=0.5, final_state="off")


def connect_to_wifi():
    print("> Connecting to Wi-Fi...")
    wifi.radio.connect(SSID, PASSWORD)
    print("< Connected with IP:", wifi.radio.ipv4_address)
    return wifi.radio.ipv4_address

def mqtt_message(client, topic, message):
    print("Received message on topic {}: {}".format(topic, message))
    push_game_information_to_player_code(message)
    # Echo the device IP back on the same topic
    #client.publish(topic, str(ip_address))

def print_current_network_info():
    print("Network information:")
    print("  SSID:", wifi.radio.ssid)
    print("  IP Address:", wifi.radio.ipv4_address)
    print("  Subnet Mask:", wifi.radio.ipv4_subnet_mask)
    print("  Gateway:", wifi.radio.ipv4_gateway)
    print("  DNS:", wifi.radio.ipv4_dns_servers)

# Connect to Wi-Fi and get IP address
ip_address = connect_to_wifi()

# Create a socket pool for network connections
pool = socketpool.SocketPool(wifi.radio)

# Initialize MQTT client
mqtt_client = MQTT.MQTT(
    broker=MQTT_BROKER,
    port=MQTT_PORT,
    client_id=MQTT_YOUR_CLIENT_NAME_WITH_IP,
    socket_pool=pool,
)



check_pi_on_with_board_led()

# Set callback for incoming messages
mqtt_client.on_message = mqtt_message

print("> Connecting to MQTT broker...")
mqtt_client.connect()
print("< Connected to MQTT broker...")

print("> Subscribing to topic:", MQTT_TOPIC_RECOVERT_GAME_INFO)
mqtt_client.subscribe(MQTT_TOPIC_RECOVERT_GAME_INFO)
print("< Subscribed to topic.")


try:
    while True:
        try:
            turn_led_on()
            mqtt_client.loop()
            push_execute_time_to_player_code()
            time.sleep(0.001)
        except (OSError, MQTT.MMQTTException) as e:
            turn_led_off()
            print(f"MQTT error: {e}")
            print("Attempting to reconnect...")
            try:
                mqtt_client.disconnect()
            except:
                pass
            time.sleep(5)
            try:
                mqtt_client.connect()
                mqtt_client.subscribe(MQTT_TOPIC_RECOVERT_GAME_INFO)
                print("Reconnected to MQTT broker")
            except Exception as reconnect_error:
                print(f"Failed to reconnect: {reconnect_error}")
                time.sleep(10)
except KeyboardInterrupt:
    print("Exiting...")