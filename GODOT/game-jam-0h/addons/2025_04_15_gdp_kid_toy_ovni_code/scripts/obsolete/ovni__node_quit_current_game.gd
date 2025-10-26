extends Node

@export var action_name_to_trigger :="quit_game"
# Function to quit the game
func quit_game():
	get_tree().quit()

# Check for input in _input
func _input(event):
	if event.is_action_pressed(action_name_to_trigger):  # Check for the input action
		quit_game()
