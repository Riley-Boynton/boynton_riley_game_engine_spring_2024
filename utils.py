import pygame as pg

def test_func():
    print("Test func ran...")

def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.rect)

class Spritesheet:
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0,0), (x,y, width, height))
        # use code below if scaling is necessary
        # image = pg.transform.scale(image, (width // 2, height // 2))
        return image