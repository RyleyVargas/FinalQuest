# KidsCanCode - Game Development with Pygame video series
# Shmup game - part 1
# Video link: https://www.youtube.com/watch?v=nGufy7weyGY
# Player sprite and movement
import pygame as pg
from pygame.sprite import Sprite
import random
from os import path
from pathlib import Path
img_folder = Path("img")
bg_img = img_folder / "bg.png"
print(bg_img)

game_dir = path.join(path.dirname(__file__))
print(game_dir)

# global variables
WIDTH = 480
HEIGHT = 600
FPS = 60
POWERUP_TIME = 5000

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# initialize pygame and create window
pg.init()
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Shmup!")
clock = pg.time.Clock()

# Load all game graphics
background = pg.image.load(path.join(game_dir + "/img/bg.png")).convert()
background_rect = background.get_rect()
background_rect2 = background.get_rect()
player_img = pg.image.load(path.join(img_dir, "playerShip1_orange.png")).convert()
mob_img = pg.image.load(path.join(game_dir + "/img/mob.png")).convert()
lazer_img = pg.image.load(path.join(game_dir + "/img/lazer.png")).convert()
spit_img = pg.image.load(path.join(game_dir + "/img/spit.png")).convert()
powerup_images = {}
powerup_images['shield'] = pg.image.load(path.join(game_dir + "/img/power.png")).convert()
powerup_images['gun'] = pg.image.load(path.join(game_dir + "/img/power.png")).convert()
player_mini_img = pg.transform.scale(player_img, (25, 19))


font_name = pg.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def draw__health(surf, x, y, w):
    outline_rect = pg.Rect(x, y, 100, 20)
    fill_rect = pg.Rect(x, y, w, 20)
    pg.draw.rect(surf, RED, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)

def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    pg.draw.rect(surf, GREEN, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)

def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x - 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)    
    
class Player(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.image = pg.Surface((50,40))
        self.image = pg.transform.scale(player_img, (50, 40))
        self.image = player_img
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT -10
        self.speedx = 0
        self.speedy = 10
        self.power = 1
        self.shield = 100
        self.lives = 10
    def update(self):
        self.speedx = 0
        self.speedy = 0
        keystate = pg.key.get_pressed()
        if keystate[pg.K_a]:
            self.speedx = -8
        if keystate[pg.K_d]:
            self.speedx = 8
        if keystate[pg.K_SPACE]:
           self.pew()
        if keystate[pg.K_w]:
            self.speedy = -8
        if keystate[pg.K_s]:
            self.speedy = 8
        self.rect.x += self.speedx
        self.rect.y += self.speedy
    # taken and modified from Bradfield - power up method
    def powerup(self):
        self.power += 1
        self.power_time = pg.time.get_ticks()
    def pew(self):
        lazer = Lazer(self.rect.centerx, self.rect.top)
        all_sprites.add(lazer)
        lazers.add(lazer)
        print('trying to shoot..')
        
class Pow(Sprite):
    def __init__(self, center):
        Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun'])
        self.image = powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 5

    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the top of the screen
        if self.rect.top > HEIGHT:
            self.kill()

class Mob(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.image = pg.Surface((30,30))
        self.image = mob_img
        self.image.set_colorkey(BLACK)
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(0, 250)
        self.speedy = random.randrange(1, 10)
        self.speedx = random.randrange(1, 8)
        self.hitpoints = 10
        def pew(self):
        spit = Spit(self.rect.centerx, self.rect.top)
        all_sprites.add(spit)
        spits.add(spit)
        # print('trying to shoot..')
    def update(self):
        self.health_image = pg.Surface(self.hitpoints, 10)
        self.health_rect.x = self.x
        self.health_rect.y = self.y
        self.rect.x += self.speedx
        if random.random() > 0.99:
            self.pew()
        # self.rect.y += self.speedy
        if self.rect.x > WIDTH or self.rect.x < 0:
            self.speedx*=-1
            self.rect.y += random.randrange(5,25)
        if self.rect.top > HEIGHT + 10:
            self.rect.y = 0
        if self.hitpoints <= 0:
            self.kill()   
            
class Lazer(Sprite):
    def __init__(self, x, y):
        Sprite.__init__(self)
        self.image = lazer_img
        self.image = pg.Surface((5,10))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10
    def update(self):
        self.rect.y += self.speedy
        if self.rect.y < 0:
            self.kill()
            print(len(lazers))
            
class Spit(Sprite):
    def __init__(self, x, y):
        Sprite.__init__(self)
        self.image = spit_img
        # self.image = pg.Surface((5,10))
        # self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = 10
    def update(self):
        self.rect.y += self.speedy
        if self.rect.y < 0:
            self.kill()
            # print(len(lazers))

all_sprites = pg.sprite.Group()
mobs = pg.sprite.Group()
lazers = pg.sprite.Group()
spits = pg.sprite.Group()
powerups = pg.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(8):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

# game loop
running = True
while running:
    # do stuff over and over
    clock.tick(FPS)

    for event in pg.event.get():
        # check for window close
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                player.pew()
                
    # Update the sprites in the game
    all_sprites.update()

    hits = pg.sprite.spritecollide(player, mobs, False)

    if hits:
        running = False
    
    hits = pg.sprite.groupcollide(lazers, mobs, True, True)

    if hits:
        player.shield -= 1

    
    hits = pg.sprite.groupcollide(mobs, lazers, True, True)
    for hit in hits:
        if random.random() > 0.9:
            pow = Pow(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)

    if len(mobs) == 0:
        for i in range(8):
            m = Mob()
            all_sprites.add(m)
            mobs.add(m)

    # for m in mobs:
    #     lhits = pg.sprite.spritecollide(m, lazers, False)
    #     if lhits:
    #         m.hitpoints-=1
    #         # print(m.hitpoints)
    #         if random.random() > 0.9:
    #             pow = Pow(hit.rect.center)
    #             all_sprites.add(pow)
    #             powerups.add(pow)

    # check to see if player hit a powerup
    hits = pg.sprite.spritecollide(player, powerups, True)
    for hit in hits:
        if hit.type == 'shield':
            player.shield += random.randrange(10, 30)
            # shield_sound.play()
            if player.shield >= 100:
                player.shield = 100
        if hit.type == 'gun':
            player.powerup()
            # power_sound.play()

    background_rect2.y = background_rect.y - 600
    background_rect.y+= player.speedy
    background_rect2.y+= player.speedy

    if background_rect2.y >- 0:
        background_rect.y = background_rect.y -600
          
    # Draw or render
    screen.fill(RED)
    screen.blit(background, background_rect)
    draw_shield_bar(screen, 5, 5, player.shield)
    draw_lives(screen, WIDTH - 100, 5, player.lives, player_mini_img)
    all_sprites.draw(screen)
    pg.display.flip()

pg.quit()
