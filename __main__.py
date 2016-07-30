import socket

import numpy as np
from math import cos
from math import sin
import curses


shift_delta = 0.0001
rotate_delta = np.math.pi / 10
my_point = np.array([shift_delta, 0, 1])
identity = np.array([[1, 0, 0],
                     [0, 1, 0],
                     [0, 0, 1]])


def rotate_matrix(a):
    return np.array([[cos(a), -sin(a), 0],
                     [sin(a), cos(a), 0],
                     [0, 0, 1]])


def shift_matrix(x, y):
    return np.array([[1, 0, x],
                     [0, 1, y],
                     [0, 0, 1]])


def get_transform(key):
    if key == curses.KEY_UP: return shift_matrix(shift_delta, 0)
    if key == curses.KEY_DOWN: return shift_matrix(-shift_delta, 0)
    if key == curses.KEY_LEFT: return rotate_matrix(rotate_delta)
    if key == curses.KEY_RIGHT: return rotate_matrix(-rotate_delta)

    return identity


def main(stdscr, lat, lon):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    transform = shift_matrix(lon, lat)

    while True:
        key = stdscr.getch()
        transform = transform.dot(get_transform(key))
        point = transform.dot(my_point)
        msg = str(point[1]) + "," + str(point[0])
        sock.sendto(msg.encode(), ("192.168.43.1", 12345))
        # stdscr.addstr(msg)



if __name__ == "__main__":
    # lat = 59.934720
    # lon = 30.324828
    lat = 36.016204
    lon = -114.737325
    curses.wrapper(main, lat, lon)
    pass
