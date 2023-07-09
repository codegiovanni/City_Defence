import pygame as pg
import random
from variables import powerup_images, BLACK, HEIGHT
class Powerup(pg.sprite.Sprite):
    def __init__(self, center):
        pg.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'bolt'])
        self.image = powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 7

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()