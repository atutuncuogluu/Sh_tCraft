from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from PIL import Image  # For loading the texture image
from Biome import *
import numpy as np
import pygame
import random

# Kamera değişkenleri
gravity = 0.05  # Normal yerçekimi
jump_gravity = 0.07  # Zıplama yerçekimi
ground_level = 1.5
jump_strength = 0.4
camera_pos = np.array([0.0, 10.0, 30.0])
camera_front = np.array([0.0, 0.0, -1.0])
camera_up = np.array([0.0, 1.0, 0.0])
yaw = -90.0
pitch = 0.0
sensitivity = 0.1
speed = 0.5
lastX, lastY = 400, 300
mouse_left_pressed = False
mouse_right_pressed = False
is_jumping = False
jump_velocity = 0.0

# Sahne için bloklar
blocks = {}


# Global variables
texture_id = None
block_textures = {}
selected_texture = 0

leaf_positions = []
wood_positions = []
def init():
    global   texture_id
    glClearColor(0.5, 0.8, 1.0, 1.0)  # Gökyüzü rengi
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)  # Enable 2D texturing

    pygame.mixer.init()
    place_sound = pygame.mixer.Sound("place_block.wav")
    break_sound = pygame.mixer.Sound("break_block.wav")
    init_biome_positions()
    
    

    # Texture'ları yükle
    load_block_textures()


def load_block_textures():
    global block_textures
    # Örnek texture'ları yükle
    block_textures[0] = load_texture("leaves.png")  # 240x240
    block_textures[1] = load_texture("dirt.png")  # 240x240
    block_textures[2] = load_texture("cactus.png")  # 240x240
    block_textures[3] = load_texture("wood.png")  # 240x240
    block_textures[4] = load_texture("brick.png")  # 240x240
    block_textures[5] = load_texture("sand.png")  # 240x240
    block_textures[6] = load_texture("grass_top.png")  # 240x240



def load_texture(filename):
    image = Image.open(filename)
    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    image_data = image.convert("RGBA").tobytes()
    width, height = image.size

    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    return texture_id


def display():
    global timer_id
    global leaf_positions
    global wood_positions
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Kamera konumu
    gluLookAt(camera_pos[0], camera_pos[1], camera_pos[2],
              camera_pos[0] + camera_front[0], camera_pos[1] + camera_front[1], camera_pos[2] + camera_front[2],
              camera_up[0], camera_up[1], camera_up[2])

    # Zemini çiz
    draw_ground()

    # Zemini çiz
    draw_sand_ground()

    # Doku bağlamasını sıfırla
    glBindTexture(GL_TEXTURE_2D, 0)

    # Ağaçları çiz
    leaf_positions, wood_positions = draw_forest()
    

    

    # Doku bağlamasını sıfırla
    glBindTexture(GL_TEXTURE_2D, 0)

    # Blokları çiz
    draw_blocks()

    # Crosshair'ı çiz
    draw_crosshair()

    # Ekranı güncellediğimizde timer_id değişkenini kontrol ederek zaman geçişini sağlarız
    current_time = glutGet(GLUT_ELAPSED_TIME)
    elapsed_time = current_time - timer_id
    # if elapsed_time < (1000 // 30):
    #     return  # 60 FPS'den fazla güncelleme yapma
    if elapsed_time < (1000 // 75):
        return  # 60 FPS'den fazla güncelleme yapma

    glutSwapBuffers()
    timer_id = current_time  # Timer'ı güncelle



def draw_cube(x, y, z, size=1, texture=None):
    if texture:
        glBindTexture(GL_TEXTURE_2D, texture)
    else:
        glBindTexture(GL_TEXTURE_2D, texture_id)  # Varsayılan texture

    glBegin(GL_QUADS)

    # Ön yüz
    glTexCoord2f(0.0, 0.0)
    glVertex3f(x, y, z)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(x + size, y, z)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(x + size, y + size, z)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(x, y + size, z)

    # Arka yüz
    glTexCoord2f(0.0, 0.0)
    glVertex3f(x, y, z + size)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(x + size, y, z + size)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(x + size, y + size, z + size)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(x, y + size, z + size)

    # Sol yüz
    glTexCoord2f(0.0, 0.0)
    glVertex3f(x, y, z)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(x, y, z + size)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(x, y + size, z + size)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(x, y + size, z)

    # Sağ yüz
    glTexCoord2f(0.0, 0.0)
    glVertex3f(x + size, y, z)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(x + size, y, z + size)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(x + size, y + size, z + size)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(x + size, y + size, z)

    # Üst yüz
    glTexCoord2f(0.0, 0.0)
    glVertex3f(x, y + size, z)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(x + size, y + size, z)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(x + size, y + size, z + size)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(x, y + size, z + size)

    # Alt yüz
    glTexCoord2f(0.0, 0.0)
    glVertex3f(x, y, z)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(x + size, y, z)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(x + size, y, z + size)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(x, y, z + size)

    glEnd()

    glBindTexture(GL_TEXTURE_2D, 0)  # Texture binding'i sıfırla


def draw_blocks():
    for (x, y, z), texture in blocks.items():
        glColor3f(1.0, 1.0, 1.0)  # Varsayılan renk beyaz
        draw_cube(x, y, z, texture=texture)


def draw_crosshair():
    # 2D moduna geç
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, screen_width, 0, screen_height)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    # Crosshair'ı çiz
    glColor3f(1.0, 1.0, 1.0)  # Beyaz renk
    glBegin(GL_LINES)
    glVertex2f(screen_width / 2 - 20, screen_height / 2)
    glVertex2f(screen_width / 2 + 20, screen_height / 2)
    glVertex2f(screen_width / 2, screen_height / 2 - 20)
    glVertex2f(screen_width / 2, screen_height / 2 + 20)
    glEnd()

    # Eski matrisi geri yükle
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()




