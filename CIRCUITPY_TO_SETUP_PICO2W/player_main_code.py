# Test on your own server 
"""
mosquitto_pub -h 127.0.0.1 -t read_only/game_information -m "Hello World"
"""

import random
from push_iid_with_udp import PushIntegerWithUDP
push_integer = PushIntegerWithUDP()


string_last_received_game_information = ""  

def received_game_information(text:str):
    global string_last_received_game_information
    string_last_received_game_information = text
    print("Received game information:")
    print(text)
    print("Hey! This is the player main code running!")
    if text== "PING":
        push_integer.push_udp_iid(0,0,0)

update_counter=0

def percent_minus1_to_1_to_value99(percent:float) -> int:
    if percent == 0.0:
        return 50
    # Convert from -1 to 1 range to 0 to 1 range
    normalized = (percent + 1.0) / 2.0
    # Convert to 1-99 range
    value99 = int(1 + normalized * 98.0)
    #print (f"Converted percent {percent} to value99 {value99}")
    return value99

def create_player_gamepad_axis_value(joystick_left_horizontal:float, joystick_left_vertical:float, joystick_right_horizontal:float, joystick_right_vertical:float) -> int:


    value = 1800000000 
    value += percent_minus1_to_1_to_value99(joystick_left_horizontal) * 1000000
    value += percent_minus1_to_1_to_value99(joystick_left_vertical) * 10000
    value += percent_minus1_to_1_to_value99(joystick_right_horizontal) * 100
    value += percent_minus1_to_1_to_value99(joystick_right_vertical)
    return int(value)

def get_random_percent11() -> float:
    return (random.randint(-100, 100)) / 100.0

def update_code(delta_in_seconds:float) -> float:
    print("Updating player code...")
    print(f"Last: {string_last_received_game_information}")
    global update_counter
    update_counter += 1

    random_axis_left_horizontal = get_random_percent11()
    random_axis_left_vertical = get_random_percent11()
    random_axis_right_horizontal = get_random_percent11()
    random_axis_right_vertical = get_random_percent11()
    gamepad_joystick_as_int = create_player_gamepad_axis_value(
        random_axis_left_horizontal,
        random_axis_left_vertical,
        random_axis_right_horizontal,
        random_axis_right_vertical
    )

    # print (f"Sending gamepad joystick value: {gamepad_joystick_as_int}")
    # # display random joystick values
    # print(f"Random joystick values:")
    # print(f"Left Horizontal: {random_axis_left_horizontal}")
    # print(f"Left Vertical: {random_axis_left_vertical}")
    # print(f"Right Horizontal: {random_axis_right_horizontal}")
    # print(f"Right Vertical: {random_axis_right_vertical}")
    push_integer.push_udp_iid(0,gamepad_joystick_as_int,0)
    #push_integer.push_udp_iid(0,90000 + update_counter,0)
    return 1    