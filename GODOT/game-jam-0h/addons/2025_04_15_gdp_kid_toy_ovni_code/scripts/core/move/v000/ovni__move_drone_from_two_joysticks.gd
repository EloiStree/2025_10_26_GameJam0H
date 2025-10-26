extends Node

var joystick_left: Vector2 = Vector2.ZERO
var joystick_right: Vector2 = Vector2.ZERO

@export var what_node_to_affect: Node3D
@export var move_speed: float = 5.0
@export var rotation_speed: float = 2.0
@export var vertical_speed: float = 3.0

func set_drone_joysticks(joystick_left_up_rotation: Vector2, joystick_right_move: Vector2) -> void:
	joystick_left = joystick_left_up_rotation
	joystick_right = joystick_right_move
	# print("Test received " + str(joystick_left) + " " + str(joystick_right))

func _physics_process(delta: float) -> void:
	if not what_node_to_affect:
		return

	# --- Rotation (yaw, left stick X) ---
	what_node_to_affect.rotate_y(-joystick_left.x * deg_to_rad( rotation_speed) * delta)
	what_node_to_affect.translate(Vector3(0, joystick_left.y * vertical_speed * delta, 0) )
	what_node_to_affect.position += what_node_to_affect.basis.x* joystick_right.x * move_speed * delta
	what_node_to_affect.position -= what_node_to_affect.basis.z* joystick_right.y * move_speed * delta
