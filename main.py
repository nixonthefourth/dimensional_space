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
        return None

    # Calculate
    x_proj = (focal * x) / z
    y_proj = (focal * y) / z

    u = width / 2 + x_proj
    v = height / 2 - y_proj

    return np.array([u, v])

# Multiple Points Projection
def project_points(points, foc, width, height):
    return [project_point(p, foc, width, height) for p in points]

# Initial Setup
f = calc_focal_length(WIDTH, 60)
obj_pos = np.array([0, 0, 5])
cam_pos = np.array([0.0, 0.0, 0.0])
obj_speed = 1
smoothing = 0.08

"""Runtime Loop"""
while True:

    # Exit Sequence
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()

    # Collect Input
    key_input = pg.key.get_pressed()
    if key_input[pg.K_w]:
        obj_pos[2] += obj_speed

    # Make Camera Follow the Object
    desired_cam_pos = obj_pos + np.array([0, 0, -7])
    cam_pos = cam_pos * (1 - smoothing) + desired_cam_pos * smoothing

    screen.fill(BLACK)

    # Cube Calculations
    world_vertices = vertices + obj_pos

    # Transform relative to camera
    camera_vertices = world_vertices  - cam_pos

    proj_vertices = project_points(camera_vertices, f, WIDTH, HEIGHT)

    # Draw Edges
    for a, b in edges:
        p_a = proj_vertices[a]
        p_b = proj_vertices[b]

        if p_a is None or p_b is None:
            continue

        pg.draw.line(screen, WHITE, p_a, p_b, 2)

    # Framerate Update
    pg.display.flip()
    clock.tick(60)
