class_name IidToPlayersGamepad
extends Resource

@export var players_gamepad_list: Array[PlayerGamepadAxisInfo] = []

func parse_99_to_percent11(value_99: int) -> float:
	if value_99 == 0:
		return 0.0
	# Force float division
	var percent: float = float(value_99 * -1) / 98.0
	return percent

func push_in_index_value_date(index: int, value: int, date: int) -> Dictionary:
	# Use float() or // (floor division) explicitly where appropriate
	var tag: int = int(value / 100000000.0) # Tag is integer-based
	if tag != 18:
		
		return {"player_list_index": -1, "gamepad": null}

	var axis: int = value % 100000000

	var left_horizontal_99: int = int(int(axis / 1000000.0) % 100)
	var left_vertical_99: int = int(int(axis / 10000.0) % 100)
	var right_horizontal_99: int = int(int(axis / 100.0) % 100)
	var right_vertical_99: int = int(int(axis) % 100)

	var left_horizontal_percent11: float = parse_99_to_percent11(left_horizontal_99)
	var left_vertical_percent11: float = parse_99_to_percent11(left_vertical_99)
	var right_horizontal_percent11: float = parse_99_to_percent11(right_horizontal_99)
	var right_vertical_percent11: float = parse_99_to_percent11(right_vertical_99)

	var new_player: PlayerGamepadAxisInfo = null
	var player_list_index: int = 0

	for player in players_gamepad_list:
		if player.player_index == index:
			new_player = player
			break
		player_list_index += 1

	if new_player == null:
		new_player = PlayerGamepadAxisInfo.new()
		new_player.player_index = index
		players_gamepad_list.append(new_player)
		player_list_index = players_gamepad_list.size() - 1

	new_player.joystick_left_horizontal = left_horizontal_percent11
	new_player.joystick_left_vertical = left_vertical_percent11
	new_player.joystick_right_horizontal = right_horizontal_percent11
	new_player.joystick_right_vertical = right_vertical_percent11

	return {
		"player_list_index": player_list_index,
		"gamepad": new_player
	}