def update_camera():
    global camera_pos, camera_front, speed, is_jumping, jump_velocity, gravity, jump_gravity, ground_level, blocks, wood_positions, leaf_positions

    # Movement vector initialization
    move_vector = np.zeros(3)

    # Check key states for movement
    if 'w' in key_states:
        move_vector += speed * np.array([camera_front[0], 0, camera_front[2]])
    if 's' in key_states:
        move_vector -= speed * np.array([camera_front[0], 0, camera_front[2]])
    if 'a' in key_states:
        move_vector -= np.cross(camera_front, camera_up) * speed
    if 'd' in key_states:
        move_vector += np.cross(camera_front, camera_up) * speed

    # Jump control
    if ' ' in key_states and not is_jumping:
        is_jumping = True
        jump_velocity = jump_strength

    # Check for collisions with blocks, woods, and leaves
    buffer_distance = 0.3  # Adjust this value as needed
    new_camera_pos = camera_pos + move_vector

    # Variables to track collisions
    is_colliding_with_block = False
    is_colliding_with_wood = False
    is_colliding_with_leaf = False

    # Check collision with blocks
    for pos, block_type in blocks.items():
        if (
            new_camera_pos[0] + buffer_distance >= pos[0] and
            new_camera_pos[0] - buffer_distance <= pos[0] + 1 and
            new_camera_pos[1] >= pos[1] and
            new_camera_pos[1] <= pos[1] + 1 and
            new_camera_pos[2] + buffer_distance >= pos[2] and
            new_camera_pos[2] - buffer_distance <= pos[2] + 1
        ):
            # Collision detected with a block
            is_colliding_with_block = True
            break

    # Check collision with woods
    for wood_pos in wood_positions:
        if (
            new_camera_pos[0] + buffer_distance >= wood_pos[0] and
            new_camera_pos[0] - buffer_distance <= wood_pos[0] + 1 and
            new_camera_pos[1] >= wood_pos[1] and
            new_camera_pos[1] <= wood_pos[1] + 1 and
            new_camera_pos[2] + buffer_distance >= wood_pos[2] and
            new_camera_pos[2] - buffer_distance <= wood_pos[2] + 1
        ):
            # Collision detected with wood
            is_colliding_with_wood = True
            break

    # Check collision with leaves
    for leaf_pos in leaf_positions:
        if (
            new_camera_pos[0] + buffer_distance >= leaf_pos[0] and
            new_camera_pos[0] - buffer_distance <= leaf_pos[0] + 1 and
            new_camera_pos[1] >= leaf_pos[1] and
            new_camera_pos[1] <= leaf_pos[1] + 1 and
            new_camera_pos[2] + buffer_distance >= leaf_pos[2] and
            new_camera_pos[2] - buffer_distance <= leaf_pos[2] + 1
        ):
            # Collision detected with leaves
            is_colliding_with_leaf = True
            break

    # Update camera position based on collision status
    if not is_colliding_with_block and not is_colliding_with_wood and not is_colliding_with_leaf:
        camera_pos += move_vector

    # Jumping state
    if is_jumping:
        if not is_colliding_with_block and not is_colliding_with_wood and not is_colliding_with_leaf:
            camera_pos[1] += jump_velocity
            jump_velocity -= jump_gravity
        if camera_pos[1] <= ground_level:
            camera_pos[1] = ground_level
            is_jumping = False
            jump_velocity = 0.0
    else:
        if camera_pos[1] > ground_level:
            camera_pos[1] -= gravity
        else:
            camera_pos[1] = ground_level

    # Check if camera is colliding with blocks, woods, or leaves from below
    if not is_colliding_with_block and not is_colliding_with_wood and not is_colliding_with_leaf:
        for pos, block_type in blocks.items():
            if (
                camera_pos[0] + buffer_distance >= pos[0] and
                camera_pos[0] - buffer_distance <= pos[0] + 1 and
                camera_pos[1] >= pos[1] + 1 and
                camera_pos[1] <= pos[1] + 2 and
                camera_pos[2] + buffer_distance >= pos[2] and
                camera_pos[2] - buffer_distance <= pos[2] + 1
            ):
                # Place camera upside down on top of the block
                camera_pos[1] = pos[1] + 2
                is_jumping = False
                break

    # Check if camera is colliding with woods or leaves from below
    if not is_colliding_with_block and not is_colliding_with_wood:
        for wood_pos in wood_positions:
            if (
                camera_pos[0] + buffer_distance >= wood_pos[0] and
                camera_pos[0] - buffer_distance <= wood_pos[0] + 1 and
                camera_pos[1] >= wood_pos[1] + 1 and
                camera_pos[1] <= wood_pos[1] + 2 and
                camera_pos[2] + buffer_distance >= wood_pos[2] and
                camera_pos[2] - buffer_distance <= wood_pos[2] + 1
            ):
                # Place camera upside down on top of wood
                camera_pos[1] = wood_pos[1] + 2
                is_jumping = False
                break

        for leaf_pos in leaf_positions:
            if (
                camera_pos[0] + buffer_distance >= leaf_pos[0] and
                camera_pos[0] - buffer_distance <= leaf_pos[0] + 1 and
                camera_pos[1] >= leaf_pos[1] + 1 and
                camera_pos[1] <= leaf_pos[1] + 2 and
                camera_pos[2] + buffer_distance >= leaf_pos[2] and
                camera_pos[2] - buffer_distance <= leaf_pos[2] + 1
            ):
                # Place camera upside down on top of leaves
                camera_pos[1] = leaf_pos[1] + 2
                is_jumping = False
                break



    #print(camera_pos)
    #print(wood_positions)







