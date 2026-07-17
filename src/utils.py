import math

def find_distance(hand, id1, id2):

    x_distance = hand.landmark[id1].x - hand.landmark[id2].x
    y_distance = hand.landmark[id1].y - hand.landmark[id2].y

    distance = math.sqrt((x_distance ** 2) + (y_distance ** 2))

    return distance