class grid:
    block_size = 50         # Number of pixels per block, for when viewing game locally
    width = 600             # Number of building windows wide, multiplied by block_size
    height = 600            # Number of building windows high, multiplied by block_size

class artnet:
    target = '2.0.0.1'      # Specify the IP of Art-Net node (TODO: Do we auto configure the last octet based on building floor?)
    broadcast = False       # We can send Art-Net data via network broadcast (i.e. target 255.255.255.255)
    universe = 0            # Specify our Art-Net universe (TODO: Do we auto configure this base on 1x node per building floor)
    packet_size = 300       # We can be more efficient by sending minimum data - Number of lights per floor (universe) * 3 (RGB channels)

class colour:
    snake = (0, 255, 0)
    food = (255, 0, 0)
    background = (0, 0, 100)
    score = (255, 255, 255)

class misc:
    speed = 5               # Game play speed... 1=slow, 10=fast
