# This file was created by: Riley
# Riley's's edits will appear shortly...
# Riley is the best
######THANK YOU SO MUCH NINTENDO I USED ALL YOUR STUFF######

'''
goals, rules, feedback, freedom, what the verb, and will it form a sentence

battling for the most coins
same-computer multiplayer
start and end screen
'''

# all the things from the other files
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
        # the dimensions of the screen
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        # the title of the game
        pg.display.set_caption("Mario Vs Link")
        # we'll work with this later
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.running = True
        # later on we'll story game info with this
        self.load_data()
    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'images')
        self.player_img = pg.image.load(path.join(img_folder, 'link.png')).convert_alpha()
        self.map_data = []
        self.player_img2 = pg.image.load(path.join(img_folder, 'mario.png')).convert_alpha()
        self.map_data = []
        self.coin_img = pg.image.load(path.join(img_folder, 'zeldacoin.png')).convert_alpha()
        self.map_data = []
        self.coin_img2 = pg.image.load(path.join(img_folder, 'mariocoin.png')).convert_alpha()
        self.map_data = []
        self.walls_img = pg.image.load(path.join(img_folder, 'marioblock.png')).convert_alpha()
        self.map_data = []
        self.walls2_img = pg.image.load(path.join(img_folder, 'zeldablock.png')).convert_alpha()
        self.map_data = []
        #  I moved link.png to the right place
    
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
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.coins = pg.sprite.Group()
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
                    Wall(self, col, row)
                if tile == '2':
                    print("an alternate wall at", row, col)
                    Wall2(self, col, row)
                if tile == 'p':
                    self.player = Player(self, col, row)
                if tile == 'P':
                    self.player2 = Player2(self, col, row)
                    # puts the player on a specific point on the screen
                if tile == 'e':
                    print("an enemy at", row, col)
                    Enemy(self, col, row)
                if tile == 'c':
                    print("a zelda coin at", row, col)
                    Coin(self, col, row)    
                if tile == 'C':
                    print("a mario coin at", row, col)
                    Coin2(self, col, row)    
    def run(self):
        # how to run the game
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
    
    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw_text(self, surface, text, size, color, x, y):
        font_name = pg.font.match_font('times new roman')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        surface.blit(text_surface, text_rect)

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        self.draw_text(self.screen, str(self.player.moneybag), 64, YELLOW, WIDTH/2 + 300, 100)
        self.draw_text(self.screen, str(self.player2.moneybag), 64, RED, WIDTH/2 + -250, 100)
        pg.display.flip()

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
        self.draw_text(self.screen, "There are seven (7) coins in total", 36, BLACK, WIDTH/2, 360)
        self.draw_text(self.screen, "PRESS ANY KEY TO BEGIN", 72, BLACK, WIDTH/2, 410)
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
    g.show_start_screen()