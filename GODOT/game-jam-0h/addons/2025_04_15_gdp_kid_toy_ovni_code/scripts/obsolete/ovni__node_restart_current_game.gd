extends Node

@export var action_name_to_trigger :="restart_current_game"

# Function to restart the current game
func restart_game():
	get_tree().reload_current_scene()

# Check for input in _process or _input
func _input(event):
	if event.is_action_pressed(action_name_to_trigger):  # Check for the input action
		restart_game()
