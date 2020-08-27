import pygame
from pygame.locals import *
import random
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random


def draw_cube(x_pos, y_pos, z_pos, x_distance, y_distance, z_distance, color, fill=False, fill_color=(255, 255, 255)):
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
        (5, 7),  # (0,7), (1,6), (2,4), (3,5)
    )
    surfaces = (
        (0, 1, 2, 3),
        (3, 2, 7, 6),
        (6, 7, 5, 4),
        (4, 5, 1, 0),
        (1, 5, 7, 2),
        (4, 0, 3, 6)
    )
    # glRotate(angle, 1, 1, 1)

    if fill:
        glPushMatrix()
        glBegin(GL_QUADS)
        for surface in surfaces:
            glColor3f(fill_color[0] / 255, fill_color[1] / 255, fill_color[2] / 255)
            x = 0
            for vertex in surface:
                x += 1
                # glColor3fv(0,0,1)
                glVertex3fv(vertices[vertex])
        glEnd()
        glPopMatrix()

    glPushMatrix()
    glBegin(GL_LINES)

    for edge in edges:
        for vertex in edge:
            glColor3f(color[0] / 255, color[1] / 255, color[2] / 255)
            glVertex3fv(vertices[vertex])

    glEnd()

    glPopMatrix()


def draw_rect(color, position):
    bottom_left = (position[0], position[1])
    bottom_right = (bottom_left[0] + position[2], bottom_left[1])
    upper_left = (bottom_left[0], bottom_left[1] + position[3])
    upper_right = (bottom_left[0] + position[2], bottom_left[1] + position[3])
    rectangle_color = color
    glBegin(GL_QUADS)
    glColor3f(rectangle_color[0], rectangle_color[1], rectangle_color[2])
    glVertex2f(bottom_left[0], bottom_left[1])
    glVertex2f(bottom_right[0], bottom_right[1])
    glVertex2f(upper_right[0], upper_right[1])
    glVertex2f(upper_left[0], upper_left[1])

    glEnd()


def draw_line(point1, point2, line_color):
    glBegin(GL_LINES)
    glColor3f(line_color[0], line_color[1], line_color[2])
    glVertex3f(point1[0], point1[1],1)
    glVertex3f(point2[0], point2[1],1)
    glEnd()


def drawtext(x, y, text):
    position = (x, y)
    font = pygame.font.Font(None, 64)
    textSurface = font.render(text, True, (255, 255, 255, 255),
                              (0, 0, 0, 255))
    textData = pygame.image.tostring(textSurface, "RGBA", True)
    glRasterPos2d(*position)
    glDrawPixels(textSurface.get_width(), textSurface.get_height(),
                 GL_RGBA, GL_UNSIGNED_BYTE, textData)


angle = 0
mouse_pos = (0, 0)


def draw_borders():
    # TODO fix bottom border to -18 but need to adjust other
    draw_cube(-33, 0, 0, 0.5, 19.5, 0.5, (0, 255, 0))
    draw_cube(33, 0, 0, 0.5, 19.5, 0.5, (0, 255, 0))

    draw_cube(0, -19, 0, 33.5, 0.5, 0.5, (0, 255, 0))
    draw_cube(0, 19, 0, 33.5, 0.5, 0.5, (0, 255, 0))


to_add_angle_y = 0
to_add_angle_x = 0


