import errno
import os
import random
import socket
import sys
from collections import Counter
import Settings_Reader
import pygame
import respawn_mechanic
from screeninfo import get_monitors


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


class Cube:
    rows = 0
    w = 500
    Window_size = (0, 0)
    Grid_size = (0, 0)

    def __init__(self, start, orientation=(1, 0), color=(255, 0, 0)):
        self.position = start
        self.orientation = orientation
        self.color = color
        self.info = '|' + str(self.position[0]) + '>' + str(self.position[1]) + '|' + str(orientation[0]) + '>' + str(
            orientation[1]) + '|' + str(self.color[0]) + '>' + str(self.color[1]) + '>' + str(self.color[2])

    def move(self, orientation):
        self.orientation = orientation
        self.position = (self.position[0] + self.orientation[0], self.position[1] + self.orientation[1])
        self.info = '|' + str(self.position[0]) + '>' + str(self.position[1]) + '|' + str(orientation[0]) + '>' + str(
            orientation[1]) + '|' + str(self.color[0]) + '>' + str(self.color[1]) + '>' + str(self.color[2])

    def draw(self, Window):
        rectangle_lengh = Cube.Window_size[0] // Cube.Grid_size[0]
        rectangle_height = Cube.Window_size[1] // Cube.Grid_size[1]
        x_position = self.position[0]
        y_position = self.position[1]
        camera_x = 0
        camera_y = 0
        pygame.draw.rect(Window, self.color, ((x_position - camera_x) * rectangle_lengh
                                              , (y_position - camera_y) * rectangle_height
                                              , rectangle_lengh, rectangle_height))


class MyDict(dict):
    check = []

    def __setitem__(self, item, value):
        self.check.append(item)
        super(MyDict, self).__setitem__(item, value)


class snake(object):
    # initialising the snake (giving it all its parameters)
    def __init__(self, color, position, name, ID):
        self.snake_info = ''
        self.body = []
        self.turns = {}
        self.name = name
        self.color = [0, 0, 0]
        self.color[0] = int(color[0])
        self.color[1] = int(color[1])
        self.color[2] = int(color[2])
        self.ID = ID
        self.lives = 3
        self.head = Cube(position, color=self.color)
        self.body.append(self.head)
        self.orientation = [0, 1]
        self.kills = 0

    # As it's name suggests it moves the snake
    def move(self, key_pressed):

        self.snake_info = ''
        # move the snake according to the inputs
        if key_pressed == 'Left' and self.orientation != (1, 0):
            self.orientation = (-1, 0)
            self.turns[self.head.position[:]] = [self.orientation[0], self.orientation[1]]

        elif key_pressed == 'Right' and self.orientation != (-1, 0):
            self.orientation = (1, 0)
            self.turns[self.head.position[:]] = [self.orientation[0], self.orientation[1]]

        elif key_pressed == 'Up' and self.orientation != (0, 1):
            self.orientation = (0, -1)
            self.turns[self.head.position[:]] = [self.orientation[0], self.orientation[1]]

        elif key_pressed == 'Down' and self.orientation != (0, -1):
            self.orientation = (0, 1)
            self.turns[self.head.position[:]] = [self.orientation[0], self.orientation[1]]

        for i, c in enumerate(self.body):

            moved = False
            p = c.position[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move([turn[0], turn[1]])
                moved = True
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            # if you are in the wall move you on the other side
            if c.orientation[0] == -1 and c.position[0] < 0:
                c.position = (c.Grid_size[0], c.position[1])
            elif c.orientation[0] == 1 and c.position[0] > c.Grid_size[0] - 1:
                c.position = (-1, c.position[1])
            elif c.orientation[1] == 1 and c.position[1] > c.Grid_size[1] - 1:
                c.position = (c.position[0], -1)
            elif c.orientation[1] == -1 and c.position[1] < 0:
                c.position = (c.position[0], c.Grid_size[1])
            # kills snake on wall
            # if c.orientation[0] != -1 and c.position[0] < 0:
            #     c.position = (c.Grid_size[0]-1, c.position[1])
            # elif c.orientation[0] != 1 and c.position[0] > c.Grid_size[0]-1:
            #     c.position = (0,c.position[1])
            # elif c.orientation[1]!= 1 and c.position[1] > c.Grid_size[1]-1:
            #     c.position = (c.position[0], 0)
            # elif c.orientation[1] != -1 and c.position[1] < 0:
            #     c.position = (c.position[0],c.Grid_size[1]-1)

            # Works but does weird things with the wall at times
            if c.orientation[1] != 0 and c.position[0] < 0:
                c.position = (c.Grid_size[0] - 1, c.position[1])
            elif c.orientation[1] != 0 and c.position[0] > c.Grid_size[0] - 1:
                c.position = (0, c.position[1])
            elif c.orientation[0] != 0 and c.position[1] > c.Grid_size[1] - 1:
                c.position = (c.position[0], 0)
            elif c.orientation[0] != 0 and c.position[1] < 0:
                c.position = (c.position[0], c.Grid_size[1] - 1)


            # if c.position[0]<0:
            #     if c.orientation[0] == -1:
            #         c.position = (c.Grid_size[0], c.position[1])
            #     else:
            #         c.position = (c.Grid_size[0]-1, c.position[1])
            # if c.position[0] > c.Grid_size[0]-1:
            #     if c.orientation[0] == 1:
            #         c.position = (-1,c.position[1])
            #     else:
            #         c.position = (0,c.position[1])
            # if c.position[1] > c.Grid_size[1]-1:
            #     if c.orientation[1]== 1:
            #         c.position = (c.position[0], 0)
            #     else:
            #         c.position = (c.position[0], -1)
            # if c.position[1] < 0:
            #     if c.orientation[1] == -1:
            #         c.position = (c.position[0],c.Grid_size[1])
            #     else:
            #         c.position = (c.position[0],c.Grid_size[1]-1)

            else:
                if not moved:
                    c.move(c.orientation)
            self.snake_info += '"' + str(c.info)
            # put all the Cube's info in a string

        # Put all the snake's info in a string
        self.snake_info = str(self.name) + ',' + str(self.snake_info) + ',' + str(self.lives)

    def reset(self, position):
        # resets the snake
        self.head = Cube(position, color=self.color)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.orientation = [0, 1]
        self.lives -= 1

    def reset_lives_kills(self):
        # resets lives /kills
        self.lives = 3
        self.kills = 0

    def AddCube(self):
        # adds a lengh to the snake
        tail = self.body[-1]

        if tail.orientation == [1, 0]:
            self.body.append(Cube((tail.position[0] - 1, tail.position[1]), color=self.color))
        elif tail.orientation == [-1, 0]:
            self.body.append(Cube((tail.position[0] + 1, tail.position[1]), color=self.color))
        elif tail.orientation == [0, 1]:
            self.body.append(Cube((tail.position[0], tail.position[1] - 1), color=self.color))
        elif tail.orientation == [0, -1]:
            self.body.append(Cube((tail.position[0], tail.position[1] + 1), color=self.color))

        self.body[-1].orientation = tail.orientation

    def draw(self, surface):
        # draws the snake
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface)
            else:
                c.draw(surface)


