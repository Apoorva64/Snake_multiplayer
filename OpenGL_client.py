import errno
import math
import os
import socket
import sys

import Settings_Reader
import decoder
import pygame
import snake_colors
from screeninfo import get_monitors
import open_gl_draw
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

def main(IP, my_username, color_input):
    # Reading settings
    settings = Settings_Reader.Read_Settings_Client()
    fps = settings['Client_Update_Fps']
    background_color = settings['Background_Color']
    Draw_grid_bool = settings['Draw_Grid']
    # Calculating brightness
    brightness = math.sqrt(
        0.241 * background_color[0] * background_color[0] + 0.691 * background_color[1] * background_color[1] + 0.068 *
        background_color[2] * background_color[2])
    print(brightness)
    # checking if we have to invert the colors
    if brightness < 127:
        Negative_color = True
        print('must negative color')
    else:
        Negative_color = False
    # initilisating mixer and loading music and sfx

    pygame.mixer.pre_init(22100, -16, 1, 64)
    pygame.mixer.init()
    Sounds_dict = {'join_sound': pygame.mixer.Sound(os.path.join('Sounds', 'Join_sound.wav')),
                   'quit_sound': pygame.mixer.Sound(os.path.join('Sounds', 'Quit_sound.wav')),
                   'kill_sound': pygame.mixer.Sound(os.path.join('Sounds', 'Kill Confirmed  Sound Effect.wav')),
                   'killed_sound': pygame.mixer.Sound(os.path.join('Sounds', 'Killed_sound.wav')),
                   'click_sound': pygame.mixer.Sound(os.path.join('Sounds', 'click.wav')),
                   'hover_sound': pygame.mixer.Sound(os.path.join('Sounds', 'hover.wav')),
                   'countdown_3': pygame.mixer.Sound(os.path.join('Sounds', 'fight321.wav')),
                   'Win_sound': pygame.mixer.Sound(os.path.join('Sounds', 'YouWin.wav')),
                   'Lose_sound': pygame.mixer.Sound(os.path.join('Sounds', 'YouLose.wav')),
                   'eating_sound': pygame.mixer.Sound(os.path.join('Sounds', 'eating_sound.wav')),
                   'Destroyed_sound': pygame.mixer.Sound(os.path.join('Sounds', 'Destroyed.wav'))}
    # Sounds_dict['countdown_5']=pygame.mixer.Sound(os.path.join('Sounds','SFX Select.wav'))
    # Sounds_dict['countdown_4']=pygame.mixer.Sound(os.path.join('Sounds','SFX Select.wav'))
    # Sounds_dict['countdown_2']=pygame.mixer.Sound(os.path.join('Sounds','SFX Select.wav'))
    # Sounds_dict['countdown_1']=pygame.mixer.Sound(os.path.join('Sounds','SFX Select.wav'))
    # Sounds_dict['fight_sound']=pygame.mixer.Sound(os.path.join('Sounds','SFX Select.wav'))
    # ability to play movies was removed
    # Sounds_dict['Destroyed_video']= pygame.movie.Movie(os.path.join('Sounds','you-died-hd.mpg'))
    music = pygame.mixer.music.load(os.path.join('Sounds', 'MusicMix.wav'))
    pygame.mixer.music.play(-1)
    # initilisating variables,buttons,list,etc...
    key_pressed = [0, 0, 0]
    ##    width=500
    ##    height=500
    Grid_factor = 4
    Grid_size = [int(16 * Grid_factor), int(9 * Grid_factor)]
    s_list = []
    Sounds_to_play_decoded_check = ''
    # Getting monitor size
    for m in get_monitors():
        print(str(m))
        print(m.width)
        print(m.height)
    print((m.width // Grid_size[0]) * Grid_size[0])
    print((m.height // Grid_size[1]) * Grid_size[1])

    width = ((m.width) // Grid_size[0]) * Grid_size[0]
    height = ((m.height) // Grid_size[1]) * Grid_size[1]
    # initilisasing fonts
    pygame.font.init()
    myfont = pygame.font.SysFont('Comic Sans MS', int(width / 54.64))
    Winning_font = pygame.font.Font("Kilogram-GvBO.otf", int(width / 27.32))
    Window_size = (width, height)

    ##    width = 500
    ##    rows = 20

    HEADER_LENGTH = 50
    # IP=str(input('Give IP address: '))
    # IP = "192.168.100.2"
    PORT = 1234
    # my_username = input("Username: ")
    # my_username ='ochinchin'
    Username = my_username
    # color_input = snake_colors.handle_input_color(input("Color ex:  115;123;23 or write common color names: "))
    color_input = snake_colors.handle_input_color(color_input)
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
    Window = pygame.display.set_mode(Window_size,pygame.DOUBLEBUF | pygame.OPENGL)
    gluPerspective(45, (width/ height), 0.1, 5000.0)
    glTranslatef(0.0, 0.0, -55)
    snakes = []
    snacks = []
    Rectangle_height = Window_size[1] // Grid_size[1]
    Game_started = False
    additional_info = ''
    timer = 0
    infinite_loop = True
    win_sound_played = False
    lose_sound_played = False
    while infinite_loop:
        pygame.time.delay(int(1000 / fps))
        ##    clock.tick(10)
        Mouse_pos = pygame.mouse.get_pos()

        if len(additional_info) == 1:
            additional_info = 'Game starting in ' + additional_info
        elif additional_info == 'not started':
            additional_info = 'Wating for host to start the game'
        elif additional_info == 'Game_started':
            additional_info = 'Started'

            # buttons['start_game'].text=additional_info
        open_gl_draw.draw(snacks, snakes, Rectangle_height, Rectangle_lengh, additional_info, Window_size,
                          Grid_size, background_color, Negative_color, Window, Draw_grid_bool, Winning_font, myfont)
        # Processing snake inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    delete_all_snakes = True
                    infinite_loop = False

                if event.key == pygame.K_LEFT:
                    key_pressed[0] = 'Left'


                elif event.key == pygame.K_RIGHT:
                    key_pressed[0] = 'Right'

                elif event.key == pygame.K_UP:
                    key_pressed[0] = 'Up'

                elif event.key == pygame.K_DOWN:
                    key_pressed[0] = 'Down'
                else:
                    key_pressed[0] = None
                    # if event.key == pygame.K_a:
                #     key_pressed[1]='Left'

                # elif event.key == pygame.K_d:
                #     key_pressed[1]='Right'

                # elif event.key == pygame.K_w:
                #     key_pressed[1]='Up'

                # elif event.key == pygame.K_s:
                #     key_pressed[1]='Down'
                # else:
                #     key_pressed[1]=None
                # if event.key == pygame.K_f:
                #     key_pressed[2]='Left'

                # elif event.key == pygame.K_h:
                #     key_pressed[2]='Right'

                # elif event.key == pygame.K_t:
                #     key_pressed[2]='Up'

                # elif event.key == pygame.K_g:
                #     key_pressed[2]='Down'
                # else:
                #     key_pressed[2]=None
        # resseting varables
        if len(additional_info) == 1:
            if additional_info != '0':
                win_sound_played = False
                lose_sound_played = False
        # Sending inputs in a message
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
                # Checking if the message comes from the server
                if username == 'SERVER(sending(Cube.info))':
                    # print('message: ',message)
                    message_from_server = True
                    # Decode the message
                    snakes, snacks, additional_info, Sounds_to_play_decoded = decoder.decode(message)
                    # Play the sounds
                    if my_username.split('|')[0] in additional_info and not win_sound_played:
                        print('you win')
                        Sounds_dict['Win_sound'].play()
                        win_sound_played = True
                    elif 'winner' in additional_info and my_username.split('|')[0] not in additional_info \
                            and not lose_sound_played:
                        print('You lose')
                        Sounds_dict['Lose_sound'].play()
                        lose_sound_played = True
                    if Sounds_to_play_decoded != Sounds_to_play_decoded_check:

                        # print('sound_change')
                        if Sounds_to_play_decoded != ['']:
                            for sound in Sounds_to_play_decoded:
                                # if sound[1]=='countdown_3'and not pygame.mixer.get_busy():
                                #     print('playing')
                                #     Sounds_dict['countdown_3'].play()

                                if sound[0] == my_username:  # not pygame.mixer.get_busy():
                                    # print(sound)
                                    # if sound=='join_sound':
                                    #     Sounds_dict['join_sound'].play()
                                    # except Exception as e:
                                    #     print (e)
                                    # print(sound[1])
                                    # print(Sounds_dict)
                                    # print(Sounds_dict['killed_sound'])
                                    # print(Sounds_dict[str(sound)])
                                    # if sound[1]=='join_sound':
                                    #     Sounds_dict['Destroyed_video'].play()
                                    Sounds_dict[sound[1]].set_volume(1)
                                    Sounds_dict[sound[1]].play()
                                    if sound[1] == 'Lose_sound':
                                        Sounds_dict['Destroyed_sound'].play()
                                elif ('countdown' in sound[1] or sound[1] == 'join_sound' or sound[
                                    1] == 'quit_sound') and not pygame.mixer.get_busy():
                                    Sounds_dict[sound[1]].play()
                                elif sound[0] != my_username and sound[0] != 'all':
                                    Sounds_dict[sound[1]].set_volume(0.3)
                                    if sound[1] == 'Lose_sound':
                                        Sounds_dict['Destroyed_sound'].play()
                                    else:

                                        # print('reducing volume')
                                        Sounds_dict[sound[1]].play()

                        Sounds_to_play_decoded_check = Sounds_to_play_decoded
                    # print(snakes)

                # Print message
                # print(f'{username} > {message}')

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


#main('10.0.0.12', 'apoorva', 'white')
main(input('give ip'), input('name'), input('give color'))