def key_pressed(key, x, y):
    global key_states, selected_texture
    key_states.add(key.decode("utf-8"))

    if key == b'q':
        glutLeaveMainLoop()
    elif key == b't':  # Texture'ları değiştirmek için "t" tuşu
        cycle_textures()


def cycle_textures(forward=True):
    global selected_texture
    if forward:
        selected_texture = (selected_texture + 1) % len(block_textures)
    else:
        selected_texture = (selected_texture - 1) % len(block_textures)


def key_released(key, x, y):
    global key_states
    key_states.discard(key.decode("utf-8"))


def mouse_click(button, state, x, y):
    global mouse_left_pressed, mouse_right_pressed
    if button == GLUT_LEFT_BUTTON:
        mouse_left_pressed = (state == GLUT_DOWN)
        if mouse_left_pressed:
            place_block()
    elif button == GLUT_RIGHT_BUTTON:
        mouse_right_pressed = (state == GLUT_DOWN)
        if mouse_right_pressed:
            remove_block()
    glutPostRedisplay()


def mouse_look(x, y):
    global yaw, pitch, camera_front, sensitivity, lastX, lastY, total_yaw, screen_width, screen_height

    # Calculate offset
    x_offset = (x - lastX) * sensitivity
    y_offset = (lastY - y) * sensitivity  # Reversed since y-coordinates go from bottom to top
    lastX = x
    lastY = y

    # Update yaw and pitch based on offsets
    yaw += x_offset
    pitch += y_offset

    # Clamp pitch to avoid flipping
    if pitch > 89.0:
        pitch = 89.0
    elif pitch < -89.0:
        pitch = -89.0

    # Update total yaw within 360-degree range
    total_yaw = yaw % 360.0

    # Calculate camera front direction based on total yaw and pitch
    front = np.array([
        np.cos(np.radians(total_yaw)) * np.cos(np.radians(pitch)),
        np.sin(np.radians(pitch)),
        np.sin(np.radians(total_yaw)) * np.cos(np.radians(pitch))
    ])
    camera_front = front / np.linalg.norm(front)

    # Center the mouse
    glutWarpPointer(screen_width // 2, screen_height // 2)
    lastX = screen_width // 2
    lastY = screen_height // 2


def place_block():
    global blocks, selected_texture
    pos = np.floor(camera_pos + camera_front * 2).astype(int)
    blocks[tuple(pos)] = block_textures.get(selected_texture, texture_id)
    pygame.mixer.Sound("place_block.wav").play()


def remove_block():
    global blocks, wood_positions
    pos = np.floor(camera_pos + camera_front * 2).astype(int)
    pos = tuple(pos)
    if pos in blocks:
        del blocks[pos]
        pygame.mixer.Sound("break_block.wav").play()


def reshape(width, height):
    global screen_width, screen_height
    screen_width = width
    screen_height = height
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, width / height, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)


