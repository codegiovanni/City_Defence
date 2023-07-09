from os import path
import pygame as pg

image_dir = path.join(path.dirname(__file__), 'image')
sound_dir = path.join(path.dirname(__file__), 'sound')

HS_FILE = "highscore.txt"

WIDTH, HEIGHT = 450, 600
FPS = 60

POWERUP_TIME = 6000

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

pg.init()
pg.mixer.init()

screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("CITY DEFENCE")
clock = pg.time.Clock()

font_name = pg.font.match_font('arial bold')

background_start = pg.image.load(path.join(image_dir, "urban_long_grey.png")).convert()
background = pg.image.load(path.join(image_dir, "urban_long.png")).convert()
player_img = pg.image.load(path.join(image_dir, "plane_white.png")).convert()
laser_img = pg.image.load(path.join(image_dir, "laser.png")).convert()
heart_img = pg.image.load(path.join(image_dir, "heart.png")).convert()
heart_mini_img = pg.transform.scale(heart_img, (25, 19))
heart_mini_img.set_colorkey(BLACK)

enemy_list = ['virus_red.png', 'virus_blue.png', 'virus_violet.png']

enemy_images = [
    pg.image.load(path.join(image_dir, image)).convert()
    for image in enemy_list
]

shoot_sound = pg.mixer.Sound(path.join(sound_dir, 'laser.wav'))
shield_sound = pg.mixer.Sound(path.join(sound_dir, 'shield.wav'))
powerup_sound = pg.mixer.Sound(path.join(sound_dir, 'powerup.wav'))
explosion_sound = pg.mixer.Sound(path.join(sound_dir, 'explosion.wav'))
player_die_sound = pg.mixer.Sound(path.join(sound_dir, 'explosion_player.ogg'))

all_sprites = pg.sprite.Group()
lasers = pg.sprite.Group()
powerups = pg.sprite.Group()

powerup_images = {
    'shield': pg.image.load(path.join(image_dir, 'shield_gold.png')).convert()
}

powerup_images['bolt'] = pg.image.load(path.join(image_dir, 'bolt_gold.png')).convert()

explosion_anim = {'large': [], 'small': []}

ground_scroll = -(background.get_height() / 2)
scroll_speed = 2

game_over = True
running = True