def draw(snacks, snakes, Rectangle_height, Rectangle_lengh, additionnal_info, Window_size, Grid_size,
         background_color, Negative_color, Window, Draw_grid_bool, Winning_font, myfont, Username, direction,
         cntrl_pressed):
    global angle
    global mouse_pos
    global to_add_angle_x
    global to_add_angle_y
    angle += 1
    head_x, head_y = 0, 0
    if angle > 10000:
        angle = 100
    width = Window_size[0]
    height = Window_size[1]
    # Clear window
    # Window.fill(background_color)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Check if we need to get Negative color
    if Negative_color:
        draw_text_color = (255, 255, 255)
    else:
        draw_text_color = (0, 0, 0)
    # Draw Grid
    # redo draw grid
    # if Draw_grid_bool:
    #    drawGrid(Window_size, Grid_size, Window, draw_text_color)
    # if winner draw text
    if 'winner' in additionnal_info:
        text_Winner = additionnal_info
        drawtext(0, 0, text_Winner)
        Window.blit(text_Winner, text_Winner_rect)
        additionnal_info = ''
    # glLineWidth(5)

    old_mouse_pos = mouse_pos
    if cntrl_pressed:
        mouse_pos = pygame.mouse.get_pos()
    if (mouse_pos[1] - old_mouse_pos[1]) > 0:
        to_add_angle_y += 1
    elif (mouse_pos[1] - old_mouse_pos[1]) < 0:
        to_add_angle_y += - 1
    if (mouse_pos[0] - old_mouse_pos[0]) > 0:
        to_add_angle_x += 1
    elif (mouse_pos[0] - old_mouse_pos[0]) < 0:
        to_add_angle_x += - 1
    counter = 0
    draw_order = []
    for snake_name, snake, lives in snakes:
        counter += 1
        if snake_name == Username:
            head_x = snake[0][0][0] - 32
            head_y = snake[0][0][1] * -1 + 18
            # draw_order.append((0,counter))
            break
    # counter=0
    # TODO Draw order still fcked fix
    for snake_name, snake, lives in snakes:
        # counter+=1
        for i, part in enumerate(snake):
            x_diff = part[0][0] - head_x
            y_diff = part[0][1] - head_y
            if direction[0] == "Left" and x_diff > 0:
                distance_from_main = -1 * (part[0][0] - head_x ** 2 + part[0][1] - head_y ** 2)
            elif direction[0] == "Right" and x_diff < 0:
                distance_from_main = -1 * (part[0][0] - head_x ** 2 + part[0][1] - head_y ** 2)
            elif direction[0] == "Up" and y_diff > 0:
                distance_from_main = -1 * (part[0][0] - head_x ** 2 + part[0][1] - head_y ** 2)
            elif direction[0] == "Down" and y_diff < 0:
                distance_from_main = -1 * (part[0][0] - head_x ** 2 + part[0][1] - head_y ** 2)
            else:
                distance_from_main = part[0][0] - head_x ** 2 + part[0][1] - head_y ** 2
            if part[2]==[0,0,0]:
                part[2]=(100,100,100)

            if i == 0:
                draw_order.append((distance_from_main, ("head", part[0], part[2])))
            else:
                draw_order.append((distance_from_main, ("part", part[0], part[2])))
    for part in snacks:
        x_diff = part[0][0] - head_x
        y_diff = part[0][1] - head_y
        if direction[0] == "Left" and x_diff > 0:
            distance_from_main = -1 * (part[0][0] - head_x ** 2 + part[0][1] - head_y ** 2)
        elif direction[0] == "Right" and x_diff < 0:
            distance_from_main = -1 * (part[0][0] - head_x ** 2 + part[0][1] - head_y ** 2)
        elif direction[0] == "Up" and y_diff > 0:
            distance_from_main = -1 * (part[0][0] - head_x ** 2 + part[0][1] - head_y ** 2)
        elif direction[0] == "Down" and y_diff < 0:
            distance_from_main = -1 * (part[0][0] - head_x ** 2 + part[0][1] - head_y ** 2)
        else:
            distance_from_main = part[0][0] - head_x ** 2 + part[0][1] - head_y ** 2
        draw_order.append((distance_from_main, ("snack", part[0], [])))
    # TODO find a better way to do this
    draw_order.sort(key=lambda tup: tup[0])
    draw_order.reverse()

    # setting camera
    far = 5 + to_add_angle_y
    distance_x = 30 + to_add_angle_x
    distance_y = distance_x
    if direction[0] == 'Right':
        gluLookAt(head_x - distance_x, head_y, far, head_x + distance_x, head_y, 0, 0, 0, 1)
    if direction[0] == 'Left':
        gluLookAt(head_x + distance_x, head_y, far, head_x - distance_x, head_y, 0, 0, 0, 1)
    if direction[0] == 'Up':
        gluLookAt(head_x, head_y - distance_y, far, head_x, head_y + distance_y, 0, 0, 0, 1)
    if direction[0] == 'Down':
        gluLookAt(head_x, head_y + distance_y, far, head_x, head_y - distance_y, 0, 0, 0, 1)
    # glRotatef(90,0,1,0)
    # dawing
    draw_borders()

    for dis, args in draw_order:
        if args[0] == "part":
            draw_cube(args[1][0] - 32, (-1 * args[1][1]) + 18, 0, 0.5, 0.5, 0.5, (0, 0, 0), fill=True,
                      fill_color=args[2])
        elif args[0] == "head":
            draw_cube(args[1][0] - 32, (-1 * args[1][1]) + 18, 0, 0.5, 0.5, 0.5, (255, 0, 0), fill=True,
                      fill_color=args[2])
        elif args[0] == "snack":

            draw_cube(args[1][0] - 32, (-1 * args[1][1]) + 18, 0, 0.5, 0.5, 0.5, (255, 255, 0), fill=True,
                      fill_color=(0, 0, 255))
            glPushMatrix()
            glLineWidth(10)
            draw_line((head_x, head_y),(args[1][0] - 32, (-1 * args[1][1]) + 18), (1,1,1))
            glPopMatrix()
            glLineWidth(2)


    pygame.display.flip()
