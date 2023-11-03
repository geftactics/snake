import hid
import time
import socket

def connect_to_server(server_address):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect(server_address)
        print("Connected to the server.")
        return client_socket
    except socket.error as e:
        print(f"Error connecting to the server: {str(e)}")
        return None
    
server_address = ('127.0.0.1', 1234)  # Replace with the actual server address and port
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Init NES Gamepad
try:
    gamepad = hid.device()
    gamepad.open(0x0810, 0xe501)
    gamepad.set_nonblocking(True)
    key_map = {
        (1, 128, 128, 127, 127, 47,  0, 0): 'a',
        (1, 128, 128, 127, 127, 31,  0, 0): 'b',
        (1, 128, 128, 127,   0, 15,  0, 0): 'up',
        (1, 128, 128, 127, 255, 15,  0, 0): 'down',
        (1, 128, 128, 0,   127, 15,  0, 0): 'left',
        (1, 128, 128, 255, 127, 15,  0, 0): 'right',
        (1, 128, 128, 127, 127, 15, 32, 0): 'space', # start
        (1, 128, 128, 127, 127, 15, 16, 0): 'select', # select
    }
except Exception as e:
    gamepad = None





while True:
    # Attempt to connect to the server
    client_socket = connect_to_server(server_address)

    if client_socket:
        while True:
            command = ""
            # Get a command from the user
            input = tuple(gamepad.read(64))
            if input != () and input != (1, 128, 128, 127, 127, 15, 0, 0):
                print(key_map.get(input, input))
                command = key_map.get(input, input)
            
            # Send the command to the server
            client_socket.send(command.encode("utf-8"))

    else:
        # Wait for a few seconds before attempting to reconnect
        print("Reconnecting in 5 seconds...")
        time.sleep(5)
