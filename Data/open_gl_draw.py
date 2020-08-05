import pygame
from pygame.locals import *
import random
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random


def draw_cube(x_pos, y_pos, z_pos, x_distance, y_distance, z_distance, angle):
    glPushMatrix()
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
        (5, 7), # (0,7), (1,6), (2,4), (3,5)
    )
    glRotate(angle, 1, 1, 1)
    glBegin(GL_LINES)


    for edge in edges:
        for vertex in edge:
            glColor3f(random.random(),random.random(),random.random())
            glVertex3fv(vertices[vertex])

    glEnd()

    #glBegin(GL_QUADS)
    for edge in edges:
        for vertex in edge:
            # glColor3f(random.random(),random.random(),random.random())
            glVertex3fv(vertices[vertex])
    #glEnd()

    glPopMatrix()


def draw_rect(color, position):
    bottom_left = (position[0], position[1])
    bottom_right = (bottom_left[0]+position[2], bottom_left[1])
    upper_left = (bottom_left[0], bottom_left[1]+position[3])
    upper_right = (bottom_left[0]+position[2], bottom_left[1]+position[3])
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
    glVertex2f(point1[0], point1[1])
    glVertex2f(point2[0], point2[1])
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

angle=0


def draw(snacks, snakes, Rectangle_height, Rectangle_lengh, additionnal_info, Window_size, Grid_size,
         background_color, Negative_color, Window, Draw_grid_bool, Winning_font, myfont):
    global angle
    angle+=1
    if angle>10000:
        angle=100
    width = Window_size[0]
    height = Window_size[1]
    # Clear window
    # Window.fill(background_color)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    # Check if we need to get Negative color
    glPushMatrix()
    glLineWidth(10)
    draw_line((-32,-20),(-32,100),(1,1,1))
    draw_line((32, -20), (32, 100), (1, 1, 1))
    draw_line((-100, -16), ( 100, -16), (1, 1, 1))
    draw_line((-100, 20), (100, 20), (1, 1, 1))
    glPopMatrix()
    draw_cube(0, 0, 0, 3, 3, 3,angle)
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
    for snake_name, snake, lives in snakes:

        cubes = snake
        for i, cube in enumerate(cubes):

            if i == 0:
                # if it's the head of the snake draw crosses on it
                bottom_left = ((cube[0][0])-32,((cube[0][1])*-1)+19)
                top_right = (bottom_left[0]+1,bottom_left[1]+1)
                bottom_right = (bottom_left[0] + 1, bottom_left[1])
                top_left = (bottom_left[0], top_right[1])
                #pygame.draw.rect(Window, cube[2], (
                #    (cube[0][0]) * Rectangle_lengh, (cube[0][1]) * Rectangle_height, Rectangle_lengh, Rectangle_height))
                #draw_rect((1,1,1), ((cube[0][0]) * Rectangle_lengh, (cube[0][1]) * Rectangle_height, Rectangle_lengh, Rectangle_height))
                draw_rect((cube[2][0]/256, cube[2][1]/256,cube[2][2]/256,),((cube[0][0])-32, ((cube[0][1])*-1)+19, 1, 1))
                # print(((cube[0][0]), (cube[0][1]), 1, 1))
                glLineWidth(1)
                draw_line(bottom_left, top_right, (1,0,0))
                draw_line(bottom_right, top_left, (1,0,0))
                #textsurface = myfont.render(snake_name + ' lives: ' + str(lives), True, draw_text_color)
                #text_startgame = myfont.render(additionnal_info, True, draw_text_color)
                #startgame_rect = text_startgame.get_rect(center=(int(width / 2), int(height / 25)))
                #Window.blit(text_startgame, startgame_rect)
                #Window.blit(textsurface, ((cube[0][0]) * Rectangle_lengh + 10, (cube[0][1]) * Rectangle_height + 10))
                #draw_rect((1,1,1),(0,0,1,1))
                #draw_line((0,0),(-1,0),(0.5,0.5,0.5))
                #print('drawing')
            else:
                if cube[2]==[0,0,0]:
                    cube[2]=(100,100,100)
                # Else just draw the rectangle
                # draw_rect(cube[2], ((cube[0][0]) * Rectangle_lengh, (cube[0][1]) * Rectangle_height, Rectangle_lengh, Rectangle_height))
                draw_rect((cube[2][0]/256,cube[2][1]/256,cube[2][2]/256,),((cube[0][0])-32, ((cube[0][1])*-1)+19, 1, 1))
                #draw_rect((cube[2][0]/256,cube[2][1]/256,cube[2][2]/256,), ((cube[0][0]) - 30, ((cube[0][1]) * -1) + 20, 1, 1))
    for snack in snacks:
        # Draw snacks
        ##        print
        ##        print(snack[0])
        ##        print(snack[0][0])
        pygame.draw.rect(Window, snack[2], (
            (snack[0][0]) * Rectangle_lengh, (snack[0][1]) * Rectangle_height, Rectangle_lengh, Rectangle_height))
        pygame.draw.rect(Window, snack[2], (
            (snack[0][0]) * Rectangle_lengh, (snack[0][1]) * Rectangle_height, Rectangle_lengh, Rectangle_height))
        bottom_left = ((snack[0][0]) * Rectangle_lengh, (snack[0][1]) * Rectangle_height)
        top_right = (
            ((snack[0][0]) * Rectangle_lengh) + Rectangle_lengh, ((snack[0][1]) * Rectangle_height) + Rectangle_height)
        bottom_right = (bottom_left[0] + Rectangle_lengh, bottom_left[1])
        top_left = (bottom_left[0], top_right[1])
        draw_rect(snack[2], ((snack[0][0])-32, (snack[0][1])*-1+19, 1, 1))
        #pygame.draw.rect(Window, snack[2], (
        #    (snack[0][0]) * Rectangle_lengh, (snack[0][1]) * Rectangle_height, Rectangle_lengh, Rectangle_height))
        #pygame.draw.line(Window, (255, 255, 255), bottom_left, top_right, 2)
        #pygame.draw.line(Window, (255, 255, 255), bottom_right, top_left, 2)
    pygame.display.flip()
