class grid:
    BLOCK_SIZE = 50         # Number of pixels per block, for when viewing game locally
    WIDTH = 13              # Number of building windows wide
    HEIGHT = 6              # Number of building windows high

class artnet:
    TARGET = '2.0.0.1'      # Specify the IP of Art-Net node (TODO: Do we auto configure the last octet based on building floor?)
    BROADCAST = False       # We can send Art-Net data via network broadcast (i.e. target 255.255.255.255)
    UNIVERSE = 0            # Specify our Art-Net universe (TODO: Do we auto configure this base on 1x node per building floor)
    PACKET_SIZE = 300       # We can be more efficient by sending minimum data - Number of lights per floor (universe) * 3 (RGB channels)

class colour:
    SNAKE = (0, 255, 0)
    FOOD = (255, 0, 0)
    BACKGROUND = (0, 0, 100)
    SCORE = (255, 255, 255)

class misc:
    SPEED = 5               # Game play speed... 1=slow, 10=fast
