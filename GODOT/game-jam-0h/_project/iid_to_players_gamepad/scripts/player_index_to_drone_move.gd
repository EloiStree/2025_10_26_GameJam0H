extends Node

@export var list_ovni_to_move: Array[Node3D] = []

func push_in_gamepad(player_in_list_index: int, gamepad: PlayerGamepadAxisInfo) -> void:
	var joystick_left = Vector2(gamepad.joystick_left_horizontal, gamepad.joystick_left_vertical)
	var joystick_right = Vector2(gamepad.joystick_right_horizontal, gamepad.joystick_right_vertical)
	print("A")
	# Check if the index exists in the array
	if player_in_list_index >= 0 and player_in_list_index < list_ovni_to_move.size():
		var ovni = list_ovni_to_move[player_in_list_index]
		print("B")		
		# If the element exists, try to call a method on it (assuming it has a method to handle joystick inputs)
		if ovni.has_method("set_drone_joysticks"):
			ovni.set_drone_joysticks(joystick_left, joystick_right)
		else:
			print("Error: The object at index ", player_in_list_index, " does not have the 'set_drone_joysticks' method.")
	else:
		print("Error: Invalid player index ", player_in_list_index)


func _on_node_iid_to_players_gamepad_on_player_gamepad_updated(player_in_list_index: int, gamepad: PlayerGamepadAxisInfo) -> void:
	pass # Replace with function body.
