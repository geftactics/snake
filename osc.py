from pythonosc.udp_client import SimpleUDPClient

osc_ip = "2.0.0.100"

client = SimpleUDPClient(osc_ip, 8010)
client.send_message("/cues/selected/cues/by_cell/col_28/row_1", 1)

# client.send_message("/some/address", [1, 2., "hello"])  # Send message with int, float and string