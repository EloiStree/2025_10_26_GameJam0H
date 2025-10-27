extends Node

@export var resource_path:String = "res://addons/2025_04_15_gdp_kid_toy_ovni_code/scenes/elements/player_ovni_with_code_no_keyboard.tscn"
var element_resource : Resource 
# The node where we’ll put the new instance
@export var spawn_target: Node3D
@export var list_ovni_to_move : Array[Node3D] = []
@export var to_create_element_scene: bool = true

func _ready() -> void:
	if resource_path != "":
		element_resource = load(resource_path)
		

func push_in_gamepad(player_in_list_index: int, gamepad: PlayerGamepadAxisInfo) -> void:
	while list_ovni_to_move.size() <= player_in_list_index:
		
		var created = element_resource.instantiate() as Node3D
		get_tree().current_scene.add_child(created)
		list_ovni_to_move.append(created)
		
	
	var joystick_left = Vector2(gamepad.joystick_left_horizontal, gamepad.joystick_left_vertical)
	var joystick_right = Vector2(gamepad.joystick_right_horizontal, gamepad.joystick_right_vertical)

	# Check if the index exists in the array
	if player_in_list_index >= 0 and player_in_list_index < list_ovni_to_move.size():
		var ovni = list_ovni_to_move[player_in_list_index]
		# If the element exists, try to call a method on it (assuming it has a method to handle joystick inputs)
		if ovni != null and ovni.has_method("set_drone_joysticks"):
			ovni.set_drone_joysticks(joystick_left, joystick_right)
		else:
			print("Error: The object at index ", player_in_list_index, " does not have the 'set_drone_joysticks' method.")
	else:
		print("Error: Invalid player index ", player_in_list_index)
