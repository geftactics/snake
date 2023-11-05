import hid
import logging
import time
import socket

server_address = ('2.0.0.101', 1234)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

def connect_to_server(server_address):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect(server_address)
        logging.info("Connected to the server.")
        return client_socket
    except socket.error as e:
        logging.error(f"Error connecting to the server: {str(e)}")
        return None

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
    logging.error('Gamepad not connected!!')
    exit()


while True:
    client_socket = connect_to_server(server_address)

    if client_socket:
        while True:
            command = ""
            input = tuple(gamepad.read(64))
            if input != () and input != (1, 128, 128, 127, 127, 15, 0, 0):
                command = key_map.get(input, input)
                if isinstance(command, str):
                    logging.info('Send command: ' + command)
                    client_socket.send(command.encode("utf-8"))

    else:
        logging.warning("Reconnecting to server...")
        time.sleep(2)