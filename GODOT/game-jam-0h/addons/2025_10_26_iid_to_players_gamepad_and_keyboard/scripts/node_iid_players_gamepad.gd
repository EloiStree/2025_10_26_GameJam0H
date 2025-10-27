extends Node

@export var player_base: IidToPlayersGamepad

signal on_player_gamepad_updated(player_in_list_index: int, gamepad: PlayerGamepadAxisInfo)

func _ready() -> void:
	player_base = IidToPlayersGamepad.new()

func push_in_index_value_date(index: int, value: int, date: int) -> void:
	print("Index " + str(index))
	print("Value " + str(value))

	var result = player_base.push_in_index_value_date(index, value, date)

	# Check if the result is valid and contains the expected keys
	if result == null or not result.has("player_list_index") or not result.has("gamepad"):
		print(" Hey ?")
		return
	
	var index_in_list: int = result["player_list_index"]
	var gamepad = result["gamepad"]

	print("test " + str(value))

	if index_in_list > -1 and gamepad != null:
		print("Player ", index_in_list, " updated gamepad: LH=", gamepad.joystick_left_horizontal,
			  " LV=", gamepad.joystick_left_vertical, " RH=", gamepad.joystick_right_horizontal,
			  " RV=", gamepad.joystick_right_vertical)
		emit_signal("on_player_gamepad_updated", index_in_list, gamepad)
