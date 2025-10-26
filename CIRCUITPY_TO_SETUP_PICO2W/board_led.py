import time
import board
import digitalio

# Required CircuitPython libraries (should be in /lib folder on CIRCUITPY):
# - adafruit_bus_device (may be needed for some boards)
# Note: board, digitalio, and time are built-in modules in CircuitPython

class BoardLED:
    def __init__(self):
        # Initialize the built-in LED (usually "board.LED" or "board.D13")
        self.led = digitalio.DigitalInOut(board.LED)
        self.led.direction = digitalio.Direction.OUTPUT

    def on(self):
        """Turn the LED on."""
        self.led.value = True

    def off(self):
        """Turn the LED off."""
        self.led.value = False

    def blink(self, n, stay_on_time=0.5, stay_off_time=0.5, final_state="off"):
        """
        Blink the LED n times with custom on/off durations.
        
        :param n: Number of blinks
        :param stay_on_time: Duration (seconds) the LED stays on per blink
        :param stay_off_time: Duration (seconds) the LED stays off per blink
        :param final_state: 'on' or 'off' — final LED state after blinking
        """
        for _ in range(n):
            self.on()
            time.sleep(stay_on_time)
            self.off()
            time.sleep(stay_off_time)

        # Set final state
        if final_state.lower() == "on":
            self.on()
        else:
            self.off()


# Example usage:
if __name__ == "__main__":
    led = BoardLED()

    # Blink 3 times, LED on for 0.3s, off for 0.2s, ending ON
    led.blink(3, stay_on_time=0.3, stay_off_time=0.2, final_state="on")
