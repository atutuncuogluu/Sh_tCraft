from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from PIL import Image  # For loading the texture image
from Blocks import *
import pygame
import random

forest_positions = []  # Ağaçların sabit konumlarını saklamak için liste
cactus_positions = []  # Kaktüslerin sabit konumalrını saklamak için liste

wood_positions = []
leaf_positions = []

def init_biome_positions():
    global forest_positions
    global cactus_positions
    forest_positions = [(random.randint(0, 45), random.randint(-45, 45)) for _ in range(20)]
    cactus_positions = [(random.randint(-45, -5), random.randint(-45, 45)) for _ in range(10)]

def draw_sand_ground():
    glBindTexture(GL_TEXTURE_2D, 6)
    glBegin(GL_QUADS)
    for x in range(-50, 0, 10):
        for z in range(-50, 51, 10):
            y1 = 0  # Set a fixed height for the ground
            y2 = 0  # Set a fixed height for the ground
            glTexCoord2f(0.0, 0.0)
            glVertex3f(x, y1, z)
            glTexCoord2f(1.0, 0.0)
            glVertex3f(x + 10, y2, z)
            glTexCoord2f(1.0, 1.0)
            glVertex3f(x + 10, y2, z + 10)
            glTexCoord2f(0.0, 1.0)
            glVertex3f(x, y1, z + 10)
    glEnd()
    glBindTexture(GL_TEXTURE_2D, 0)  # Texture binding'i sıfırla
    glColor3f(1.0, 1.0, 1.0)  # Çimen rengi diğer renklerle karışmasın

def draw_ground():
    glBindTexture(GL_TEXTURE_2D, 7)
    glBegin(GL_QUADS)
    for x in range(0, 50, 10):
        for z in range(-50, 51, 10):
            y1 = 0  # Set a fixed height for the ground
            y2 = 0  # Set a fixed height for the ground
            glTexCoord2f(0.0, 0.0)
            glVertex3f(x, y1, z)
            glTexCoord2f(1.0, 0.0)
            glVertex3f(x + 10, y2, z)
            glTexCoord2f(1.0, 1.0)
            glVertex3f(x + 10, y2, z + 10)
            glTexCoord2f(0.0, 1.0)
            glVertex3f(x, y1, z + 10)
    glEnd()
    glBindTexture(GL_TEXTURE_2D, 0)  # Texture binding'i sıfırla
    glColor3f(1.0, 1.0, 1.0)  # Çimen rengi diğer renklerle karışmasın

def draw_tree(x, z):
    local_wood_positions = [
        (x, 0, z),
        (x, 1, z),
        (x, 2, z),
        (x, 3, z),
        (x, 4, z)
    ]
    for pos in local_wood_positions:
        glPushMatrix()
        glTranslatef(*pos)
        glScalef(1, 1, 1)
        cube(4)  # all coordinates defined in Blocks file
        glPopMatrix()

    local_leaf_positions = [
        (x+1, 2, z+2), (x, 2, z+2), (x-1, 2, z+2),
        (x+2, 2, z+1), (x+1, 2, z+1), (x, 2, z+1), (x-1, 2, z+1), (x-2, 2, z+1),
        (x+2, 2, z), (x+1, 2, z), (x-1, 2, z), (x-2, 2, z),
        (x+2, 2, z-1), (x+1, 2, z-1), (x, 2, z-1), (x-1, 2, z-1), (x-2, 2, z-1),
        (x+1, 2, z-2), (x, 2, z-2), (x-1, 2, z-2),
        (x+1, 3, z+2), (x, 3, z+2), (x-1, 3, z+2),
        (x+2, 3, z+1), (x+1, 3, z+1), (x, 3, z+1), (x-1, 3, z+1), (x-2, 3, z+1),
        (x+2, 3, z), (x+1, 3, z), (x-1, 3, z), (x-2, 3, z),
        (x+2, 3, z-1), (x+1, 3, z-1), (x, 3, z-1), (x-1, 3, z-1), (x-2, 3, z-1),
        (x+1, 3, z-2), (x, 3, z-2), (x-1, 3, z-2),
        (x, 4, z+1),
        (x+1, 4, z), (x-1, 4, z),
        (x, 4, z-1),
        (x, 5, z+1),
        (x+1, 5, z), (x, 5, z), (x-1, 5, z),
        (x, 5, z-1),
    ]
    for pos in local_leaf_positions:
        glPushMatrix()
        glTranslatef(*pos)
        glScalef(1, 1, 1)
        cube(1)  # all coordinates defined in Blocks file
        glPopMatrix()

    return local_leaf_positions, local_wood_positions

def draw_cactus(x, z):
    cactus_positions = [
        (x, 0, z),
        (x, 1, z),
        (x, 2, z)
    ]
    for pos in cactus_positions:
        glPushMatrix()
        glTranslatef(*pos)
        glScalef(1, 1, 1)
        cube(3)
        glPopMatrix()

def draw_forest():
    global forest_positions
    global cactus_positions
    global leaf_positions
    global wood_positions

    all_leaf_positions = []
    all_wood_positions = []

    for x, z in forest_positions:
        local_leaf_positions, local_wood_positions = draw_tree(x, z)
        all_leaf_positions.extend(local_leaf_positions)
        all_wood_positions.extend(local_wood_positions)

    for x, z in cactus_positions:
        draw_cactus(x, z)

    leaf_positions = all_leaf_positions
    wood_positions = all_wood_positions

    return leaf_positions, wood_positions