# Update function to handle dynamic elements
def update():
    update_camera()  # Update camera position for gravity and jumping

    glutPostRedisplay()  # Request a redisplay


# Global variables
total_yaw = -90.0, 0.0, np.array([0.0, 0.0, -1.0]), 0.1, 400, 300, -90.0
screen_width, screen_height = 649, 640
timer_id = 0
key_states = set()  # Tuş durumlarını saklamak için küme oluştur


def update_frame(_):
    
    # Ekranı güncelle
    glutPostRedisplay()

    # Timer'ı yeniden başlat
    glutTimerFunc(1000 // 30, update_frame, 0)  # 60 FPS (her saniyede 60 kare)


def main():
    global lastX, lastY, screen_width, screen_height, timer_id

    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(screen_width, screen_height)
    glutCreateWindow(b"Minecraft Orman Sahnesi")
    #glutFullScreen()

    glutWarpPointer(lastX, lastY)  # Mouse'u başlangıç pozisyonuna ayarla
    glutSetCursor(GLUT_CURSOR_NONE)  # Fare imlecini gizle
    init()
    glutDisplayFunc(display)
    glutIdleFunc(update)  # Boş durumda işlevi kullan
    glutReshapeFunc(reshape)
    glutPassiveMotionFunc(mouse_look)
    glutMouseFunc(mouse_click)
    glutKeyboardFunc(key_pressed)
    glutKeyboardUpFunc(key_released)
    timer_id = glutGet(GLUT_ELAPSED_TIME)
    glutTimerFunc(0, update_frame, 0)  # Timer'ı başlat
    glutMainLoop()


if __name__ == "__main__":
    main()
