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
