import pygame
from time import sleep

pygame.init()

screen = pygame.display.set_mode([800, 600])
pygame.display.set_caption("T-800 Demo")

walkRight = [pygame.image.load('player/walk_R1.png'), pygame.image.load('player/walk_R2.png'),
             pygame.image.load('player/walk_R3.png'), pygame.image.load('player/walk_R4.png'),
             pygame.image.load('player/walk_R5.png'), pygame.image.load('player/walk_R6.png'),
             pygame.image.load('player/walk_R7.png'), pygame.image.load('player/walk_R8.png'),
             pygame.image.load('player/walk_R9.png'), pygame.image.load('player/walk_R10.png')]
walkLeft = [pygame.image.load('player/walk_L1.png'), pygame.image.load('player/walk_L2.png'),
            pygame.image.load('player/walk_L3.png'), pygame.image.load('player/walk_L4.png'),
            pygame.image.load('player/walk_L5.png'), pygame.image.load('player/walk_L6.png'),
            pygame.image.load('player/walk_L7.png'), pygame.image.load('player/walk_L8.png'),
            pygame.image.load('player/walk_L9.png'), pygame.image.load('player/walk_L10.png')]
iStand = [pygame.image.load('player/stand_R.png'), pygame.image.load('player/stand_L.png')]
shootR = [pygame.image.load('player/fire_R1.png'), pygame.image.load('player/fire_R2.png')]
shootL = [pygame.image.load('player/fire_L1.png'), pygame.image.load('player/fire_L2.png')]

bg = [pygame.image.load('bg/bg_promzone_back2.png'), pygame.image.load('bg/bg_promzone_front2.png')]

bulletSound = pygame.mixer.Sound('sound/shoot.wav')
hitSound = pygame.mixer.Sound('sound/hit.wav')
hurtSound = pygame.mixer.Sound('sound/hurt.wav')
music = pygame.mixer.music.load('sound/bg.mp3')
pygame.mixer.music.play(-1)

