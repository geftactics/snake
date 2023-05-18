from pythonosc.udp_client import SimpleUDPClient

ip = "10.101.0.31"
port = 8010

client = SimpleUDPClient(ip, port)

client.send_message("/medias/Text Generator/assign", 123) 
client.send_message("/medias/Text Generator/Font/Text", "bar")

# client.send_message("/some/address", [1, 2., "hello"])  # Send message with int, float and string