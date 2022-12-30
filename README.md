# Snake

Figuring out a way to drive a giant nokia snake game on a building!

snake.py is the game - for now it dumps .dat files into the `mock-lights` dir...

app.py in mock-lights picks up the dat files and renders them onto the building using openCV.

Will probably use MQTT or REST-API later - Need to decide how to drive lights first!