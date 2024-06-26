# This file was created by: Riley Boynton
# Appreciation to Chris Bradfield
# Also to Mr. Cozort
import pygame as pg
from settings import *
from utils import *
from os import path
from random import choice
from random import randint

vec =pg.math.Vector2

# needed for animated sprite
SPRITESHEET = "animatedlink.png"
# needed for animated sprite

# needed for animated sprite
class Spritesheet:
    # utility class for loading and parsing spritesheets
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        # grab an image out of a larger spritesheet
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        image = pg.transform.scale(image, (width * 1, height * 1))
        return image
       

game_folder = path.dirname(__file__)
img_folder = path.join(game_folder, 'images')
# write a player class
class PlayerLink(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.zelda_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.spritesheet = Spritesheet(path.join(img_folder, 'animatedlink.png'))
        self.load_images()
        # self.image.fill(GREEN)
        self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()
        self.vx, self.vy = 5, 5
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.moneybag = 7
         # needed for animated sprite
        self.current_frame = 0
        # needed for animated sprite
        self.last_update = 0
        self.material = True
        # needed for animated sprite
        self.jumping = False
        # needed for animated sprite
        self.walking = False

    def load_images(self):
        self.standing_frames = [self.spritesheet.get_image(0,0, 32, 32), 
                                self.spritesheet.get_image(32,0, 32, 32)]
     
    def animate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 350:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
            bottom = self.rect.bottom
            self.image = self.standing_frames[self.current_frame]
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom

    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.vx = -PLAYER_SPEED * TILESIZE
        if keys[pg.K_RIGHT]:
            self.vx = PLAYER_SPEED * TILESIZE
        if keys[pg.K_UP]:
            self.vy = -PLAYER_SPEED * TILESIZE
        if keys[pg.K_DOWN]:
            self.vy = PLAYER_SPEED * TILESIZE
            
    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False )
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False )
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y
    def collide_with_Enemy(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.Enemy, False )
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.Enemy, False )
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y
    def collide_with_group(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            if str(hits[0].__class__.__name__) == "ZeldaCoin":
                self.moneybag -= 1
                zeldacoin_sound = pg.mixer.Sound("zeldacoinsound.mp3")
                zeldacoin_sound.play()  
            if str(hits[0].__class__.__name__) == "FreezeItem":
                self.game.timefreezelink = True
                freeze_sound = pg.mixer.Sound("freezesound.mp3")
                freeze_sound.play()
    # old motion
    # def move(self, dx=0, dy=0):
    #     self.x += dx
    #     self.y += dy
    def animate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 350:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
            bottom = self.rect.bottom
            self.image = self.standing_frames[self.current_frame]
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom

    # UPDATE THE UPDATE
    def update(self):
        self.animate()
        # self.rect.x = self.x
        # self.rect.y = self.y
        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')
        self.collide_with_group(self.game.coins, True)
        self.collide_with_group(self.game.freezes, True)
        # self.rect.x = self.x * TILESIZE
        # self.rect.y = self.y * TILESIZE



class PlayerMario(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mario_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.spritesheet = Spritesheet(path.join(img_folder, 'superanimatedmario.png'))
        self.load_images()
        # self.image.fill(GREEN)
        self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()
        self.vx, self.vy = 5, 5
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.moneybag = 7
         # needed for animated sprite
        self.current_frame = 0
        # needed for animated sprite
        self.last_update = 0
        self.material = True
        # needed for animated sprite
        self.jumping = False
        # needed for animated sprite
        self.walking = False

    def load_images(self):
        self.standing_frames = [
                                self.spritesheet.get_image(0,0, 32, 32), 
                                self.spritesheet.get_image(32,0, 32, 32),
                                self.spritesheet.get_image(64,0, 32, 32),
                                self.spritesheet.get_image(96,0, 32, 32),
                                self.spritesheet.get_image(128,0, 32, 32),
                                self.spritesheet.get_image(160,0, 32, 32),
                                self.spritesheet.get_image(192,0, 32, 32),
                                self.spritesheet.get_image(224,0, 32, 32)]
     
    def animate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 150:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
            bottom = self.rect.bottom
            self.image = self.standing_frames[self.current_frame]
            self.rect.bottom = bottom

    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.vx = -PLAYER_SPEED * TILESIZE
        if keys[pg.K_d]:
            self.vx = PLAYER_SPEED * TILESIZE
        if keys[pg.K_w]:
            self.vy = -PLAYER_SPEED * TILESIZE
        if keys[pg.K_s]:
            self.vy = PLAYER_SPEED * TILESIZE
        # if keys[pg.K_e]:
        #     self.pew()
            
    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False )
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False )
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y
    def collide_with_Enemy(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.Enemy, False )
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.Enemy, False )
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y
    def collide_with_group(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            if str(hits[0].__class__.__name__) == "MarioCoin":
                self.moneybag -= 1
                coin_sound = pg.mixer.Sound("mariocoinsound.mp3")
                coin_sound.play()
            if str(hits[0].__class__.__name__) == "FreezeItem":
                self.game.timefreezemario = True
                freeze_sound = pg.mixer.Sound("freezesound.mp3")
                freeze_sound.play()
    # old motion
    # def move(self, dx=0, dy=0):
    #     self.x += dx
    #     self.y += dy


    # UPDATE THE UPDATE
    def update(self):
        self.animate()
        # self.rect.x = self.x
        # self.rect.y = self.y
        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')
        self.collide_with_group(self.game.coins, True)
        self.collide_with_group(self.game.freezes, True)
        # self.rect.x = self.x * TILESIZE
        # self.rect.y = self.y * TILESIZE

class ZeldaWall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls, game.zelda_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = game.walls2_img
        # self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.speed = 0
    def update(self):
        # self.rect.x += 1
        self.rect.x += TILESIZE * self.speed
        # self.rect.y += TILESIZE * self.speed
        if self.rect.x > WIDTH or self.rect.x < 0:
            self.speed *= -1
        # if self.rect.y > HEIGHT or self.rect.y < 0:
        #     self.speed *= -1

class FakeWall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.fakewalls, game.zelda_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = game.walls2_img
        # self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.speed = 0
    def update(self):
        # self.rect.x += 1
        self.rect.x += TILESIZE * self.speed
        # self.rect.y += TILESIZE * self.speed
        if self.rect.x > WIDTH or self.rect.x < 0:
            self.speed *= -1
        # if self.rect.y > HEIGHT or self.rect.y < 0:
        #     self.speed *= -1

class ZeldaCoin(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.coins, game.zelda_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = game.coin_img
        # self.image.fill(GOLD)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class MarioCoin(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.coins, game.mario_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = game.coin_img2
        # self.image.fill(GOLD)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


class MarioWall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls, game.mario_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = game.walls_img
        # self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.speed = 0
    def update(self):
        # self.rect.x += 1
        self.rect.x += TILESIZE * self.speed
        # self.rect.y += TILESIZE * self.speed
        if self.rect.x > WIDTH or self.rect.x < 0:
            self.speed *= -1
        # if self.rect.y > HEIGHT or self.rect.y < 0:
        #     self.speed *= -1


class FakeWall2(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.fakewalls, game.mario_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = game.walls_img
        # self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.speed = 0
    def update(self):
        # self.rect.x += 1
        self.rect.x += TILESIZE * self.speed
        # self.rect.y += TILESIZE * self.speed
        if self.rect.x > WIDTH or self.rect.x < 0:
            self.speed *= -1
        # if self.rect.y > HEIGHT or self.rect.y < 0:
        #     self.speed *= -1

class FreezeItem(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.freezes
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(BGCOLOR)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.speed = 0