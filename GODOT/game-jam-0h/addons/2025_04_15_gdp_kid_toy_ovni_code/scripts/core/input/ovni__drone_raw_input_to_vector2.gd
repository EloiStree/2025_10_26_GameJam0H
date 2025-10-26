extends Node

# Exposed vectors for other developers to use
@export var joystick_left_vertical_rotate: Vector2 = Vector2.ZERO
@export var joystick_right_move: Vector2 = Vector2.ZERO

# Keys (can be customized per developer if needed)
@export var key_move_forward: Key = KEY_W
@export var key_move_backward: Key = KEY_S
@export var key_move_left: Key = KEY_A
@export var key_move_right: Key = KEY_D
@export var key_move_up: Key = KEY_SPACE
@export var key_move_down: Key = KEY_SHIFT
@export var key_turn_left: Key = KEY_Q
@export var key_turn_right: Key = KEY_E

signal on_input_processed(left_joystick_vertical_rotation: Vector2, right_joystick_move: Vector2)

# Track pressed state manually since InputEvent is instantaneous
var pressed_keys: = {}

func _ready() -> void:
	# Initialize all tracked keys as not pressed
	pressed_keys = {
		key_move_forward: false,
		key_move_backward: false,
		key_move_left: false,
		key_move_right: false,
		key_move_up: false,
		key_move_down: false,
		key_turn_left: false,
		key_turn_right: false,
	}

func _input(event: InputEvent) -> void:
	if event is InputEventKey:
		if event.keycode in pressed_keys:
			pressed_keys[event.keycode] = event.pressed

func _process(_delta: float) -> void:
	_process_input()

func _process_input() -> void:
	joystick_left_vertical_rotate = Vector2.ZERO
	joystick_right_move = Vector2.ZERO

	# Movement (X,Z plane)
	if pressed_keys[key_move_forward]:
		joystick_right_move.y += 1
	if pressed_keys[key_move_backward]:
		joystick_right_move.y -= 1
	if pressed_keys[key_move_left]:
		joystick_right_move.x -= 1
	if pressed_keys[key_move_right]:
		joystick_right_move.x += 1

	# Vertical
	if pressed_keys[key_move_up]:
		joystick_left_vertical_rotate.y += 1
	if pressed_keys[key_move_down]:
		joystick_left_vertical_rotate.y -= 1

	# Turning
	if pressed_keys[key_turn_left]:
		joystick_left_vertical_rotate.x -= 1
	if pressed_keys[key_turn_right]:
		joystick_left_vertical_rotate.x += 1

	on_input_processed.emit(joystick_left_vertical_rotate, joystick_right_move)
