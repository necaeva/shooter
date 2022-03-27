#Создай собственный Шутер!
from pygame import *
from random import randint

class GameSprite(sprite.Sprite):
    def __init__(self, sprite_image, speed, x, y, size_x, size_y):
        super().__init__()
        self.speed = speed
        self.image = transform.scale(image.load(sprite_image), (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x <630:
            self.rect.x += self.speed
        if keys[K_UP]:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < 430:
            self.rect.y += self.speed
    def fire(self):
        bullet = Bullet('bullet.png',-15, self.rect.centerx, self.rect.top,15,20)
        bullets.add(bullet)

lost = 0
score = 0

class Enemy(GameSprite):
 def update(self):
    global lost
    global score
    self.rect.y += self.speed
    if self.rect.y >500:
        self.rect.y = -100
        self.rect.x = randint(0,600)
        score -= 5
        self.speed = randint(1,5)
        lost += 1

class Asteroid(GameSprite):
 def update(self):
    global lost
    global score
    self.rect.y += self.speed
    if self.rect.y >500:
        self.rect.y = -100
        self.rect.x = randint(0,600)
        score -= 5
        self.speed = randint(1,5)
        lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

player = Player('rocket.png', 5, 325, 425, 80, 100)
#monster = Enemy('ufo.png', 2, 500, 300)
#final = GameSprite('treasure.png', 0, 500, 400)
monsters = sprite.Group()
for i in range(5):
    monster = Enemy('ufo.png', randint(1 , 2), randint(0, 600), -100, 80, 50)
    monsters.add(monster)

asteroids = sprite.Group()
for i in range(5):
    asteroid = Asteroid('asteroid.png', randint(1 , 2), randint(0, 600), -100, 80, 50)
    asteroids.add(asteroid)

win_width = 700
win_height = 500 
window = display.set_mode((win_width,win_height))
background = transform.scale(image.load('galaxy.jpg'), (win_width, win_height))

menu = transform.scale(image.load('asteroid.png'), (win_width, win_height))

#screamer = transform.scale(image.load('скример.jpg'), (win_width, win_height))

run = True
FPS = 60
clock = time.Clock()
#bad = [w1,w2,w3,w4,monster,monster2,monster3]

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire = mixer.Sound('fire.ogg')
scream = mixer.Sound('muy.ogg')

font.init()
font1 = font.SysFont('Arial',20)
font2 = font.SysFont('Arial',100)
menutext = font1.render('Нажмите R для продолжения',True,(255,0,0))
#win = font.render('WIN',True,(100,200,250))
losetext = font2.render('LOSE',True,(255,0,0))
wintext = font2.render('WIN', True,(255,0,0))
menutext2 = font1.render('',True,(255,0,0))

fire_sound = mixer.Sound('fire.ogg')
bullets = sprite.Group()

bullets_count = 0

run = True
finish = False
pause = 0

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key == K_p:
                finish = True
                pause = 1
            if e.key == K_r:
                finish = False
            if e.key == K_l:
                score = 0
                lost= 0
                for m in monsters:
                    m.rect.y = - 100
            if e.key == K_SPACE and bullets_count< 20:
                fire_sound.play()
                player.fire()
                bullets_count += 1
                waittime = 0

    if not finish:
        window.blit(background, (0,0))
        player.reset()
        player.update()
        monsters.update()
        monsters.draw(window)
        bullets.update()
        bullets.draw(window)
        asteroids.update()
        asteroids.draw(window)

        text_lose = font1.render('Пропущено:' + str(lost), 1 ,(255,0,0))
        window.blit(text_lose, (10,10))
        text_score = font1.render('Счёт:' + str(score), 1, (255,0,0))
        window.blit(text_score, (10,30))

        if player.rect.y < 0:
            window.blit(screamer,(0,0))
            scream.play()

        if bullets_count == 20 and waittime < 120:
            text = font2.render('Перезарядка', True, (255,0,0))
            window.blit(text,(200,200))
            waittime += 1
        elif bullets_count == 10 and waittime >= 120:
            waittime = 0
            bullets_count = 0 

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            monster = Enemy('ufo.png', randint(1 , 2), randint(0, 600), -100, 80, 50)
            monsters.add(monster)
            score += 10

        if sprite.spritecollide(player, monsters, False) or lost > 5:
            finish = True
            menutext2 = losetext

        if score > 100 :
            finish = True
            menutext2 = wintext
            pause = 0 

    else:
        if pause:
            window.blit(menu,(0,0))
            window.blit(menutext, (250,200))
        else:
            window.blit(menu, (0,0))
            window.blit(menutext2, (250,200))
            score = 0
            lost = 0
            bullets_count = 0
            player.rect.x = 300
            player.rect.y = 400
            for m in monsters:
                m.rect.x = randint(0,600)
                m.rect.y = -100
            for b in bullets:
                b.kill()
            finish = False
            display.update()

            time.delay(3000)

        #if sprite.collide_rect(player, final):
            #finish = True
            #money.play()
            #window.blit(win, (470, 300))
    
        #if sprite.collide_rect(player, monster) or sprite.collide_rect(player,monster2) or sprite.collide_rect(player,monster3) or sprite.collide_rect(player,w1) or sprite.collide_rect(player,w2) or sprite.collide_rect(player,w3) or sprite.collide_rect(player,w4):
            #finish = True
            #kick.play()
            #window.blit(lose, (100, 200))
        #for enemy in bad:
            #if sprite.collide_rect(player,enemy):
                #finish = True
                #kick.play()
                #window.blit(lose, (100, 200))

    display.update()
    clock.tick(FPS)