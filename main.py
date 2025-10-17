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
    [-1, -1, -1],
    [ 1, -1, -1],
    [ 1,  1, -1],
    [-1,  1, -1],
    [-1, -1,  1],
    [ 1, -1,  1],
    [ 1,  1,  1],
    [-1,  1,  1],
], dtype=float)

# Edges between vertices
edges = [
    (0, 1), (1, 2), (2, 3), (3, 0),  # Back
    (4, 5), (5, 6), (6, 7), (7, 4),  # Front
    (0, 4), (1, 5), (2, 6), (3, 7)   # Connect
]

"""Functions"""

'''Focal Length Calculation'''
def calc_focal_length(d, fov):
    fov_rad = np.radians(fov)
    return (d / 2) / np.tan(fov_rad / 2)

'''Project Object'''

# Individual Point Projection
def project_point(point, focal, width, height):
    x, y, z = point


    # z is a denominator
    if z <= 0:
        z = 0.00001

    # Calculate each projected point
    x_proj = (focal * x) / (z + 5)
    y_proj = (focal * y) / (z + 5)

    u = width / 2 + x_proj
    v = height / 2 - y_proj

    return np.array([u, v])

# Multiple Points Projection
def project_points(points, foc, width, height):
    return [project_point(p, foc, width, height) for p in points]

"""Runtime Loop"""
while True:

    # Exit Sequence
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()

    screen.fill(BLACK)

    f = calc_focal_length(WIDTH, 60)
    proj_vertices = project_points(vertices, f, WIDTH, HEIGHT)

    # Draw Edges
    for i in edges:
        start, end = i
        pg.draw.line(screen, WHITE, proj_vertices[start], proj_vertices[end], 2)

    # Framerate Update
    pg.display.flip()
    clock.tick(60)
