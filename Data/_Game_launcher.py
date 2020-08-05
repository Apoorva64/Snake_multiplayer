import os
import sys

import Settings_Reader
import Snake_client
import pygame
import pygame as pg
import start_server
from screeninfo import get_monitors

pygame.init()
pygame.mixer.init()
Grid_factor = 4
Grid_size = [int(16 * Grid_factor), int(9 * Grid_factor)]
s_list = []
# Getting window size
m = 0
for m in get_monitors():
    print(str(m))
    print(m.width)
    print(m.height)
print((m.width // Grid_size[0]) * Grid_size[0])
print((m.height // Grid_size[1]) * Grid_size[1])

width = (m.width // Grid_size[0]) * Grid_size[0]
height = (m.height // Grid_size[1]) * Grid_size[1]
# width = 1920
# height = 1080

clock_tick_rate = 20
clock = pygame.time.Clock()
click = False

pos = pygame.mouse.get_pos()

background = pygame.image.load("Background.jpg")
win = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
click_sound = pygame.mixer.Sound(os.path.join("Sounds", "SFX Select.wav"))
hover_sound = pygame.mixer.Sound(os.path.join("Sounds", "hover.wav"))
music = pygame.mixer.music.load(os.path.join("Sounds", "music.wav"))
pygame.mixer.music.set_volume(0.075)


class button():
    text_size = 0

    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win, outline=None):
        # Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont('comicsans', self.text_size)
            text = font.render(self.text, 1, (0, 0, 0))
            win.blit(text, (int(self.x + (self.width / 2 - text.get_width() / 2)),
                            int(self.y + (self.height / 2 - text.get_height() / 2))))

    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True

        return False


pg.init()
COLOR_INACTIVE = pg.Color('lightskyblue3')
COLOR_ACTIVE = pg.Color('dodgerblue2')
FONT1 = pg.font.Font(None, 32)


class InputBox:
    # InputBox.text_size=0
    def __init__(self, x, y, w, h, text=''):
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT1.render(text, True, self.color)
        self.active = False
        self.Enter_txt = ''

    def handle_event(self, event):
        # print(self.active)
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    # print(self.text)
                    self.Enter_txt = self.text
                    self.text = ''
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT1.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, win):
        # Blit the text.
        win.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        # Blit the rect.
        pg.draw.rect(win, self.color, self.rect, 2)


def redrawWindow(win, background, PlayButton, QuitButton, OptionButton):
    win.fill((255, 255, 255))
    win.blit(pygame.transform.scale(background, (width, height)), [0, 0])
    PlayButton.draw(win, (0, 0, 0))
    QuitButton.draw(win, (0, 0, 0))
    OptionButton.draw(win, (0, 0, 0))
    font = pygame.font.SysFont('comicsans', int(width / 16))
    text = font.render("Snake", 1, (0, 0, 0))
    win.blit(text, (int(width / 2 - width / 13), int(height / 5)))


def redrawWindow2(win, background, BackButton, SpeedButton, FpsButton):
    win.fill((255, 255, 255))
    win.blit(pygame.transform.scale(background, (width, height)), [0, 0])
    BackButton.draw(win, (0, 0, 0))
    SpeedButton.draw(win, (0, 0, 0))
    FpsButton.draw(win, (0, 0, 0))
    font = pygame.font.SysFont('comicsans', int(width / 16))
    text = font.render("Options", 1, (0, 0, 0))
    win.blit(text, (int(width / 2 - width / 13), int(height / 5)))


def redrawWindowSpeed(win, background, FastButton, MediumButton, SlowButton, BackButton, Game_speed):
    win.fill((255, 255, 255))
    win.blit(pygame.transform.scale(background, (width, height)), [0, 0])
    FastButton.draw(win, (0, 0, 0))
    MediumButton.draw(win, (0, 0, 0))
    SlowButton.draw(win, (0, 0, 0))
    BackButton.draw(win, (0, 0, 0))
    font = pygame.font.SysFont('comicsans', int(width / 16))
    text = font.render("Speed     " + str(Game_speed) + 'Fps', 1, (0, 0, 0))
    win.blit(text, (int(width / 2 - width / 13), int(height / 5)))


def redrawWindowFps(win, background, BackButton, input_boxes, fps):
    win.fill((255, 255, 255))
    win.blit(pygame.transform.scale(background, (width, height)), [0, 0])
    BackButton.draw(win, (0, 0, 0))
    font = pygame.font.SysFont('comicsans', int(width / 16))
    font2 = pygame.font.SysFont('comicsans', int(width / 24))
    text_fps = font2.render(str(fps), 1, (0, 0, 0))
    text = font.render("FPS", 1, (0, 0, 0))
    win.blit(text, (int(width / 2 - width / 13), int(height / 5)))
    win.blit(text_fps, (int(width / 2 - width / 13), int(height / 2)))
    for box in input_boxes:
        box.draw(win)


def redrawWindowPlay(win, background, ServerButton, ClientButton, BackButton):
    win.fill((255, 255, 255))
    win.blit(pygame.transform.scale(background, (width, height)), [0, 0])
    ServerButton.draw(win, (0, 0, 0))
    ClientButton.draw(win, (0, 0, 0))
    BackButton.draw(win, (0, 0, 0))
    font = pygame.font.SysFont('comicsans', int(width / 16))
    text = font.render("Play", 1, (0, 0, 0))
    win.blit(text, (int(width / 2 - width / 13), int(height / 5)))


def redrawWindowServer(win, background, BackButton, ColorsButton, input_boxes, StartButton, username):
    win.fill((255, 255, 255))
    win.blit(pygame.transform.scale(background, (width, height)), [0, 0])
    BackButton.draw(win, (0, 0, 0))
    ColorsButton.draw(win, (0, 0, 0))
    StartButton.draw(win, (0, 0, 0))
    font = pygame.font.SysFont('comicsans', int(width / 16))
    font2 = pygame.font.SysFont('comicsans', int(width / 24))
    text = font.render("Server", 1, (0, 0, 0))
    text_selected_username = font2.render(username, 1, (0, 0, 0))
    text_username = font2.render("Username", 1, (100, 100, 100))
    win.blit(text, (int(width / 2 - width / 13), int(height / 5)))
    win.blit(text_username, (width / 4, height / 3))
    win.blit(text_selected_username, (width / 4, height / 2))
    for box in input_boxes:
        box.draw(win)


def redrawWindowColors(win, background, RedButton, BlueButton, GreenButton, YellowButton, PinkButton, BackButton):
    win.fill((255, 255, 255))
    win.blit(pygame.transform.scale(background, (width, height)), [0, 0])
    RedButton.draw(win, (0, 0, 0))
    BlueButton.draw(win, (0, 0, 0))
    GreenButton.draw(win, (0, 0, 0))
    YellowButton.draw(win, (0, 0, 0))
    PinkButton.draw(win, (0, 0, 0))
    BackButton.draw(win, (0, 0, 0))
    font = pygame.font.SysFont('comicsans', int(width / 16))
    text = font.render("Colors", 1, (0, 0, 0))
    win.blit(text, (int(width / 2 - width / 13), int(height / 5)))


def redrawWindowClient(win, background, BackButton, ColorsButton, input_boxes, StartButton, ip, username):
    win.fill((255, 255, 255))
    win.blit(pygame.transform.scale(background, (width, height)), [0, 0])
    BackButton.draw(win, (0, 0, 0))
    ColorsButton.draw(win, (0, 0, 0))
    StartButton.draw(win, (0, 0, 0))
    font = pygame.font.SysFont('comicsans', int(width / 16))
    font2 = pygame.font.SysFont('comicsans', int(width / 24))
    text = font.render("Client", 1, (0, 0, 0))
    text_selected_username = font2.render(username, 1, (0, 0, 0))
    text_selected_ip = font2.render(ip, 1, (0, 0, 0))
    text_username = font2.render("Username", 1, (100, 100, 100))
    text_ip = font2.render("IP Adress", 1, (100, 100, 100))
    win.blit(text, (int(width / 2 - width / 13), int(height / 5)))
    win.blit(text_username, (width / 4, height / 3))
    win.blit(text_selected_username, (width / 4, height / 2.7))
    win.blit(text_ip, (width / 4, height / 3 * (3 / 2)))
    win.blit(text_selected_ip, (width / 4, height / 1.8))
    for box in input_boxes:
        box.draw(win)


def menu():
    run = True
    PlayButton = button((255, 255, 255), width / 2 - width / 15, height / 3, width / 10, height / 10, "Play")
    QuitButton = button((255, 255, 255), width / 2 - width / 15, height / 3 * 2, width / 10, height / 10, "Quit")
    OptionButton = button((255, 255, 255), width / 2 - width / 15, height / 3 * (3 / 2), width / 10, height / 10,
                          "Options")
    win = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
    ##    pygame.mixer.music.play(-1)
    while run:
        redrawWindow(win, background, PlayButton, QuitButton, OptionButton)
        pygame.display.update()
        pos = pygame.mouse.get_pos()
        # print(pos)

        pygame.display.flip()
        clock.tick(clock_tick_rate)
        pygame.time.delay(30)

        click_start = False
        click_quit = False
        click_option = False
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if PlayButton.isOver(pos) and event.button == 1:
                    click_start = True
                if click_start:
                    click_sound.play()
                    menuPlay()

                if QuitButton.isOver(pos) and event.button == 1:
                    click_quit = True
                if click_quit:
                    click_sound.play()
                    pygame.quit()
                    sys.exit()

                if OptionButton.isOver(pos) and event.button == 1:
                    click_option = True
                if click_option:
                    click_sound.play()
                    menuOption()

            if event.type == pygame.MOUSEMOTION:
                if PlayButton.isOver(pos):
                    PlayButton.color = (0, 255, 0)

                else:
                    PlayButton.color = (255, 255, 255)

                if QuitButton.isOver(pos):
                    QuitButton.color = (255, 0, 0)
                    if not pygame.mixer.get_busy():
                        hover_sound.play()
                else:
                    QuitButton.color = (255, 255, 255)

                if OptionButton.isOver(pos):
                    OptionButton.color = (255, 255, 0)
                    if not pygame.mixer.get_busy():
                        hover_sound.play()
                else:
                    OptionButton.color = (255, 255, 255)


button.text_size = int(width / 32)


def menuOption():
    run = True
    BackButton = button((255, 255, 255), width / 2 - width / 15, height / 3 * 2, width / 10, height / 10, "Back")
    SpeedButton = button((255, 255, 255), width / 2 - width / 15, height / 3, width / 10, height / 10, "Speed")
    FpsButton = button((255, 255, 255), width / 2 - width / 15, height / 3 * (3 / 2), width / 10, height / 10, "FPS")
    win = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
    settings_server = Settings_Reader.Read_Settings_Server()
    # settings_client = Settings_Reader.Read_Settings_Client()
    fps = settings_server['Server_Update_Fps']
    Game_speed = settings_server['Game_Update_Fps']
    while run:
        redrawWindow2(win, background, BackButton, SpeedButton, FpsButton)
        pygame.display.update()
        Mouse_position = pygame.mouse.get_pos()
        # print(Mouse_position)

        pygame.display.flip()
        clock.tick(clock_tick_rate)
        pygame.time.delay(30)

        click_back = False
        click_speed = False
        click_fps = False
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if SpeedButton.isOver(Mouse_position) and event.button == 1:
                    click_speed = True
                if click_speed:
                    click_sound.play()
                    Game_speed = menuSpeed(win, Game_speed)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if BackButton.isOver(Mouse_position) and event.button == 1:
                    click_back = True
                if click_back:
                    click_sound.play()
                    run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if FpsButton.isOver(Mouse_position) and event.button == 1:
                    # click_speed = True

                    # if click_speed == True:
                    click_sound.play()
                    fps = menuFps(fps)

            if event.type == pygame.MOUSEMOTION:
                if BackButton.isOver(Mouse_position):
                    BackButton.color = (255, 0, 0)
                    if not pygame.mixer.get_busy():
                        hover_sound.play()
                else:
                    BackButton.color = (255, 255, 255)

            if event.type == pygame.MOUSEMOTION:
                if FpsButton.isOver(Mouse_position):
                    FpsButton.color = (255, 255, 0)
                    if not pygame.mixer.get_busy():
                        hover_sound.play()
                else:
                    FpsButton.color = (255, 255, 255)

            if event.type == pygame.MOUSEMOTION:
                if SpeedButton.isOver(Mouse_position):
                    SpeedButton.color = (0, 255, 0)
                    if not pygame.mixer.get_busy():
                        hover_sound.play()
                else:
                    SpeedButton.color = (255, 255, 255)
    Settings_Reader.Write_Settings_Server(Game_speed, fps, settings_server['Background_Color'],
                                          settings_server['Enable_Draw'])


def menuSpeed(win, Game_speed):
    # print('started')
    run = True
    SlowButton = button((255, 255, 255), width / 2 - width / 15, height / 3 * 2, width / 10, height / 10, "Slow")
    FastButton = button((255, 255, 255), width / 2 - width / 15, height / 3, width / 10, height / 10, "Fast")
    MediumButton = button((255, 255, 255), width / 2 - width / 15, height / 3 * (3 / 2), width / 10, height / 10,
                          "Medium")
    BackButton = button((255, 255, 255), width / 3 * 2, height / 3 * (3 / 2), width / 10, height / 10, "Back")
    # input_box1 = InputBox(width/2-width/15, height/3, width/10, height/10)
    ##    fps = input_box1.text
    ##    input_box2 = InputBox(width/2-width/15, height/3*(3/2), width/10, height/10)
    ##    input_boxes = [input_box1]#, input_box2 ]
    ##    done = False
    ##
    ##    while not done:
    ##    return input_boxes
    # win = pygame.display.set_mode((width,height))
    while run:
        redrawWindowSpeed(win, background, FastButton, MediumButton, SlowButton, BackButton, Game_speed)
        pygame.display.update()
        pos = pygame.mouse.get_pos()
        # print(pos)

        pygame.display.flip()
        clock.tick(clock_tick_rate)
        pygame.time.delay(30)

        click_fast = False
        click_medium = False
        click_slow = False
        click_back = False

        win.fill((30, 30, 30))
        win.blit(pygame.transform.scale(background, (width, height)), [0, 0])
        ##        for box in input_boxes:
        ##            box.draw(win)

        for event in pygame.event.get():
            # for box in input_boxes:
            #     box.handle_event(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if FastButton.isOver(pos) and event.button == 1:
                    # click_fast = True
                    # if click_fast == True:
                    click_sound.play()
                    Game_speed = 25
                    pass

            if event.type == pygame.MOUSEBUTTONDOWN:
                if MediumButton.isOver(pos) and event.button == 1:
                    # click_medium = True
                    # if click_medium == True:
                    click_sound.play()
                    Game_speed = 15
                    pass

            if event.type == pygame.MOUSEBUTTONDOWN:
                if SlowButton.isOver(pos) and event.button == 1:
                    # click_slow = True
                    # if click_slow == True:
                    click_sound.play()
                    Game_speed = 10
                    pass

            if event.type == pygame.MOUSEBUTTONDOWN:
                if BackButton.isOver(pos) and event.button == 1:
                    click_back = True
                if click_back:
                    click_sound.play()
                    run = False

            if event.type == pygame.MOUSEMOTION:
                if BackButton.isOver(pos):
                    BackButton.color = (255, 0, 0)
                    if not pygame.mixer.get_busy():
                        hover_sound.play()
                else:
                    BackButton.color = (255, 255, 255)
    ##            for box in input_boxes:
    ##                box.handle_event(event)

    ##        for box in input_boxes:
    ##            #print(box)
    ##            box.update()

    # print('started')
    return Game_speed


def menuFps(fps):
    run = True
    BackButton = button((255, 255, 255), width / 3 * 2, height / 3 * (3 / 2), width / 10, height / 10, "Back")
    input_box1 = InputBox(width / 2 - width / 15, height / 3, width / 10, height / 10)

    ##    input_box2 = InputBox(width/2-width/15, height/3*(3/2), width/10, height/10)
    input_boxes = [input_box1]  # , input_box2 ]
    ##    done = False
    ##
    ##    while not done:
    ##    return input_boxes
    # win = pygame.display.set_mode((width,height))
    while run:
        # print(input_box1.Enter_txt)
        if input_box1.Enter_txt != '':
            fps = int(input_box1.Enter_txt)
        redrawWindowFps(win, background, BackButton, input_boxes, fps)
        pygame.display.update()
        pos = pygame.mouse.get_pos()
        # print(pos)

        pygame.display.flip()
        clock.tick(clock_tick_rate)
        pygame.time.delay(30)

        click_back = False

        ##        win.fill((30, 30, 30))
        ##        win.blit(pygame.transform.scale(background, (width,height)), [0, 0])
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False

            for box in input_boxes:
                box.handle_event(event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if BackButton.isOver(pos) and event.button == 1:
                    click_back = True
                if click_back == True:
                    click_sound.play()
                    run = False

            if event.type == pygame.MOUSEMOTION:
                if BackButton.isOver(pos):
                    BackButton.color = (255, 0, 0)
                    if not pygame.mixer.get_busy():
                        hover_sound.play()
                else:
                    BackButton.color = (255, 255, 255)
    ##        for box in input_boxes:
    ##            box.draw(win)
    return fps


def menuPlay():
    run = True
    BackButton = button((255, 255, 255), width / 2 - width / 15, height / 3 * 2, width / 10, height / 10, "Back")
    ServerButton = button((255, 255, 255), width / 2 - width / 15, height / 3, width / 10, height / 10, "Server")
    ClientButton = button((255, 255, 255), width / 2 - width / 15, height / 3 * (3 / 2), width / 10, height / 10,
                          "Client")
    win = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
    while run:
        redrawWindowPlay(win, background, ServerButton, ClientButton, BackButton)
        pygame.display.update()
        pos = pygame.mouse.get_pos()

        pygame.display.flip()
        clock.tick(clock_tick_rate)
        pygame.time.delay(30)

        click_server = False
        click_client = False
        click_back = False

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if ServerButton.isOver(pos) and event.button == 1:
                    click_server = True
                if click_server:
                    click_sound.play()
                    menuServer()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if BackButton.isOver(pos) and event.button == 1:
                    click_back = True
                if click_back:
                    click_sound.play()
                    run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if ClientButton.isOver(pos) and event.button == 1:
                    # click_client = True
                    menuClient()
                    # if click_client == True:
                    click_sound.play()
                    pass

            if event.type == pygame.MOUSEMOTION:
                if BackButton.isOver(pos):
                    BackButton.color = (255, 0, 0)
                    if not pygame.mixer.get_busy():
                        hover_sound.play()
                else:
                    BackButton.color = (255, 255, 255)

                if ServerButton.isOver(pos):
                    ServerButton.color = (0, 255, 0)
                    if not pygame.mixer.get_busy():
                        hover_sound.play()
                else:
                    ServerButton.color = (255, 255, 255)

                if ClientButton.isOver(pos):
                    ClientButton.color = (255, 255, 0)
                    if not pygame.mixer.get_busy():
                        hover_sound.play()
                else:
                    ClientButton.color = (255, 255, 255)


def menuServer():
    run = True
    BackButton = button((255, 255, 255), width / 3 * 2, height / 3 * (3 / 2), width / 10, height / 10, "Back")
    input_box1 = InputBox(width / 2 - width / 15, height / 3, width / 10, height / 10)
    ColorsButton = button((255, 255, 255), width / 2 - width / 15, height / 3 * (3 / 2), width / 10, height / 10,
                          "Colors")
    StartButton = button((255, 255, 255), width / 2 - width / 15, height / 3 * 2, width / 10, height / 10, "Start")

    input_boxes = [input_box1]
    # Color=(255,0,255)
    username = 'Host'
    Color = (0, 0, 255)
    while run:
        # print(input_box1.Enter_txt)
        if input_box1.Enter_txt != '':
            username = input_box1.Enter_txt

        redrawWindowServer(win, background, BackButton, ColorsButton, input_boxes, StartButton, username)
        pygame.display.update()
        pos = pygame.mouse.get_pos()
        # print(pos)

        pygame.display.flip()
        clock.tick(clock_tick_rate)
        pygame.time.delay(30)

        click_back = False
        click_colors = False
        click_start = False

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False

            for box in input_boxes:
                box.handle_event(event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if BackButton.isOver(pos) and event.button == 1:
                    click_back = True
                if click_back:
                    click_sound.play()
                    run = False

            if event.type == pygame.MOUSEMOTION:
                if BackButton.isOver(pos):
                    BackButton.color = (255, 0, 0)
                else:
                    BackButton.color = (255, 255, 255)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if ColorsButton.isOver(pos) and event.button == 1:
                    click_colors = True
                if click_colors:
                    click_sound.play()
                    Color = menuColorsServer()

            # if event.type == pygame.MOUSEMOTION:
            if ColorsButton.isOver(pos):
                ColorsButton.color = (0, 255, 255)
                if not pygame.mixer.get_busy():
                    hover_sound.play()
            else:
                ColorsButton.color = Color

            if event.type == pygame.MOUSEBUTTONDOWN:
                if StartButton.isOver(pos) and event.button == 1:
                    click_start = True
                    # print('started')
                    # lauching server
                    start_server.main(username=username,
                                      color=str(Color[0]) + ';' + str(Color[1]) + ';' + str(Color[2]))
                if click_start:
                    click_sound.play()
                    pass

            if event.type == pygame.MOUSEMOTION:
                if StartButton.isOver(pos):
                    StartButton.color = (0, 255, 0)
                    if not pygame.mixer.get_busy():
                        hover_sound.play()
                else:
                    StartButton.color = (255, 255, 255)


def menuColorsServer():
    run = True
    RedButton = button((255, 255, 255), width / 3 - width / 15, height / 3 * 2, width / 10, height / 10, "Red")
    BlueButton = button((255, 255, 255), width / 3 - width / 15, height / 3, width / 10, height / 10, "Blue")
    GreenButton = button((255, 255, 255), width / 3 - width / 15, height / 3 * (3 / 2), width / 10, height / 10,
                         "Green")
    YellowButton = button((255, 255, 255), width / 2 + width / 15, height / 3, width / 10, height / 10, "Yellow")
    PinkButton = button((255, 255, 255), width / 2 + width / 15, height / 3 * (3 / 2), width / 10, height / 10, "Pink")
    BackButton = button((255, 255, 255), width / 2 + width / 15, height / 3 * 2, width / 10, height / 10, "Back")
    win = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
    Color = (0, 0, 255)
    while run:
        redrawWindowColors(win, background, RedButton, BlueButton, GreenButton, YellowButton, PinkButton, BackButton)
        pygame.display.update()
        pos = pygame.mouse.get_pos()
        # print(pos)

        pygame.display.flip()
        clock.tick(clock_tick_rate)
        pygame.time.delay(30)

        click_red = False
        click_blue = False
        click_green = False
        click_yellow = False
        click_pink = False
        click_back = False

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # menuServer()
                    run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if RedButton.isOver(pos) and event.button == 1:
                    # click_red == True and click_blue == False and  click_green == False and click_yellow == False and click_pink == False
                    # if click_red == True:
                    click_sound.play()
                    Color = (255, 0, 0)

                elif BlueButton.isOver(pos) and event.button == 1:
                    # click_red == False and click_blue == True and  click_green == False and click_yellow == False and click_pink == False
                    # if click_blue == True:
                    click_sound.play()
                    Color = (0, 0, 200)

                elif GreenButton.isOver(pos) and event.button == 1:
                    # click_red == False and click_blue == False and  click_green == True and click_yellow == False and click_pink == False
                    # if click_green == True:
                    click_sound.play()
                    Color = (0, 255, 0)

                elif YellowButton.isOver(pos) and event.button == 1:
                    # click_red == False and click_blue == False and  click_green == False and click_yellow == True and click_pink == False
                    # if click_yellow == True:
                    click_sound.play()
                    Color = (255, 255, 0)

                elif PinkButton.isOver(pos) and event.button == 1:
                    # click_red == False and click_blue == False and  click_green == False and click_yellow == False and click_pink == True
                    # if click_pink == True:
                    click_sound.play()
                    Color = (255, 0, 255)

            if event.type == pygame.MOUSEMOTION:
                if RedButton.isOver(pos):
                    RedButton.color = (255, 0, 0)
                else:
                    RedButton.color = (255, 255, 255)

                if BlueButton.isOver(pos):
                    BlueButton.color = (0, 0, 200)
                else:
                    BlueButton.color = (255, 255, 255)

                if GreenButton.isOver(pos):
                    GreenButton.color = (0, 255, 0)
                else:
                    GreenButton.color = (255, 255, 255)

                if YellowButton.isOver(pos):
                    YellowButton.color = (255, 255, 0)
                else:
                    YellowButton.color = (255, 255, 255)

                if PinkButton.isOver(pos):
                    PinkButton.color = (255, 0, 255)
                else:
                    PinkButton.color = (255, 255, 255)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if BackButton.isOver(pos) and event.button == 1:
                    click_back = True
                if click_back == True:
                    click_sound.play()
                    run = False
                    # menuServer()

            if event.type == pygame.MOUSEMOTION:
                if BackButton.isOver(pos):
                    BackButton.color = (169, 169, 169)
                else:
                    BackButton.color = (255, 255, 255)
    # print(Color)
    return Color


def menuColorsClient():
    run = True
    RedButton = button((255, 255, 255), width / 3 - width / 15, height / 3 * 2, width / 10, height / 10, "Red")
    BlueButton = button((255, 255, 255), width / 3 - width / 15, height / 3, width / 10, height / 10, "Blue")
    GreenButton = button((255, 255, 255), width / 3 - width / 15, height / 3 * (3 / 2), width / 10, height / 10,
                         "Green")
    YellowButton = button((255, 255, 255), width / 2 + width / 15, height / 3, width / 10, height / 10, "Yellow")
    PinkButton = button((255, 255, 255), width / 2 + width / 15, height / 3 * (3 / 2), width / 10, height / 10, "Pink")
    BackButton = button((255, 255, 255), width / 2 + width / 15, height / 3 * 2, width / 10, height / 10, "Back")
    win = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
    Color = (0, 0, 255)
    while run:
        redrawWindowColors(win, background, RedButton, BlueButton, GreenButton, YellowButton, PinkButton, BackButton)
        pygame.display.update()
        pos = pygame.mouse.get_pos()
        # print(pos)

        pygame.display.flip()
        clock.tick(clock_tick_rate)
        pygame.time.delay(30)

        click_red = False
        click_blue = False
        click_green = False
        click_yellow = False
        click_pink = False
        click_back = False

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # menuClient()
                    run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if RedButton.isOver(pos) and event.button == 1:
                    # click_red == True and click_blue == False and  click_green == False and click_yellow == False and click_pink == False
                    # if click_red == True:
                    click_sound.play()
                    Color = (255, 0, 0)

                elif BlueButton.isOver(pos) and event.button == 1:
                    # click_red == False and click_blue == True and  click_green == False and click_yellow == False and click_pink == False
                    # if click_blue == True:
                    click_sound.play()
                    Color = (0, 0, 200)

                elif GreenButton.isOver(pos) and event.button == 1:
                    # click_red == False and click_blue == False and  click_green == True and click_yellow == False and click_pink == False
                    # if click_green == True:
                    click_sound.play()
                    Color = (0, 255, 0)

                elif YellowButton.isOver(pos) and event.button == 1:
                    # click_red == False and click_blue == False and  click_green == False and click_yellow == True and click_pink == False
                    # if click_yellow == True:
                    click_sound.play()
                    Color = (255, 255, 0)

                elif PinkButton.isOver(pos) and event.button == 1:
                    # click_red == False and click_blue == False and  click_green == False and click_yellow == False and click_pink == True
                    # if click_pink == True:
                    click_sound.play()
                    Color = (255, 0, 255)

            if event.type == pygame.MOUSEMOTION:
                if RedButton.isOver(pos):
                    RedButton.color = (255, 0, 0)
                else:
                    RedButton.color = (255, 255, 255)

                if BlueButton.isOver(pos):
                    BlueButton.color = (0, 0, 200)
                else:
                    BlueButton.color = (255, 255, 255)

                if GreenButton.isOver(pos):
                    GreenButton.color = (0, 255, 0)
                else:
                    GreenButton.color = (255, 255, 255)

                if YellowButton.isOver(pos):
                    YellowButton.color = (255, 255, 0)
                else:
                    YellowButton.color = (255, 255, 255)

                if PinkButton.isOver(pos):
                    PinkButton.color = (255, 0, 255)
                else:
                    PinkButton.color = (255, 255, 255)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if BackButton.isOver(pos) and event.button == 1:
                    click_back = True
                if click_back == True:
                    click_sound.play()
                    run = False

            if event.type == pygame.MOUSEMOTION:
                if BackButton.isOver(pos):
                    BackButton.color = (169, 169, 169)
                else:
                    BackButton.color = (255, 255, 255)
    return Color


def menuClient():
    run = True
    BackButton = button((255, 255, 255), width / 3 * 2, height / 3 * (3 / 2), width / 10, height / 10, "Back")
    input_box1 = InputBox(width / 2 - width / 15, height / 3, width / 10, height / 10)
    input_box2 = InputBox(width / 2 - width / 15, height / 3 * (3 / 2), width / 10, height / 10)
    ColorsButton = button((255, 255, 255), width / 2 - width / 15, height / 3 * 2, width / 10, height / 10, "Colors")
    StartButton = button((255, 255, 255), width / 3 * 2, height / 3 * 2, width / 10, height / 10, "Start")

    input_boxes = [input_box1, input_box2]
    Color = (155, 0, 255)
    username = 'Client'
    ip = '127.0.0.1'
    Color = (0, 0, 255)
    while run:
        # print(input_box1.Enter_txt)
        if input_box1.Enter_txt != '':
            username = input_box1.Enter_txt
        if input_box2.Enter_txt != '':
            ip = input_box2.Enter_txt
        redrawWindowClient(win, background, BackButton, ColorsButton, input_boxes, StartButton, ip, username)
        pygame.display.update()
        pos = pygame.mouse.get_pos()
        # print(pos)

        pygame.display.flip()
        clock.tick(clock_tick_rate)
        pygame.time.delay(30)

        click_back = False
        click_colors = False
        click_start = False

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False

            for box in input_boxes:
                box.handle_event(event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if BackButton.isOver(pos) and event.button == 1:
                    click_back = True
                if click_back == True:
                    click_sound.play()
                    run = False

            if event.type == pygame.MOUSEMOTION:
                if BackButton.isOver(pos):
                    BackButton.color = (255, 0, 0)
                    if not pygame.mixer.get_busy():
                        hover_sound.play()
                else:
                    BackButton.color = (255, 255, 255)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if ColorsButton.isOver(pos) and event.button == 1:
                    click_colors = True
                if click_colors == True:
                    click_sound.play()
                    Color = menuColorsClient()

            # if event.type == pygame.MOUSEMOTION:
            if ColorsButton.isOver(pos):
                ColorsButton.color = (0, 255, 255)
                if not pygame.mixer.get_busy():
                    hover_sound.play()
            else:
                ColorsButton.color = Color

            if event.type == pygame.MOUSEBUTTONDOWN:
                if StartButton.isOver(pos) and event.button == 1:
                    click_start = True
                    # if click_start == True:
                    click_sound.play()
                    Snake_client.main(ip, username, str(Color[0]) + ';' + str(Color[1]) + ';' + str(Color[2]))
                    pass

            if event.type == pygame.MOUSEMOTION:
                if StartButton.isOver(pos):
                    StartButton.color = (0, 255, 0)
                    if not pygame.mixer.get_busy():
                        hover_sound.play()
                else:
                    StartButton.color = (255, 255, 255)


pygame.mixer.music.play(-1)
menu()
##menuClient()
