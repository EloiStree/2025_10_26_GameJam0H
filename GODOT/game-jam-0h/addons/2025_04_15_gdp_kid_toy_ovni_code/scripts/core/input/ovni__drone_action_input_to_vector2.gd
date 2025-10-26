extends Node

# Exposed vectors for other developers to use
@export var joystick_left_vertical_rotate: Vector2 = Vector2.ZERO
@export var  joystick_right_move: Vector2 = Vector2.ZERO

@export var  drone_move_forward: String = "drone_move_forward"
@export var  drone_move_backward: String = "drone_move_backward"
@export var  drone_move_left: String = "drone_move_left"
@export var  drone_move_right: String = "drone_move_right"
@export var  drone_move_up: String = "drone_move_up"
@export var  drone_move_down: String = "drone_move_down"
@export var  drone_turn_left: String = "drone_turn_left"
@export var  drone_turn_right: String = "drone_turn_right"



signal on_input_processed(left_joystick_vertical_rotation:Vector2, right_joystick_move:Vector2)

func _process(_delta: float) -> void:
	_process_input()

func _process_input() -> void:
	# Reset inputs
	joystick_left_vertical_rotate = Vector2.ZERO
	joystick_right_move = Vector2.ZERO
	
	# Movement inputs (X,Z plane)
	if Input.is_action_pressed(drone_move_forward):
		joystick_right_move.y += 1
	if Input.is_action_pressed(drone_move_backward):
		joystick_right_move.y -= 1
	if Input.is_action_pressed(drone_move_left):
		joystick_right_move.x -= 1
	if Input.is_action_pressed(drone_move_right):
		joystick_right_move.x += 1

	# Vertical movement
	if Input.is_action_pressed(drone_move_up):
		joystick_left_vertical_rotate.y += 1
	if Input.is_action_pressed(drone_move_down):
		joystick_left_vertical_rotate.y -= 1

	# Look / Turn inputs
	if Input.is_action_pressed(drone_turn_left):
		joystick_left_vertical_rotate.x -= 1
	if Input.is_action_pressed(drone_turn_right):
		joystick_left_vertical_rotate.x += 1
	on_input_processed.emit(joystick_left_vertical_rotate, joystick_right_move)
	# print("Test" +str(joystick_left_vertical_rotate) + " "+str(joystick_right_move))
	
