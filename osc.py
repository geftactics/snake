from pythonosc.udp_client import SimpleUDPClient
import time

osc_ip = "2.0.0.100"

client = SimpleUDPClient(osc_ip, 8010)


client.send_message("/medias/number_29.png/assign_to_all_surfaces", 1)
client.send_message("/fixtures/All/visible", 1)



# client.send_message("/some/address", [1, 2., "hello"])  # Send message with int, float and string

# osc_address = "/madmapper/surface/{}/load_image".format(surface_index)
# client.send_message(osc_address, image_path)