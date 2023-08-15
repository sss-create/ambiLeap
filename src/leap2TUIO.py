import math
import json
from pythonosc import udp_client
from websocket import create_connection

# send data to:
ip = "127.0.0.1"
port = 9001

ws = create_connection("ws://127.0.0.1:6437/v6.json")
ws.send(json.dumps({"background": True}))
ws.send(json.dumps({"enableGestures": True}))
client = udp_client.SimpleUDPClient(ip, port)

# [(x_min, x_max), (y_min, y_max), (z_min, z_max)]
box_ranges = [(-200, 200), (25, 480), (-200, 200)]

""" EXAMPLE RESPONSE
{'currentFrameRate': 27.958,
 'devices': [],
 'gestures': [],
 'hands': [],
 'id': 1749,
 'interactionBox': {'center': [0.0, 200.0, 0.0], 'size': [235.247, 235.247, 147.751]},
 'pointables': [],
 'r': [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]],
 's': 1.0,
 't': [0.0, 0.0, 0.0],
 'timestamp': 1650652100788880}
"""


def process_hands(hand: dict, queue: list = []) -> list:
    # 'queue' to calculate acceleration based on previous position
    hand_id = hand_to_id(hand.get("type"))
    positions = scale_xyz(hand.get("palmPosition"), box_ranges)
    velocity = scale_capital_xyz(hand.get("palmVelocity"), box_ranges)
    motion_acceleration = calculate_acceleration(to_scalar(velocity), queue)
    return [hand_id, *positions, *velocity, motion_acceleration]


def process_pointables(hand: dict, pointables: dict, queue: list = []) -> list:
    # pointable "type": 0=thumb, 4=pinky
    # building id: hand{1,2} ++ pointable{0..4}
    # eg.: left index finger is 11, right thumb is 20
    # 'queue' to calculate acceleration based on previous position
    pointable_id = int(f"{hand_to_id(hand.get('type'))}{pointables.get('type')}")
    positions = scale_xyz(pointables.get("tipPosition"), box_ranges)
    velocity = scale_capital_xyz(pointables.get("tipVelocity"), box_ranges)
    motion_acceleration = calculate_acceleration(to_scalar(velocity), queue)
    return [pointable_id, *positions, *velocity, motion_acceleration]


def process_gestures(gestures: dict) -> str:
    return gestures.get("type")


def hand_to_id(hand: str) -> int:
	return 1 if hand is "left" else 2


def to_scalar(velocities: list) -> float:
    return math.sqrt(sum([pow(i, 2) for i in velocities]))


def calculate_acceleration(speed: float, queue: list) -> float:
    # velocity in mm/s
    queue.append(speed)
    if len(queue) == 2:
        delta = queue[1] - queue[0]
        queue.pop(0)
        return delta
    else:
        return 0


def scale_xyz(xyz: list, ranges: list) -> list:
    # https://www.sciencedirect.com/topics/computer-science/max-normalization
    # https://developer-archive.leapmotion.com/documentation/v2/python/devguide/Leap_Coordinate_Mapping.html
    normalized = map(lambda i, n: (i - n[0])/(n[1] - n[0]), xyz, ranges)
    return reorder_xyz([min(max(i, 0), 1) for i in normalized])


def scale_capital_xyz(capital_xyz: list, ranges: list) -> list:
    normalized = map(lambda i, n: i/(n[1] - n[0]), capital_xyz, ranges)
    return reorder_xyz([min(max(i, 0), 1) for i in normalized])


def reorder_xyz(xyz: list) -> list:
    # Leap Motion has a different order of x, y, z than TUIO does
    return [xyz[0], xyz[2], xyz[1]]


def send_3dcur(msg: list):
    # https://www.tuio.org/?specification
    # /tuio/3Dcur set s x y z X Y Z m
    client.send_message("/tuio/3Dcur", ["set", *msg])


def send_gesture(msg: str):
    # custom tuio message
    client.send_message("/tuio/_sP", ["set", msg])


while True:
    # https://developer-archive.leapmotion.com/documentation/python/supplements/Leap_JSON.html
    response = json.loads(ws.recv())
    response_hands = response.get("hands")
    response_pointables = response.get("pointables")
    response_gesture = response.get("gestures")

    # check for number of hands, then process and send data
    if response_hands:
        send_3dcur(process_hands(response_hands[0]))
        send_3dcur(process_pointables(response_hands[0], response_pointables[0]))
        if len(response_hands) == 2:
            send_3dcur(process_hands(response_hands[1]))
            send_3dcur(process_pointables(response_hands[1], response_pointables[1]))
            # gestures working with two hands for better control
            if response_gesture:
                send_gesture(process_gestures(response_gesture[0]))
