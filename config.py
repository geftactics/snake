class grid:
    BLOCK_SIZE = 100       # Number of pixels per block, for when viewing game locally
    WIDTH = 1000           # Number of building windows wide, multiplied by block_size
    HEIGHT = 500           # Number of building windows high, multiplied by block_size

class artnet:
    TARGET = '255.255.255.255'      # Specify the IP of Art-Net node
    BROADCAST = True                # We can send Art-Net data via network broadcast (i.e. target is 255.255.255.255)
    UNIVERSE_BASE = 21              # Specify our Art-Net universe base, each floor is +1 added to this
    PACKET_SIZE = 512               # We can be more efficient by sending minimum data - Number of lights per floor (universe) * 3 (RGB channels)

class colour:
    SNAKE = (0, 255, 0)
    FOOD = (255, 0, 0)
    BACKGROUND = (0, 0, 0)
    SCORE = (255, 255, 255)

class misc:
    SPEED = 2               # Game play speed... 1=slow, 10=fast