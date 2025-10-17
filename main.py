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

# Cube Vertices
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

# Edges
edges = [
    (0, 1), (1, 2), (2, 3), (3, 0),  # Back face
    (4, 5), (5, 6), (6, 7), (7, 4),  # Front face
    (0, 4), (1, 5), (2, 6), (3, 7)   # Connections
]

"""Functions"""

def calc_focal_length(d, fov):
    fov_rad = np.radians(fov)
    return (d / 2) / np.tan(fov_rad / 2)

def project_point(point, focal, width, height):
    x, y, z = point

    # Denominator, Can't Be 0
    if z <= 0:
        return None

    x_proj = (focal * x) / z
    y_proj = (focal * y) / z

    u = width / 2 + x_proj
    v = height / 2 - y_proj

    return np.array([u, v])

def project_points(points, foc, width, height):
    total = []

    for p in points:
        proj = project_point(p, foc, width, height)
        total.append(proj)

    return total

"""Initial Setup"""
f = calc_focal_length(WIDTH, 60)
obj_pos = np.array([0, 0, 20])
obj_speed = 0.1

"""Runtime Loop"""
while True:

    # Exit
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()

    # Input
    keys = pg.key.get_pressed()
    if keys[pg.K_w]:
        obj_pos[2] -= obj_speed

    screen.fill(BLACK)

    # Move
    world_vertices = vertices + obj_pos

    # Project Object
    proj_vertices = project_points(world_vertices, f, WIDTH, HEIGHT)

    # Draw Edges, If Points Are Correct
    for start, end in edges:
        p1 = proj_vertices[start]
        p2 = proj_vertices[end]

        if p1 is not None and p2 is not None:
            pg.draw.line(screen, WHITE, p1, p2, 2)

    pg.display.flip()
    clock.tick(60)