def redrawWindow(surface, s_list, snack_list):
    # draws the window
    surface.fill((0, 0, 0))
    for key, s in s_list.items():
        s.draw(surface)
    for key, snack in snack_list.items():
        try:
            snack.draw(surface)
        except:
            print('rip')
            pass
    pygame.display.update()


def Check_winner(s_list):
    # checks for winner
    Not_dead_snakes = []
    for s in s_list:
        if s_list[s] != '':
            Not_dead_snakes.append((s_list[s].ID, s_list[s].name))

    return Not_dead_snakes


def main():
    # Getting info from settings file
    Settings_data = Settings_Reader.Read_Settings_Server()

    # Game_Update_Fps=25
    Game_Update_Fps = Settings_data['Game_Update_Fps']
    # Server_Update_Fps=50
    Server_Update_Fps = Settings_data['Server_Update_Fps']
    draw_Window = Settings_data['Enable_Draw']
    Game_Update_Delay = int(1000 / Game_Update_Fps)
    Server_Delay = int(1000 / Server_Update_Fps)

    IP = get_ip()
    # IP=str(input('pls give IP: '))
    ##        IP = "127.0.0.1"
    # Declaring lists, bools, strings and variables
    Gamestarted = False
    Game_State_Info = 'not started'
    Sounds_To_Play = []
    players = MyDict()
    HEADER_LENGTH = 50
    PORT = 1234
    my_username = 'SERVER(sending(Cube.info))'
    key_pressed = [0, 0, 0]
    Grid_factor = 4
    Grid_size = [int(16 * Grid_factor), int(9 * Grid_factor)]
    # Get monitor size
    for m in get_monitors():
        print(str(m))
        print(m.width)
        print(m.height)
    print((m.width // Grid_size[0]) * Grid_size[0])
    print((m.height // Grid_size[1]) * Grid_size[1])
    width = ((int(m.width / 10)) // Grid_size[0]) * Grid_size[0]
    height = ((int(m.height / 10)) // Grid_size[1]) * Grid_size[1]
    Window_size = (width, height)
    Cube.Window_size = Window_size
    Cube.Grid_size = Grid_size
    s_list = {}

    if draw_Window:
        Window = pygame.display.set_mode(Window_size, )  # pygame.FULLSCREEN)
    snack_list = {}
    # players_check=[123]
    timer = 0
    infinite_loop = True
    Time_out = []
    clock = pygame.time.Clock()
    snake_name = []
    x = random.randrange(Grid_size[0])
    y = random.randrange(Grid_size[1])
    snack = Cube((x, y), color=(127, 127, 127))
    No_spawn_positions = snack.position
    print('Snack_position', x, y)

    Grid_position_list = []
    # Getting all possible position in a list to not have to compute this everytime
    for position_y in range(Grid_size[1]):
        for position_x in range(Grid_size[0]):
            Grid_position_list.append((position_x, position_y))
    # for snake1 in s_list:
    #     snake_name.append(snake1.name)
    players_items_changed_reset_timer = 0
    Start_Gamestarted_timer = False
    Gamestarted_timer = 0

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
    connected = True
    fps_number = 0

    while infinite_loop:
        # Regulate fps
        clock.tick(Server_Update_Fps)
        ##########################ADDING AND REMOVING PLAYERS
        #######removing players
        if Gamestarted and len(Check_winner(s_list)) == 1:
            Gamestarted = False
            Game_State_Info = 'The winner is ' + str(Check_winner(s_list)[0][1])
            print('The Winner is', Check_winner(s_list)[0][1])
        # print(Check_winner(s_list))

        players_items_changed_reset_timer += 1
        if players_items_changed_reset_timer > 10:
            players_items_changed_reset_timer = 0
            for s in s_list:
                if s not in players.check:
                    Time_out.append(s)
                    # print(s,' is lagging?!?')
            players.check = []
        Time_outdict = dict(Counter(Time_out))
        No_spawn_positions = []
        for key in Time_outdict:
            ##            if Time_outdict[key]>10:

            # print(key,'is lagging')
            if Time_outdict[key] > 20:
                print(key, 'has disconnected, deleting snake')
                Sounds_To_Play.append((key, 'quit_sound'))
                del s_list[key]
                del players[key]
                Time_out = []

        # print('2',players.check)
        # ADDING PLAYERS
        if len(players) != len(s_list):
            print('detected list change')
            if len(players) > len(s_list):

                for player in players:
                    print('1', player)
                    if player not in snake_name:
                        print('2', player)
                        name, color = player.split('|')
                        color_split = color.split(';')
                        # print(color_split)
                        color = (color_split[0], color_split[1], color_split[2])
                        ID = player
                        Spawn_position = respawn_mechanic.Get_spawn_location(Grid_position_list, No_spawn_positions)
                        s_list[player] = snake(color, Spawn_position, name, ID)
                        Sounds_To_Play.append((player, 'join_sound'))
                        # snack_list[player]=Cube(randomSnack(Grid_size,s_list[player]), color=(0,0,255))

        ##########################ADDING AND REMOVING PLAYERS
        ##########################check if gamestarted and reset(starting and reseting game)

        if os.path.isfile(os.path.join('temp', 'start game.txt')):
            Start_Gamestarted_timer = True
            os.remove(os.path.join('temp', 'start game.txt'))
            print('starting Game')

        if os.path.isfile(os.path.join('temp', 'reset.txt')):
            Gamestarted = False
            os.remove(os.path.join('temp', 'reset.txt'))
            s_list = {}
            Game_State_Info = 'not started'
            print('Stopped Game and reset')

        if Start_Gamestarted_timer:
            Gamestarted_timer += 1
        if 2000 / Server_Delay > Gamestarted_timer > 1000 / Server_Delay:
            Game_State_Info = '3'
            if ('all', 'countdown_3') not in Sounds_To_Play:
                Sounds_To_Play.append(('all', 'countdown_3'))

        elif 3000 / Server_Delay > Gamestarted_timer > 2000 / Server_Delay:
            Game_State_Info = '2'
            # if ('all','countdown_2') not in Sounds_To_Play:
            #     Sounds_To_Play.append(('all','countdown_2'))

        elif 4000 / Server_Delay > Gamestarted_timer > 3000 / Server_Delay:
            Game_State_Info = '1'
            # if ('all','countdown_1') not in Sounds_To_Play:
            #     Sounds_To_Play.append(('all','countdown_1'))

        # elif 5000/Server_Delay>Gamestarted_timer>4000/Server_Delay:
        #     Game_State_Info='2'

        # elif 6000/Server_Delay>Gamestarted_timer>5000/Server_Delay:
        #     Game_State_Info='1'

        elif Gamestarted_timer > 4000 / Server_Delay:
            # if ('all','fight_sound') not in Sounds_To_Play:
            #     Sounds_To_Play.append(('all','fight_sound'))
            Game_State_Info = '0'
            Game_State_Info = 'Game_started'
            Gamestarted = True
            s_list = {}
            Gamestarted_timer = 0
            Start_Gamestarted_timer = False

        # print(Gamestarted)
        ##########################check if gamestarted and reset(starting and reseting game)

        delete_all_snakes = False
        key_pressed = [0, 0, 0]
        timer += 1

        if draw_Window:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        delete_all_snakes = True
                        infinite_loop = False

        if timer > Game_Update_Delay / Server_Delay:
            Sounds_To_Play = []
            list_head = []
            bodies = []
            timer = 0
            for key, s in s_list.items():

                if s != '':
                    if Gamestarted:
                        if s.lives <= 0:
                            Sounds_To_Play.append((key, 'Lose_sound'))
                            s_list[key] = ''

                    # print('sanke',key,value)
                    No_spawn_positions = []
                    No_spawn_positions.append(snack.position)
                    Last_snack_position = snack.position
                    s.move(players[key][0])
                    # GETTING HEAD POSITION
                    list_head.append((s.ID, s.body[0].position))
                    No_spawn_positions.append(s.body[0].position)
                    # GETTING BODY POSITIONS
                    for index in range(len(s.body)):
                        if index != 0:
                            bodies.append((s.ID, s.body[index].position))
                            No_spawn_positions.append(s.body[index].position)

                    # IF HEAD POSITION IS THE SAME POSITION AS THE SNACK ADD A CUBE TO THE SNAKE AND THEN CHANGE SNACK POSITION
                    if s.body[0].position == snack.position:
                        s.AddCube()
                        Sounds_To_Play.append((s.ID, 'eating_sound'))
                        snack_color = (127, 127, 127)

                        Snack_spawn = respawn_mechanic.Get_spawn_location(Grid_position_list, No_spawn_positions)
                        snack = Cube(Snack_spawn, color=snack_color)
                        No_spawn_positions.remove(Last_snack_position)
            # IF HEAD POSITION IS THE SAME AS ANY BODY POSITION RESET SNAKE
            for ID, head in list_head:
                for ID_killer, body in bodies:
                    if head == body:
                        Snake_spawn = respawn_mechanic.Get_spawn_location(Grid_position_list, No_spawn_positions)
                        s_list[ID].reset(Snake_spawn)
                        print('reset')
                        if ID != ID_killer:
                            print(ID)
                            s_list[ID_killer].kills += 1
                            print(s_list[ID_killer].name, 'has killed', s_list[ID].name)
                            Sounds_To_Play.append((ID_killer, 'kill_sound'))
                            print(s_list[ID_killer].name, 'has', s_list[ID_killer].kills, 'kills')
                            Sounds_To_Play.append((ID, 'killed_sound'))
                        else:
                            Sounds_To_Play.append((ID, 'killed_sound'))

        # DONT DRAW FOR PERFOMANCE
        if draw_Window:
            redrawWindow(Window, s_list, snack_list)

        # print('Player data',players)
        # print('Number of players',len(players))
        ################server
        message = ''
        # Put all the info of the snakes in a string
        for key, s in s_list.items():
            if s != '':
                message += str(s.snake_info) + ' '
        # print(message)
        # Put all the info of the snack in a string
        snack_message = ''
        # if we have more than one snack use a list
        ##        for key,s in snack_list.items():
        ##            snack_message+=str(s.info)+' '
        snack_message = str(snack.info)
        # Put all the sounds to play in a string
        Sounds_message = ''
        for ID, sound in Sounds_To_Play:
            Sounds_message += '=' + str(ID) + '*' + sound
        # print(Sounds_To_Play)
        # Combine all the strings into a single message
        message = message + '??' + snack_message + '??' + Game_State_Info + '??' + Sounds_message
        # print(message)
        # print(snack_message)

        # If message is not empty - send it
        if message:
            # Encode message to bytes, prepare header and convert to bytes, like for username above, then send
            message = message.encode('utf-8')
            message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
            client_socket.send(message_header + message)

        try:
            # Now we want to loop over received messages (there might be more than one) and print them
            while True:

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
                # message.split(' ')
                # We put all the inputs of the players in a dictionnary with thier name|color as key
                # players[username]=message.split(' ')
                players[username] = [message]
                # players_check=players

                # Print message
        ##                print(f'{username} > {message}')
        except IOError as e:
            # This is normal on non blocking connections - when there are no incoming data error is going to be raised
            # Some operating systems will indicate that using AGAIN, and some using WOULDBLOCK error code
            # We are going to check for both - if one of them - that's expected, means no incoming data, continue as normal
            # If we got different error code - something happened
            if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                print('Reading error: {}'.format(str(e)))
                # print(message.decode('utf-8'))
                # sys.exit()

            # We just did not receive anything
            continue

        except Exception as e:
            # Any other exception - something happened, exit
            print('Reading error: '.format(str(e)))
            print(message.decode('utf-8'))
            pass
            # sys.exit()
        except:
            pass


main()
