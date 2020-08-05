import errno
import random
import socket
import string
import sys
import time
from statistics import mean
import Path_finding_algorithim
import decoder
import pygame
import snake_colors
from screeninfo import get_monitors

pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 25)


def randomString(stringLength=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


def draw(path, snacks, snakes, Rectangle_height, Rectangle_lengh, Username, buttons, additionnal_info, Window_size,
         Window, fps_number, enable_draw):
    Snake_bodies = []
    snake_head_position = []
    Snack_position = []
    width = Window_size[0]
    height = Window_size[1]
    if enable_draw:
        Window.fill((0, 255, 0))
        # update_fps(myfont,clock)
        Window.blit(myfont.render(str(fps_number), 1, pygame.Color("coral")), (10, 0))

    ##    for i,b in buttons.items():
    ##        b.draw(Window)
    for snake_name, snake, lives in snakes:
        # print(snake)

        # print('found snake')

        cubes = snake

        for i, cube in enumerate(cubes):
            if i == 0:
                if snake_name == Username:
                    snake_head_position = (cube[0][0], cube[0][1])

                else:
                    Snake_bodies.append((cube[0][0], cube[0][1]))

                if enable_draw:
                    bottom_left = ((cube[0][0]) * Rectangle_lengh, (cube[0][1]) * Rectangle_height)
                    top_right = (((cube[0][0]) * Rectangle_lengh) + Rectangle_lengh,
                                 ((cube[0][1]) * Rectangle_height) + Rectangle_height)
                    bottom_right = (bottom_left[0] + Rectangle_lengh, bottom_left[1])
                    top_left = (bottom_left[0], top_right[1])
                    pygame.draw.rect(Window, cube[2], (
                        (cube[0][0]) * Rectangle_lengh, (cube[0][1]) * Rectangle_height, Rectangle_lengh,
                        Rectangle_height))
                    pygame.draw.line(Window, (0, 0, 0), bottom_left, top_right, 2)
                    pygame.draw.line(Window, (0, 0, 0), bottom_right, top_left, 2)
                    textsurface = myfont.render(snake_name + ' lives: ' + str(lives), True, (255, 255, 255))
                    text_startgame = myfont.render(additionnal_info, True, (255, 255, 255))
                    Window.blit(text_startgame, ((width / 2 - (width / 5) / 2, height / 30)))
                    Window.blit(textsurface,
                                ((cube[0][0]) * Rectangle_lengh + 10, (cube[0][1]) * Rectangle_height + 10))
            else:
                Snake_bodies.append((cube[0][0], cube[0][1]))
                if enable_draw:
                    pygame.draw.rect(Window, cube[2], (
                        (cube[0][0]) * Rectangle_lengh, (cube[0][1]) * Rectangle_height, Rectangle_lengh,
                        Rectangle_height))
    for snack in snacks:
        Snack_position = (snack[0][0], snack[0][1])
        if enable_draw:
            pygame.draw.rect(Window, snack[2], (
                (snack[0][0]) * Rectangle_lengh, (snack[0][1]) * Rectangle_height, Rectangle_lengh, Rectangle_height))
    if enable_draw:
        for part in path:
            pygame.draw.rect(Window, (0, 0, 0), (
                (part[0]) * Rectangle_lengh, (part[1]) * Rectangle_height, Rectangle_lengh, Rectangle_height))
        pygame.display.update()
    return Snake_bodies, snake_head_position, Snack_position


def draw_path(path, Window_size, Window):
    width = Window_size[0]
    height = Window_size[1]
    for part in path:
        pygame.draw.rect(Window, (100, 100, 100),
                         ((part[0]) * Rectangle_lengh, (part[1]) * Rectangle_height, Rectangle_lengh, Rectangle_height))




def main(IP, size, enable_draw):
    key_pressed = [0, 0, 0]
    Grid_factor = 4
    Grid_size = [int(16 * Grid_factor), int(9 * Grid_factor)]
    for m in get_monitors():
        print(str(m))
        print(m.width)
        print(m.height)
    print((m.width // Grid_size[0]) * Grid_size[0])
    print((m.height // Grid_size[1]) * Grid_size[1])

    width = ((m.width // size) // Grid_size[0]) * Grid_size[0]
    height = ((m.height // size) // Grid_size[1]) * Grid_size[1]

    Window_size = (width, height)

    HEADER_LENGTH = 50
    PORT = 1234
    my_username = 'BOT' + randomString(stringLength=4)
    Username = my_username
    color_input = snake_colors.handle_input_color('black')
    my_username += '|' + color_input

    # Create a socket
    # socket.AF_INET - address family, IPv4, some otehr possible are AF_INET6, AF_BLUETOOTH, AF_UNIX
    # socket.SOCK_STREAM - TCP, conection-based, socket.SOCK_DGRAM - UDP, connectionless, datagrams, socket.SOCK_RAW - raw IP packets
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to a given ip and port
    client_socket.connect((IP, PORT))

    # Set connection to non-blocking state, so .recv() call won;t block, just return some exception we'll handle
    client_socket.setblocking(False)

    # Prepare username and header and send them
    # We need to encode username to bytes, then count number of bytes and prepare header of fixed size, that we encode to bytes as well
    username = my_username.encode('utf-8')
    username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
    client_socket.send(username_header + username)
    clock = pygame.time.Clock()
    Rectangle_lengh = Window_size[0] // Grid_size[0]

    #################START WINDOW
    if enable_draw:
        Window = pygame.display.set_mode(Window_size)
    else:
        Window = 0

    snakes = []
    snacks = []
    buttons = {}
    Rectangle_height = Window_size[1] // Grid_size[1]
    additional_info = ''
    Clear_Grid = []
    Grid_factor = size
    Grid_size = [int(16 * Grid_factor), int(9 * Grid_factor)]
    for loop in range(Grid_size[1]):
        Clear_Grid.append([1] * Grid_size[0])
    # for loop in matrix:
    #     print(loop)
    fps_number = None
    path = []
    fps_list = []
    while True:
        start_time = time.time()
        Snake_bodies, snake_head_position, Snack_position = draw(path, snacks, snakes, Rectangle_height,
                                                                 Rectangle_lengh, Username, buttons, additional_info,
                                                                 Window_size, Window, fps_number, enable_draw)

        try:
            path = Path_finding_algorithim.find_path_to_snack(Snake_bodies, snake_head_position, Snack_position)
            if path[1][1] < path[0][1]:
                key_pressed[0] = 'Up'
            if path[1][1] > path[0][1]:
                key_pressed[0] = 'Down'
            if path[1][0] < path[0][0]:
                key_pressed[0] = 'Left'
            if path[1][0] > path[0][0]:
                key_pressed[0] = 'Right'

        except IndexError:
            print("pathfinding Failed")

        if enable_draw:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
        # Wait for user to input a message
        message = str(key_pressed[0])  # +' '+str(key_pressed[1])+' '+str(key_pressed[2])

        # If message is not empty - send it

        if message:
            # Encode message to bytes, prepare header and convert to bytes, like for username above, then send
            message = message.encode('utf-8')
            message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
            client_socket.send(message_header + message)

        try:
            # Now we want to loop over received messages (there might be more than one) and print them
            while True:
                message_from_server = False
                # Receive our "header" containing username length, it's size is defined and constant
                username_header = client_socket.recv(HEADER_LENGTH)

                # If we received no data, server gracefully closed a connection, for example using socket.close() or socket.shutdown(socket.SHUT_RDWR)
                if not len(username_header):
                    print('Connection closed by the server')
                    sys.exit()

                # Convert header to int value
                username_length = int(username_header.decode('utf-8').strip())

                # Receive and decode username
                username = client_socket.recv(username_length).decode('utf-8')

                # Now do the same for message (as we received username, we received whole message, there's no need to check if it has any length)
                message_header = client_socket.recv(HEADER_LENGTH)
                message_length = int(message_header.decode('utf-8').strip())
                message = client_socket.recv(message_length).decode('utf-8')

                snakes, snacks, additional_info, Sounds_to_play_decoded = decoder.decode(message)
                try:
                    fps_number = 1.0 / (time.time() - start_time)
                    fps_list.append(fps_number)

                    if len(fps_list) > 30:
                        # print(fps_list)
                        print("Average fps is", mean(fps_list))
                        fps_list = []
                    if fps_number < 25:
                        fps_number = "It's lagging under 25 fps threshold " + str(fps_number)

                except:
                    fps_number = 0


        except IOError as e:
            # This is normal on non blocking connections - when there are no incoming data error is going to be raised
            # Some operating systems will indicate that using AGAIN, and some using WOULDBLOCK error code
            # We are going to check for both - if one of them - that's expected, means no incoming data, continue as normal
            # If we got different error code - something happened
            if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                print('Reading error: {}'.format(str(e)))
                # sys.exit()

            # We just did not receive anything
            continue

        except Exception as e:
            # Any other exception - something happened, exit
            print('Reading error: '.format(str(e)))
            # sys.exit()
            pass
        except:
            pass


main('10.0.0.3', 4, True)
