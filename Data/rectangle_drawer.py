import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


def draw_rect(bottom_left, bottom_right, upper_left, upper_right, rectangle_color):
    glBegin(GL_QUADS)
    glColor3f(rectangle_color[0], rectangle_color[1], rectangle_color[2])
    glVertex2f(bottom_left[0], bottom_left[1])
    glVertex2f(bottom_right[0], bottom_right[1])
    glVertex2f(upper_left[0], upper_left[1])
    glVertex2f(upper_right[0], upper_right[1])
    glEnd()


def draw_line(point1, point2, line_color):
    glBegin(GL_LINES)
    glColor3f(line_color[0], line_color[1], line_color[2])
    glVertex2f(point1[0], point1[1])
    glVertex2f(point2[0], point2[1])
    glEnd()


def draw_cube(x_pos, y_pos, z_pos, x_distance, y_distance, z_distance):
    vertices = (
        (x_distance + x_pos, -y_distance + y_pos, -z_distance + z_pos),
        (x_distance + x_pos, y_distance + y_pos, -z_distance + z_pos),
        (-x_distance + x_pos, y_distance + y_pos, -z_distance + z_pos),
        (-x_distance + x_pos, -y_distance + y_pos, -z_distance + z_pos),
        (x_distance + x_pos, -y_distance + y_pos, z_distance + z_pos),
        (x_distance + x_pos, y_distance + y_pos, z_distance + z_pos),
        (-x_distance + x_pos, -y_distance + y_pos, z_distance + z_pos),
        (-x_distance + x_pos, y_distance + y_pos, z_distance + z_pos)
    )

    edges = (
        (0, 1),
        (0, 3),
        (0, 4),
        (2, 1),
        (2, 3),
        (2, 7),
        (6, 3),
        (6, 4),
        (6, 7),
        (5, 1),
        (5, 4),
        (5, 7)
    )

    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()


def drawtext(x, y, text):
    position = (x, y, 0)
    font = pygame.font.Font(None, 64)
    textSurface = font.render(text, True, (255, 255, 255, 255),
                              (0, 0, 0, 255))
    textData = pygame.image.tostring(textSurface, "RGBA", True)
    glRasterPos3d(*position)
    glDrawPixels(textSurface.get_width(), textSurface.get_height(),
                 GL_RGBA, GL_UNSIGNED_BYTE, textData)


def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluPerspective(45, (display[0] / display[1]), 0.1, 5000.0)

    glTranslatef(0.0, 0.0, -10)
    grid = []
    start = 0
    while True:
        start = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    glTranslatef(-0.2, 0.0, 0)
                if event.key == pygame.K_LEFT:
                    glTranslatef(0.2, 0.0, 0)
                if event.key == pygame.K_UP:
                    glTranslatef(0.0, -0.2, 0)
                if event.key == pygame.K_DOWN:
                    glTranslatef(0.0, 0.2, 0)

        # glRotatef(1, 3, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # drawtext(0,0,"ochinchin")
        # for loop in range(start, start+100):
        # grid.append(draw_cube(0, 0, loop*2, 1, 1, 1))
        # glTranslatef(0.00, 0.0, -0.1)
        # glRotate(11.25,0,0,1)
        # draw_line((0, -1), (0, -2), (1, 1, 1))
        # draw_rect((0, 0), (1, 0), (1, 1), (0, 1), (1, 0, 1))

        pygame.display.flip()
        # pygame.time.wait(1)


main()
