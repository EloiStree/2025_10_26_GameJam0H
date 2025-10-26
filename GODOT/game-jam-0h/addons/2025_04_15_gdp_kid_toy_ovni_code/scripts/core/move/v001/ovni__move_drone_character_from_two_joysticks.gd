extends CharacterBody3D

var joystick_left: Vector2 = Vector2.ZERO
var joystick_right: Vector2 = Vector2.ZERO

@export var move_speed: float = 5.0
@export var rotation_speed: float = 270
@export var vertical_speed: float = 3.0


func set_drone_joysticks(joystick_left_up_rotation: Vector2, joystick_right_move: Vector2) -> void:
	joystick_left = joystick_left_up_rotation
	joystick_right = joystick_right_move
	# print("Test received " + str(joystick_left) + " " + str(joystick_right))

func _physics_process(delta: float) -> void:
	rotate_y(-joystick_left.x * deg_to_rad(rotation_speed) * delta)
	var new_velocity: Vector3 = Vector3.ZERO
	new_velocity.y = joystick_left.y * vertical_speed
	var direction = (transform.basis.x * joystick_right.x) - (transform.basis.z * joystick_right.y)
	if direction.length() > 0.01:
		direction = direction.normalized()
		new_velocity.x = direction.x * move_speed
		new_velocity.z = direction.z * move_speed

	velocity = new_velocity
	move_and_slide()
