# This file was created by: Riley
# Riley's's edits will appear shortly...
# Riley is the best
######THANK YOU SO MUCH NINTENDO I USED ALL YOUR STUFF######
######I ALSO USED A LOT OF MR. COZORT'S CODE THANKS FOR THAT######
######I ALSO USED CHATGPT FOR SOME OF THE MUSIC STUFF THAT DIDN'T WORK######

'''
goals, rules, feedback, freedom, what the verb, and will it form a sentence
'''


'''
ALPHA GOALS
getting coins faster than opponent
same-computer multiplayer
start screen to show how to play
'''

'''
BETA GOALS
add awesome music to get the player happy
sound effects for collecting coins
'''

'''
FINAL GOALS
have more music soundtracks
random background music
'''


# all the things from the other files
import time
import pygame as pg
from settings import *
from sprites import *
import sys
from random import randint
from os import path

# create a game class 
class Game:
    # behold the methods...
    def __init__(self):
        pg.init()
        pg.mixer.init()
        # the dimensions of the screen
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        # the title of the game
        pg.display.set_caption("Mario Vs Link")
        # eeewe'll work with this later
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.running = True
        # later on we'll story game info with this
        self.load_data()
    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'images')
        self.snd_folder = path.join(game_folder, 'sounds')
        # Idk why I had to add "self"
        self.player_img = pg.image.load(path.join(img_folder, 'animatedlink.png')).convert_alpha()
        self.map_data = []
        self.player_img2 = pg.image.load(path.join(img_folder, 'animatedmario.png')).convert_alpha()
        self.map_data = []
        self.coin_img = pg.image.load(path.join(img_folder, 'zeldacoin.png')).convert_alpha()
        self.map_data = []
        self.coin_img2 = pg.image.load(path.join(img_folder, 'mariocoin.png')).convert_alpha()
        self.map_data = []
        self.walls_img = pg.image.load(path.join(img_folder, 'marioblock.png')).convert_alpha()
        self.map_data = []
        self.walls2_img = pg.image.load(path.join(img_folder, 'zeldablock.png')).convert_alpha()
        self.map_data = []
        self.goomba_img = pg.image.load(path.join(img_folder, 'goomba.png')).convert_alpha()
        self.map_data = []
        # did a lot of different images
    
        '''
        The with statement is a context manager in Python. 
        It is used to ensure that a resource is properly closed or released 
        after it is used. This can help to prevent errors and leaks.
        '''
        with open(path.join(game_folder, 'map.txt'), 'rt') as f:
            for line in f:
                print(line)
                self.map_data.append(line)
    # def load_data(self):
    #     game_folder = path.dirname(__file__)
    #     self.map_data = []
    #     '''
    #     The with statement is a context manager in Python. 
    #     It is used to ensure that a resource is properly closed or released 
    #     after it is used. This can help to prevent errors and leaks.
    #     '''
    #     with open(path.join(game_folder, 'map.txt'), 'rt') as f:
    #         for line in f:
    #             print(line)
    #             self.map_data.append(line)
    #             print(self.map_data)
    def new(self):
        pg.mixer.music.load(path.join(self.snd_folder, 'latesummerrun.mp3'))
        # this music I downloaded but added my own sounds
        # the "mmmmmmm" was my voice
        # this is from a podcast "Chasing Scratch"
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.fakewalls = pg.sprite.Group()
        self.pew_pews = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        # self.player = Player(self, 10, 10)
        # self.all_sprites.add(self.player)
        # for x in range(10, 20):
        #     Wall(self, x, 5)
        for row, tiles in enumerate(self.map_data):
            print(row)
            for col, tile in enumerate(tiles):
                print(col)
                if tile == '1':
                    print("a wall at", row, col)
                    ZeldaWall(self, col, row)
                if tile == '2':
                    print("an alternate wall at", row, col)
                    MarioWall(self, col, row)
                if tile == '3':
                    print("an fake wall at", row, col)
                    FakeWall(self, col, row)
                if tile == '4':
                    print("an alternate fake wall at", row, col)
                    FakeWall2(self, col, row)
                if tile == 'L':
                    self.playerlink = PlayerLink(self, col, row)
                if tile == 'M':
                    self.playermario = PlayerMario(self, col, row)
                    # puts the player on a specific point on the screen
                if tile == 'c':
                    print("a zelda coin at", row, col)
                    ZeldaCoin(self, col, row)    
                if tile == 'C':
                    print("a mario coin at", row, col)
                    MarioCoin(self, col, row)
                if tile == 'g':
                    print("a goomba at", row, col)
                    Mob(self, col, row)
        # soooo many sprites
                        
    def run(self):
        # how to run the game
        pg.mixer.music.play(loops=-1)
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            # this is input
            self.events()
            # this is processing
            self.update()
            # this output
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()
    # methods
    def input(self): 
        pass
    def update(self):
        self.all_sprites.update()
        if self.playerlink.moneybag == 0:
            self.playing = False
        if self.playermario.moneybag == 0:
            self.playing = False
    
    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))
            # the grid is invisible

    def draw_text(self, surface, text, size, color, x, y):
        font_name = pg.font.match_font('times new roman')
        # idk why I like times new roman
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        surface.blit(text_surface, text_rect)

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        self.draw_text(self.screen, str(self.playerlink.moneybag), 144, YELLOW, WIDTH/2 + 300, 85)
        self.draw_text(self.screen, str(self.playermario.moneybag), 144, RED, WIDTH/2 + -250, 85)
        pg.display.flip()
        # puts everything on the screen

    def events(self):
            # THE OLD WAY OF GETTING THINGS TO MOVE
            # listening for events
            for event in pg.event.get():
                # when you hit the red x the window closes the game ends
                if event.type == pg.QUIT:
                    self.quit()
                    print("the game has ended..")
                # keyboard events
                # if event.type == pg.KEYDOWN:
                #     if event.key == pg.K_LEFT:
                #         self.player.move(dx=-1)
                # if event.type == pg.KEYDOWN:
                #     if event.key == pg.K_RIGHT:
                #         self.player.move(dx=1)
                # if event.type == pg.KEYDOWN:
                #     if event.key == pg.K_UP:
                #         self.player.move(dy=-1)
                # if event.type == pg.KEYDOWN:
                #     if event.key == pg.K_DOWN:
                #         self.player.move(dy=1)
    def show_start_screen(self):
        self.screen.fill(BGCOLOR)
        self.draw_text(self.screen, "MARIO VS LINK", 96, BLACK, WIDTH/2, 90)
        self.draw_text(self.screen, "Mario: use WASD to move", 48, RED, WIDTH/2, 210)
        self.draw_text(self.screen, "Link: use arrows to move", 48, YELLOW, WIDTH/2, 260)
        self.draw_text(self.screen, "The goal is to collect all the coins the fastest", 36, BLACK, WIDTH/2, 325)
        self.draw_text(self.screen, "Whoever gets to zero (0) coins the fastest wins", 36, BLACK, WIDTH/2, 360)
        self.draw_text(self.screen, "There are seven (7) coins in total", 36, BLACK, WIDTH/2, 360 + 35)
        self.draw_text(self.screen, "PRESS ANY KEY TO BEGIN", 72, BLACK, WIDTH/2, 410 + 35)
        pg.display.flip()
        self.wait_for_key()
        # I think the start screen took the longest

    def show_go_screen1(self):
        if not self.running:
            return
        self.screen.fill(BGCOLOR)
        self.draw_text(self.screen, "LINK WINS", 24, BLACK, WIDTH/2, HEIGHT/2)
        pg.display.flip()
        self.wait_for_key()
    
    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.KEYUP:
                    waiting = False
####################### Instantiate game... ###################
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
# starts the game