timer = pygame.time.Clock()


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = 3
        self.isJump = False
        self.jumpCount = 8
        self.left = False
        self.right = True
        self.animCount = 0
        self.standing = True
        self.hitbox = (self.x, self.y, self.width, self.height)
        self.fire = False
        self.fireCount = 0
        self.shootLoop = 0
        self.health = 100
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.visible = True

    def draw(self, screen):
        global facing  # для анимации стрельбы

        # анимация ходьбы
        if self.visible:
            if self.animCount + 1 >= 30:
                self.animCount = 0

            if not self.standing:
                if self.left:
                    screen.blit(walkLeft[self.animCount // 3], (self.x, self.y))
                    self.animCount += 1
                elif self.right:
                    screen.blit(walkRight[self.animCount // 3], (self.x, self.y))
                    self.animCount += 1
            else:
                if self.right:
                    screen.blit(iStand[0], (self.x, self.y))
                else:
                    screen.blit(iStand[1], (self.x, self.y))

            # анимация стрельбы
            if self.fireCount + 1 >= 3:
                self.fireCount = 0

            if self.fire:
                if facing == 1:
                    if self.fireCount <= 1:
                        screen.blit(shootR[0], (self.x + 3, self.y))
                    else:
                        screen.blit(shootR[1], (self.x, self.y))
                    self.fireCount += 1
                elif facing == -1:
                    if self.fireCount <= 1:
                        screen.blit(shootL[0], (self.x - 23, self.y))
                    else:
                        screen.blit(shootL[1], (self.x, self.y))
                    self.fireCount += 1

            # self.hitbox = (self.x, self.y, self.width, self.height)
            # pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y - 20, 60, 10))  # HP bar
            # pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)  # hitbox
            self.rect = pygame.Rect(self.x, self.y, self.width, self.height)  # обновление прямоугольника

    def hit(self):
        hurtSound.play()
        # self.isJump = False
        # self.jumpCount = 8
        self.x -= 15
        if self.health > 0:
            self.health -= 5
        else:
            self.health = 0
        print('Oops!')
        sleep(0.1)


class Shell(pygame.sprite.Sprite):
    def __init__(self, x, y, radius, color, facing):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 15 * facing
        self.rect = pygame.Rect(self.x, self.y, 10, 10)

    def draw(self, screen):
        self.rect = pygame.Rect(self.x, self.y, 5, 5)  # обновление прямоугольника
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)


class Enemy(pygame.sprite.Sprite):
    walkRight = [pygame.image.load('robot/walk_R1.png'), pygame.image.load('robot/walk_R2.png'),
                 pygame.image.load('robot/walk_R3.png'), pygame.image.load('robot/walk_R4.png'),
                 pygame.image.load('robot/walk_R5.png'), pygame.image.load('robot/walk_R6.png'),
                 pygame.image.load('robot/walk_R7.png'), pygame.image.load('robot/walk_R8.png'),
                 pygame.image.load('robot/walk_R9.png'), pygame.image.load('robot/walk_R10.png'),]
    walkLeft = [pygame.image.load('robot/walk_L1.png'), pygame.image.load('robot/walk_L2.png'),
                pygame.image.load('robot/walk_L3.png'), pygame.image.load('robot/walk_L4.png'),
                pygame.image.load('robot/walk_L5.png'), pygame.image.load('robot/walk_L6.png'),
                pygame.image.load('robot/walk_L7.png'), pygame.image.load('robot/walk_L8.png'),
                pygame.image.load('robot/walk_L9.png'), pygame.image.load('robot/walk_L10.png'),]
    strikeLeft = [pygame.image.load('robot/strike_L2.png'), pygame.image.load('robot/strike_L3.png'),
                  pygame.image.load('robot/strike_L2.png'), pygame.image.load('robot/strike_L1.png')]
    light = [pygame.image.load('robot/light1.png'), pygame.image.load('robot/light1.png'),
             pygame.image.load('robot/light1.png'), pygame.image.load('robot/light2.png'),
             pygame.image.load('robot/light3.png'), pygame.image.load('robot/light4.png'),
             pygame.image.load('robot/light5.png'), pygame.image.load('robot/light4.png'),
             pygame.image.load('robot/light3.png'), pygame.image.load('robot/light2.png')]

    def __init__(self, x, y, width, height, end):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.speed = 2
        # self.hitbox = (self.x, self.y, 85, 105)
        self.health = 10
        self.visible = True
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.anim = 0
        self.attack = False

    def update(self, screen):
        global scroll
        self.move()

        if self.visible:
            if self.walkCount + 1 >= 30:
                self.walkCount = 0

            if self.anim >= 90:
                self.anim = 0

            if not self.attack:
                if self.speed > 0:
                    screen.blit(self.walkRight[self.walkCount // 3], (self.x + scroll, self.y))
                    self.walkCount += 1
                elif self.speed < 0:
                    screen.blit(self.walkLeft[self.walkCount // 3], (self.x + scroll, self.y))
                    self.walkCount += 1
                else:
                    if self.anim > 59:
                        screen.blit(self.light[self.walkCount // 3], (self.x + scroll, self.y))
                        self.walkCount += 1
                    else:
                        screen.blit(self.walkRight[4], (self.x + scroll, self.y))
                    self.anim += 1
            else:
                screen.blit(self.strikeLeft[self.walkCount // 8], (self.x + scroll, self.y))
                self.walkCount += 2
                if self.walkCount >= 29:
                    self.attack = False
                    self.walkCount = 0

            # self.hitbox = (self.x, self.y, 85, 105)
            # pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)  # hitbox
            pygame.draw.rect(screen, (255,0,0), (self.x + scroll, self.y - 20, 80, 10))  # HP bar
            pygame.draw.rect(screen, (0,255,0), (self.x + scroll, self.y - 20, 8 * self.health, 10))
            self.rect = pygame.Rect(self.x + scroll, self.y, 85, 105)  # обновление прямоугольника

    # движение по пути
    def move(self):
        if self.path[0] == self.path[1]:
            self.speed = 0
        if self.speed > 0:
            if self.x + self.speed < self.path[1]:
                self.x += self.speed
            else:
                self.speed = self.speed * -1
                # self.walkCount = 0
        else:
            if self.x + self.speed > self.path[0]:
                self.x += self.speed
            else:
                self.speed = self.speed * -1
                # self.walkCount = 0

    def hit(self):
        hitSound.play()
        if self.health > 1:
            self.health -= 1
        else:
            self.health = 0
            self.visible = False
        print('hit', self.health)

    def strike(self):
        self.walkCount = 0
        self.attack = True


class Cloud(pygame.sprite.Sprite):
    types = [pygame.image.load('bg/cloud1.png'), pygame.image.load('bg/cloud2.png'),
             pygame.image.load('bg/cloud3.png'), pygame.image.load('bg/cloud4.png'),
             pygame.image.load('bg/cloud5.png'), pygame.image.load('bg/cloud6.png')]

    def __init__(self, x, y, type, speed):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.speed = speed
        self.image = self.types[type]
        self.width = self.image.get_width()

    def update(self, screen):
        screen.blit(self.image, (self.x + self.speed, self.y))


# отрисовка всего
def screen_draw():
    text_score = font.render('Score: ' + str(score), 1, (0,0,0))
    text_hp = font2.render(str(man.health), 1, (255,0,0))

    screen.blit(bg[0], (1 * scroll // 2, 0))
    clouds.update(screen)

    for bullet in bullets:
        bullet.draw(screen)

    man.draw(screen)
    enemies.update(screen)
    screen.blit(bg[1], (1 * scroll, 0))

    pygame.draw.rect(screen, (0, 255, 0), (15, 545, 210, 40), 5)
    pygame.draw.rect(screen, (255, 0, 0), (20, 550, 2 * man.health, 30))  # HP внизу экрана
    screen.blit(text_hp, (235, 547))
    screen.blit(text_score, (10, 10))

    if man.health <= 0:
        man.visible = False
        screen.blit(text_gg, (screen.get_width() // 2 - text_gg.get_width() // 2, screen.get_height() // 3 - 20))
        screen.blit(text_gg2, (screen.get_width() // 2 - text_gg2.get_width() // 2,
                               screen.get_height() // 3 + text_gg.get_height() - 20))
        man.speed = 0

    pygame.display.update()


scroll = 0
score = 0
font = pygame.font.SysFont("comicsans", 30, True)
font2 = pygame.font.SysFont("comicsans", 60, True)
font3 = pygame.font.SysFont("comicsans", 100, True)
text_gg = font3.render('GAME OVER', 1, (255,0,0))
text_gg2 = font2.render('F to retry, Esc to exit', 1, (255,0,0))

bullets = []
man = Player(60, 390, 60, 73)
clouds = pygame.sprite.Group()
clouds.add(Cloud(600, 0, 0, 0.5), Cloud(50, 30, 1, 0.5), Cloud(300, 10, 2, 0.7),
           Cloud(400, 100, 3, 0.7), Cloud(0, 160, 4, 0.6), Cloud(400, 150, 5, 0.6),
           Cloud(500, 20, 3, 0.6), Cloud(800, 30, 4, 0.7))
enemies = pygame.sprite.Group()
enemies.add(Enemy(250, 358, 85, 105, 550), Enemy(500, 358, 85, 105, 750),
            Enemy(200, 358, 85, 105, 200), Enemy(940, 310, 85, 105, 940),
            Enemy(1000, 358, 85, 105, 1200), Enemy(1450, 358, 85, 105, 1450),
            Enemy(1650, 358, 85, 105, 1850), Enemy(2070, 310, 85, 105, 2070))
run = True

while run:
    timer.tick(30)

    # счётчик пуль, частота срельбы
    if man.shootLoop > 0:
        man.shootLoop += 1
    if man.shootLoop > 4:
        man.shootLoop = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f and man.health <= 0:
                man.health = 100
                man.speed = 3
                man.visible = True
                man.x = 60
                man.y = 390
            if event.key == pygame.K_ESCAPE and man.health <= 0:
                run = False

    # коллизии игрока
    for enemy in enemies:
        if pygame.sprite.collide_rect(man, enemy) and enemy.visible and man.visible:
            man.hit()
            enemy.strike()

    # коллизии пуль
    for bullet in bullets:
        if 0 < bullet.x < screen.get_width():
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))
            break

        for enemy in enemies:
            if pygame.sprite.collide_rect(bullet, enemy) and enemy.visible:  # функция коллизии
                bullets.pop(bullets.index(bullet))
                enemy.hit()
                score += 1
                break

    # движение облаков
    for cloud in clouds:
        if cloud.x + cloud.width > 0:
            cloud.x -= cloud.speed
        else:
            cloud.x = screen.get_width()

    # сайд скролл
    if man.x > screen.get_width() - 450 and scroll > -1600:
        scroll -= 2
        man.x -= 2

    keys = pygame.key.get_pressed()

    # стрельба
    if keys[pygame.K_SPACE] and man.shootLoop == 0:
        man.fire = True
        man.shootLoop = 1
        if man.right:
            facing = 1
        else:
            facing = -1

        if len(bullets) < 50:
            if facing == 1:
                bulletSound.play()
                bullets.append(Shell(round(man.x + man.width // 2) + 40 * facing,
                                     round(man.y + man.height // 2) - 11, 5, (0, 0, 0), facing))
            else:
                bulletSound.play()
                bullets.append(Shell(round(man.x + man.width // 2) + 40 * facing,
                                     round(man.y + man.height // 2) - 11, 5, (0, 0, 0), facing))
    else:
        man.fire = False

    # ходьба
    if keys[pygame.K_LEFT] and man.x > 0:
        man.x -= man.speed
        man.left = True
        man.right = False
        man.standing = False
    elif keys[pygame.K_RIGHT] and man.x < screen.get_width() - man.width:
        man.x += man.speed
        man.right = True
        man.left = False
        man.standing = False
    else:
        man.standing = True
        man.animCount = 0

    # прыжки
    if not man.isJump:
        if keys[pygame.K_UP]:
            man.isJump = True
    else:
        if man.jumpCount >= -8:
            if man.jumpCount < 0:
                man.y += (man.jumpCount ** 2) // 2
            else:
                man.y -= (man.jumpCount ** 2) // 2
            man.jumpCount -= 1
        else:
            man.isJump = False
            man.jumpCount = 8

    screen_draw()

pygame.quit()
