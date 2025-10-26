import subprocess
import os


# List of script names to launch (without .py extension)
scripts = [
    "RelayToGame/relay_udp_message_from_ip_addresses",
    "RelayToMQTT/ping_loop_relay",
    "RelayToMQTT/relay_udp_text_to_mqtt_gameinfo"
]

# Get the directory of the current script
base_dir = os.path.dirname(os.path.abspath(__file__))

# Launch each script in a new terminal window on the Pi
processes = []
for script in scripts:
    script_path = os.path.join(base_dir, f"{script}.py")
    if os.path.exists(script_path):
        # Use LXTerminal (common on Raspberry Pi OS) to launch the script
        p = subprocess.Popen([
            "lxterminal", "--command", f"python3 '{script_path}'"
        ])
        processes.append(p)
    else:
        print(f"Script not found: {script_path}")

# Optionally, wait for all processes to finish
for p in processes:
    p.wait()