"""Imports"""
import pygame as pg
import sys
import numpy as np

'''Constants'''
BLACK, WHITE = (0, 0, 0), (242, 240, 239)
WIDTH, HEIGHT = 800, 600

"""PyGame Setup"""
pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('Dimensional Space')
clock = pg.time.Clock()

"""Models"""

'''Simple Cube'''

# Vertices
vertices = np.array([
    (-1, 1, -1), # V1
    (1, 1, -1), # V2
    (-1, -1, -1), # V3
    (1, -1, 1), # V4

    (-1, 1, 1), # V5
    (1, 1, 1), # V6
    (-1, -1, 1), # V7
    (1, -1, 1) # V8
])

# Edges
edges = np.array([
    (0, 1), (1, 3), (3, 2), (3, 0), # Rear
    (0, 4), (4, 6), (6, 2), # West
    (4, 5), (5, 7), (7, 6), # Front
    (5, 1), (1, 3), (3, 7) # East
])

"""Functions"""

'''Focal Length Calculation'''
def calc_focal_length(d, fov):
    f = (d * np.arctan(np.radians(fov) / 2)) / 2
    return f

'''Project Object'''

# Individual Point Projection
def project_point(point, f, width, height):
    x, y, z = point

    # Principal Points
    c_x, c_y = width / 2, height / 2

    # z can't mathematically be 0
    if z <= 0:
        z = 0.00001

    # Calculate each projected point
    x_proj = (f * x) / z + c_x
    y_proj = (f * y) / z + c_y

    return np.array([x_proj, y_proj])

# Multiple Points Projection
def project_points(points, f, width, height):
    proj_points = []

    for i in points:
        x_proj, y_proj = project_point(i, f, width, height)

        u = width / 2 + x_proj
        v = height / 2 - y_proj

        proj_points.append(np.array([u, v]))

    return proj_points

"""Runtime Loop"""
while True:

    # Exit Sequence
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()

    screen.fill(BLACK)

    # Framerate Update
    pg.display.flip()
    clock.tick(60)

# Shuts Down Engine
pg.quit()
sys.exit()
