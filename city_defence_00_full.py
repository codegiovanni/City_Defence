# Sound and Music
# Frozen Jam by tgfcoder <https://twitter.com/tgfcoder> licensed under CC-BY-3
import pygame as pg
import random
from os import path
from enemy import Enemy
from explosion import Explosion
from laser import Laser
from powerup import Powerup
from variables import *

global score
score = 0

pg.mixer.music.load(path.join(sound_dir, 'FrozenJam-SeamlessLoop.ogg'))
pg.mixer.music.set_volume(0.3)
pg.mixer.music.play(loops=-1)

class Player(pg.sprite.Sprite):
    #I couldn't put Player in a different file because it needs to update all_sprites and lasers
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.scale(player_img, (100, 80))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT
        self.speedx = 0
        self.shoot_delay = 300
        self.last_shot = 0
        self.hidden = False
        self.lives = 3
        self.shield = 100
        self.hide_timer = pg.time.get_ticks()
        self.power = 1
        self.powerup_time = pg.time.get_ticks()
        self.radius = int(self.rect.width * .8 / 2)

    def update(self):
        """
        Updates the player's position depending on the key(s) pressed.
        It also checks and decreases the player's power after the powerup time is up.
        """

        #decrease the power if the time is up
        if self.power > 1 and pg.time.get_ticks() - self.powerup_time > POWERUP_TIME:
            self.power -= 1
            self.powerup_time = pg.time.get_ticks()

        #unhide if the time is up
        if self.hidden and pg.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10

        #reset dx and change according to which keys are pressed
        self.speedx = 0
        keystate = pg.key.get_pressed()
        if keystate[pg.K_LEFT]:
            self.speedx = -7
        if keystate[pg.K_RIGHT]:
            self.speedx = 7
        if keystate[pg.K_SPACE]:
            self.shoot()
        #update x by dx
        self.rect.x += self.speedx
        #check for collision with the screen borders
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        self.rect.left = max(self.rect.left, 0)

    def powerup(self):
        self.power += 1
        self.powerup_time = pg.time.get_ticks()

    def shoot(self):
        if self.hidden:
            return
        now = pg.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            shoot_sound.play()
            #create a laser for every laser
            for i in range(self.power):
                l = Laser(divide_equal(self.rect.left, self.rect.right, self.power-1)[i], self.rect.centery)
                all_sprites.add(l)
                lasers.add(l)

    def hide(self):
        self.hidden = True
        self.hide_timer = pg.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 1000)

def draw_shield_bar(surface:pg.display, x:int, y:int, percent:int):
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    percent = max(percent, 0)
    fill = (percent / 100) * BAR_LENGTH
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    pg.draw.rect(surface, GREEN, fill_rect)
    pg.draw.rect(surface, WHITE, outline_rect, 2)


def draw_text(surface:pg.display, text:str, size:int, x:int, y:int):
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)


def draw_lives(surface:pg.display, x:int, y:int, lives:int, image:pg.image):
    for i in range(lives):
        img_rect = image.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surface.blit(image, img_rect)


def add_enemy():
    x = Enemy()
    all_sprites.add(x)
    enemies.add(x)

def divide_equal(start:int, end:int, num:int) -> list:
    """
    Given a start and an end, returns a list of all the coordinates that divide that segment in equal parts.
    If num == 0, returns the average between start and end
    """
    if num == 0:
        return [(start+end)/2]
    if start > end or num < 1:
        raise SyntaxError
    if start == end or num == 1:
        return [start, end]
    res = [start]
    for _ in range(num):
        res.append(int(res[-1] + (end-start)/num))
    return res

def load_data():
    dir = path.dirname(__file__)
    try:
        with open(path.join(dir, HS_FILE), 'r') as f:
            highscore = int(f.read())
    except:
        with open(path.join(dir, HS_FILE), 'w') as f:
            highscore = 0
    return highscore


def show_go_screen(svalue:int, hvalue:int):
    score = svalue
    highscore = hvalue
    dir = path.dirname(__file__)
    screen.blit(background_start, (0, 0))
    draw_text(screen, "CITY DEFENCE!", 64, WIDTH / 2, HEIGHT / 3)
    draw_text(screen, "Press any key to begin", 32, WIDTH / 2, HEIGHT / 7 * 3)
    draw_text(screen, "(Arrow keys to move, Space to fire)", 18, WIDTH / 2, HEIGHT / 8 * 4 - 20)
    if score > highscore:
        highscore = score
        with open(path.join(dir, HS_FILE), 'r+') as f:
            f.write(str(highscore))
    draw_text(screen, "High Score: " + str(highscore), 24, WIDTH / 2, 15)

    pg.display.update()

    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            if event.type == pg.KEYDOWN:
                waiting = False

for i in range(7):
    filename = f'explosion_0{i}.png'
    img = pg.image.load(path.join(image_dir, filename)).convert()
    img.set_colorkey(BLACK)
    img_large = pg.transform.scale(img, (75, 75))
    explosion_anim['large'].append(img_large)
    img_small = pg.transform.scale(img, (32, 32))
    explosion_anim['small'].append(img_small)

while running:

    clock.tick(FPS)

    if game_over:
        highscore = load_data()
        show_go_screen(score, highscore)
        game_over = False
        all_sprites = pg.sprite.Group()
        player = Player()
        all_sprites.add(player)
        enemies = pg.sprite.Group()
        for _ in range(5):
            add_enemy()
        lasers = pg.sprite.Group()
        powerups = pg.sprite.Group()

        score = 0

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    all_sprites.update()

    hits = pg.sprite.groupcollide(enemies, lasers, True, True)
    for hit in hits:
        score += int(hit.radius)
        expl = Explosion(hit.rect.center, 'large')
        explosion_sound.play()
        all_sprites.add(expl)
        if random.random() > 0.95:
            powerup = Powerup(hit.rect.center)
            all_sprites.add(powerup)
            powerups.add(powerup)
        add_enemy()

    hits = pg.sprite.spritecollide(player, enemies, True, pg.sprite.collide_circle)
    for hit in hits:
        player.shield -= hit.radius * 2
        expl = Explosion(hit.rect.center, 'small')
        all_sprites.add(expl)
        add_enemy()
        if player.shield <= 0:
            death_explosion = Explosion(player.rect.center, 'large')
            player_die_sound.play()
            all_sprites.add(death_explosion)
            player.hide()
            player.lives -= 1
            player.shield = 100

    hits = pg.sprite.spritecollide(player, powerups, True)
    for hit in hits:
        if hit.type == 'shield':
            player.shield += 10
            shield_sound.play()
            player.shield = min(player.shield, 100)
        if hit.type == 'bolt':
            player.powerup()
            powerup_sound.play()

    if player.lives == 0 and not death_explosion.alive():
        game_over = True

    screen.blit(background, (0, ground_scroll))
    ground_scroll += scroll_speed
    if ground_scroll > 0:
        ground_scroll = -(background.get_height() / 2)
    all_sprites.draw(screen)

    draw_lives(screen, WIDTH - 100, 5, player.lives, heart_mini_img)
    draw_text(screen, str(score), 36, WIDTH / 2, 5)
    draw_shield_bar(screen, 5, 10, player.shield)

    pg.display.update()

pg.quit()
