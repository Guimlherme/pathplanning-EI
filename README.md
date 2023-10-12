# Mini autonomous car

This is the project for a mini autonomous car that follows a line via camera. It was made to work on a Raspberry Pi.

It has 3 main parts:

- Control: wheels control based on modern control theory;
- Decision making: finds the best routes for a given map;
- Perception: calculates the state and position of the car.

The `server.py` must be run on the Raspberry Pi, and the `client.py` must be run in a computer that is connected to the same WiFi network as the server.
