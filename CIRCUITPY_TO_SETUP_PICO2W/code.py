import time
import wifi
import socketpool
import adafruit_minimqtt.adafruit_minimqtt as MQTT
from board_led import BoardLED
import sys
from adafruit_httpserver import Server, Request, Response, POST, GET


from player_main_code import received_byte_game_information
from player_main_code import received_text_game_information
from player_main_code import update_code
import os
import microcontroller

import adafruit_ntp
import rtc


# --------------


def read_boot_out():
    """Read and return the contents of boot_out.txt file"""
    try:
        with open("boot_out.txt", "r") as f:
            boot_content = f.read()
        print("Boot output:")
        print(boot_content)
        return boot_content
    except OSError:
        print("boot_out.txt not found or cannot be read")
        return None

# Call the method
read_boot_out()


# --------------


player_code_path_file = "player_main_code.py"
player_code_default_path_file = "player_main_code_default.txt"

def override_or_create_player_code(new_code:str):
    """Override or create the player code file with new code"""
    try:
        with open(player_code_path_file, "w") as f:
            f.write(new_code)
        print(f"Player code {'overridden' if os.path.exists(player_code_path_file) else 'created'} in {player_code_path_file}")
    except OSError as e:
        print(f"Error writing to {player_code_path_file}: {e}")

def reset_player_code_to_default():
    """Reset the player code file to default code"""
    try:
        with open(player_code_default_path_file, "r") as default_file:
            default_code = default_file.read()
        with open(player_code_path_file, "w") as player_file:
            player_file.write(default_code)
        print(f"Player code reset to default in {player_code_path_file}")
    except OSError as e:
        print(f"Error resetting player code to default: {e}")

# --------------

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

NTP_SERVER = os.getenv('NTP_SERVER', '192.168.0.136')

# Update variables for WiFi connection
SSID = WIFI_SSID
PASSWORD = WIFI_PASSWORD



PLAYER_MAIN_CODE_PATH =os.getenv('PLAYER_MAIN_CODE_PATH', 'PICO_W2')

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

s = pool.socket()
s.bind(("", 8080))
s.listen(1)
print("Listening on", wifi.radio.ipv4_address, ":8080")
# ========= HTTP UPLOAD CODE ========
server = Server(pool, "/static")

# Simple GET route (status page)
@server.route("/", GET)
def home(request: Request):
    html = """
    <html>
        <body>
            <h2>Pico W Update Server</h2>
            <form action="/upload" method="post" enctype="text/plain">
                <textarea name="filedata" rows="10" cols="40"></textarea><br>
                <button type="submit">Upload</button>
            </form>
        </body>
    </html>
    """
    return Response(request, html, content_type="text/html")


# Check player file code 
@server.route("/check_player_code", GET)
def check_player_code(request: Request):
    try:
        with open(player_code_path_file, "r") as f:
            code = f.read()
        return Response(request, code, content_type="text/plain")
    except Exception as e:
        return Response(request, f"Error: {e}\n", status=500)

# POST route to replace the main file
@server.route("/upload", POST)
def upload(request: Request):
    try:
        # Read POST body
        data = request.body.decode("utf-8")
        print(f"Received {len(data)} bytes")

        # Write to file
        override_or_create_player_code(data)

        return Response(request, "File updated successfully.\n")
    except Exception as e:
        return Response(request, f"Error: {e}\n", status=500)

# Start server on all interfaces
server.start("0.0.0.0")
print(f"Server running at http://{wifi.radio.ipv4_address}:8080")



# ======== NTP Time Synchronization ========

print("Querying NTP server: ", NTP_SERVER)
ntp = adafruit_ntp.NTP(pool, server=NTP_SERVER, tz_offset=0)  # UTC

# ======== Get NTP Time with nanosecond precision ========
ntp_unix_ns = ntp.utc_ns  # returns nanoseconds since epoch
ntp_unix = ntp_unix_ns / 1_000_000_000  # convert to seconds with decimal precision

# ======== Get Local Device Time with millisecond precision ========
local_unix = time.monotonic()  # seconds since boot

# ======== Calculate Difference with millisecond precision ========
difference_ms = (ntp_unix - local_unix) * 1000
print("NTP time (UTC):", time.localtime(int(ntp_unix)))
print("Local monotonic time:", local_unix, "seconds since boot")
print("Time difference:", f"{difference_ms:.3f}", "ms")

# ======== Optionally Set RTC to NTP Time ========
ntp_time = time.localtime(int(ntp_unix))
rtc.RTC().datetime = ntp_time
print("RTC updated with NTP time.")







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

print("> Connecting to MQTT broker:", MQTT_BROKER)
print("  Client name:", MQTT_YOUR_CLIENT_NAME_WITH_IP)
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
            server.poll()
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