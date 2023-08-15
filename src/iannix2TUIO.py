from pythonosc import udp_client
from pythonosc import osc_server, dispatcher

ip = "127.0.0.1"
client_port = 9001
server_port = 57120 

client = udp_client.SimpleUDPClient(ip, client_port)


def send_osc(*msg: list):
    # https://www.iannix.org/download/documentation.pdf
    # https://www.tuio.org/?specification
    msg_new = [msg[1], msg[3], msg[4], msg[5], 0, 0, 0, 0]
    client.send_message("/tuio/3Dcur", ["set", *msg_new])


dispatcher = dispatcher.Dispatcher()
dispatcher.map("/cursor", send_osc)

server = osc_server.ThreadingOSCUDPServer((ip, server_port), dispatcher)
server.serve_forever()
