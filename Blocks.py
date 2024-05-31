from OpenGL.GL import *
from OpenGL.GLUT import *
from Biome import *
from mc import *


def cube(texture):
    if texture:
        glBindTexture(GL_TEXTURE_2D, texture)
    else:
        glBindTexture(GL_TEXTURE_2D, texture_id)  # Varsayılan texture

    glBegin(GL_QUADS)  # Start Drawing The Cube

    # Ön yüz
    glTexCoord2f(0.0, 0.0)
    glVertex3f(0, 0, 0)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(1.0, 0, 0)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(1.0, 1.0, 0)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(0, 1.0, 0)

    # Arka yüz
    glTexCoord2f(0.0, 0.0)
    glVertex3f(0, 0, 1.0)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(1.0, 0, 1.0)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(1.0, 1.0, 1.0)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(0, 1.0, 1.0)

    # Sol yüz
    glTexCoord2f(0.0, 0.0)
    glVertex3f(0, 0, 0)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(0, 0, 1.0)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(0, 1.0, 1.0)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(0, 1.0, 0)

    # Sağ yüz
    glTexCoord2f(0.0, 0.0)
    glVertex3f(1.0, 0, 0)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(1.0, 0, 1.0)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(1.0, 1.0, 1.0)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(1.0, 1.0, 0)

    # Üst yüz
    glTexCoord2f(0.0, 0.0)
    glVertex3f(0, 1.0, 0.0)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(1.0, 1.0, 0.0)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(1.0, 1.0, 1.0)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(0.0, 1.0, 1.0)

    # Alt yüz
    glTexCoord2f(0.0, 0.0)
    glVertex3f(0.0, 0.0, 0.0)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(1.0, 0.0, 0.0)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(1.0, 0.0, 1.0)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(0.0, 0.0, 1.0)

    glEnd()  # Done Drawing The Cube

    glBindTexture(GL_TEXTURE_2D, 0)  # Texture binding'i sıfırla

