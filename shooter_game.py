#Create your own shooter

from pygame import*
import random
import pygame
score = 0
difficulty = 1
fps = 60
pX = 0
lives = 3
enemies = 5

init()
mixer.init()
window = display.set_mode((700,500))
display.set_caption("RocketC5000")
background = transform.scale(image.load("galaxy.jpg"),(700,500))
clock = time.Clock()
mixer.music.load("space.ogg")
monsters = sprite.Group()
bullets = sprite.Group()

class GameSprite(sprite.Sprite):
    def __init__(self,imagefile,x,y):
        super().__init__()
        self.image = transform.scale(image.load(imagefile),(50,35))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def draw(self):
        window.blit(self.image,(self.rect.x,self.rect.y))

class Player(GameSprite):
    def __init__(self,imagefile,x,y,speed):
        super().__init__(imagefile,x,y)
        self.image = transform.scale(image.load(imagefile),(60,100))
        self.speed = speed
    def update(self):
        keysdown = key.get_pressed()
        if keysdown[K_LEFT]:
            self.rect.x -= self.speed
        if keysdown[K_RIGHT]:
            self.rect.x += self.speed
        global pX
        pX = self.rect.x
    def fire(self):
        bullet = Bullet("bullet.png",0,400)
        bullets.add(bullet)

class Bullet(GameSprite):
    def __init__(self,imagefile,x,y):
        super().__init__(imagefile,x,y)
        self.image = transform.scale(image.load(imagefile),(20,20))
        self.rect.x = pX + 20
    def update(self):
        self.rect.y -= 5

class Enemy(GameSprite):
    def __init__(self,imagefile,x,y):
        super().__init__(imagefile,x,y)
        self.rect.x = random.randint(50,650)
        self.morespeed = random.randint(1,2)
    def update(self):
        self.rect.y += difficulty * self.morespeed
        if self.rect.y > 700:
            pass

mixer.music.play()
rocket = Player("rocket.png",350,400,5)
game = True
dead = False
font.init()
bullet = Bullet("bullet.png",0,400)
a_font = font.SysFont(None,36)
for i in range(enemies):
    enemy = Enemy("ufo.png",0,50)
    monsters.add(enemy)
while game:
    for event in pygame.event.get():
        if event.type == KEYDOWN and event.key == K_SPACE:
            rocket.fire()
        if event.type == QUIT:
            game = False
    if dead == True:
        pass
    scr = a_font.render(
            "Score: " + str(score),1,(255,255,255)
        )
    sprite_list = sprite.spritecollide(
        rocket,monsters, True,)
    if len(sprite_list) > 0:
        print("h" * 50)
        scr = a_font.render(
            "You lost",1,(255,255,255)
        )
        window.blit(scr,(250,350))
        for i in range(60):
            clock.tick(fps)
        game = False
    sprite_list = sprite.groupcollide(
        monsters,bullets, True, True)
    enemies -= len(sprite_list)
    score += len(sprite_list)
    window.blit(background,(0,0))
    rocket.update()
    rocket.draw()
    monsters.update()
    monsters.draw(window)
    try:
        bullets.update()
        bullets.draw(window)
    except Exception:
        pass
    difficulty += (1/600)
    window.blit(scr,(0,0))
    clock.tick(fps)
    display.update()
    if enemies < 5:
        enemy = Enemy("ufo.png",0,50)
        monsters.add(enemy)