import pygame
import sys
import random
import math
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(ROOT_DIR, 'images')
SCREEN_DIMENSIONS = (1200, 800)
screen = pygame.display.set_mode(SCREEN_DIMENSIONS)
pygame.display.set_caption('Platform')
pygame.font.init()


class Character:

    def __init__(self, x, y, imagefile):
        self._image = pygame.image.load(imagefile).convert_alpha()
        self._rect = self._image.get_rect()
        self._rect.move_ip(x, y)
        self._vertical_speed = 30
        self._horizontal_speed = 0
        self._on_the_ground = False

    def move(self,limit_rect):
        x = self._horizontal_speed
        y = self._vertical_speed

        self._rect.move_ip(x, y)

        clamp = False
        # At the bottom edge
        if  self._rect.y+self._rect.height >= limit_rect.y+limit_rect.height:
            clamp = True
            self._horizontal_speed = 0
            self._vertical_speed = 0
            self._on_the_ground = True
        else:
            self._on_the_ground = False

        # At the top edge
        if  self._rect.y < limit_rect.y:
            clamp = True
            self._horizontal_speed = 0
            self._vertical_speed = 0

        # At the left edge
        if self._rect.x < limit_rect.x:
            clamp = True
            self._horizontal_speed = 0
            if self._vertical_speed < 0:
                self._vertical_speed = 0

        # At the right edge
        if self._rect.x +self._rect.width > limit_rect.x + limit_rect.width:
            clamp = True
            self._horizontal_speed = 0
            if self._vertical_speed < 0:
                self._vertical_speed = 0

        if clamp:
            self._rect.clamp_ip(limit_rect)

        if self._vertical_speed < 50 :
            self._vertical_speed += 3

    def jumpUp(self):
        self._vertical_speed = -40

    def jumpLeft(self,onGround):
        if onGround:
            self._vertical_speed = -5
        self._horizontal_speed = -10

    def jumpRight(self,onGround):
        if onGround:
            self._vertical_speed = -5
        self._horizontal_speed = 10

    def draw(self, screen):
        screen.blit(self._image, self._rect)

    def rect(self):
        return self._rect

    def onGround(self):
        return self._on_the_ground

    def movingUp(self):
        return self._vertical_speed < 0

    def movingDown(self):
        return self._vertical_speed > 0

    def movingLeft(self):
        return self._horizontal_speed < 0

    def movingRight(self):
        return self._horizontal_speed > 0


class FlyingNPC:

    def __init__(self, imagefile):
        self._image = pygame.image.load(imagefile).convert_alpha()
        self._rect = self._image.get_rect()
        self._position = self.__chooseRandomPosition()
        self._speed = random.randint(10, 30)
        self._rect.move_ip(self._position[0], self._position[1])
        self._nextpos = self.__chooseRandomPosition()
        self.__calculateXYSpeed()

    def __chooseRandomPosition(self):
        x = random.randint(int(self._rect.width / 2), SCREEN_DIMENSIONS[0] - int(self._rect.width / 2))
        y = random.randint(int(self._rect.height / 2), SCREEN_DIMENSIONS[1] - int(self._rect.height / 2))
        return (x, y)

    def __calculateXYSpeed(self):
        offsetx = abs(self._rect.centerx - self._nextpos[0])
        offsety = abs(self._rect.centery - self._nextpos[1])
        hypot = math.sqrt((offsetx * offsetx) + (offsety * offsety))
        self._speedx = max(1.0, (float(offsetx) / hypot) * self._speed)
        self._speedy = max(1.0, (float(offsety) / hypot) * self._speed)

    def move(self):
        reachedTarget = [False, False]
        if self._rect.centerx <= self._nextpos[0]:
            if self._nextpos[0] - self._rect.centerx <= self._speedx:
                reachedTarget[0] = True
            else:
                self._rect.move_ip(self._speedx, 0)

        elif self._rect.centerx > self._nextpos[0]:
            if self._rect.centerx - self._nextpos[0] <= self._speedx:
                reachedTarget[0] = True
            else:
                self._rect.move_ip(-self._speedx, 0)

        if self._rect.centery <= self._nextpos[1]:
            if self._nextpos[1] - self._rect.centery <= self._speedy:
                reachedTarget[1] = True
            else:
                self._rect.move_ip(0, self._speedy)

        elif self._rect.centery > self._nextpos[1]:
            if self._rect.centery - self._nextpos[1] <= self._speedy:
                reachedTarget[1] = True
            else:
                self._rect.move_ip(0, -self._speedx)

        if reachedTarget[0] and reachedTarget[1]:
            # we reach the fly's target position - choose another one
            self._nextpos = self.__chooseRandomPosition()
            self.__calculateXYSpeed()

    def draw(self, screen):
        screen.blit(self._image, self._rect)

    def rect(self):
        return self._rect


class Feature:

    def __init__(self, x, y, imagefile):
        self._image = pygame.image.load(imagefile).convert_alpha()
        self._rect = self._image.get_rect()
        self._rect.move_ip(x, y)

    def rect(self):
        return self._rect

    def draw(self, screen):
        screen.blit(self._image, self._rect)


class WelcomeScreen:

    def __init__(self, message):
        self.__message = message

    def show(self, screen):
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render(self.__message, True, (0, 255, 0), (0, 0, 255))
        textRect = text.get_rect()
        textRect.center = (SCREEN_DIMENSIONS[0] // 2, SCREEN_DIMENSIONS[1] // 2)
        screen.fill((255, 255, 255))
        screen.blit(text, textRect)
        pygame.display.update()


class Game:
    def __init__(self, screen):
        self.running = False
        self.score = 0
        self.frog = None
        self.flies = []
        self.features = []

        self.screen = screen
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Comic Sans MS', 50)

    def refreshScreen(self):
        # refresh the display
        self.screen.fill((255, 255, 255))

        for feature in self.features:
            feature.draw(self.screen)

        self.frog.draw(self.screen)

        for fly in self.flies:
            fly.draw(self.screen)

        text = self.font.render('%d' % self.score, False, (32, 128, 32))
        self.screen.blit(text, (15, 15))

        pygame.display.update()

    def characterOnTheGround(self):
        rect = self.frog.rect()
        return rect.y >= SCREEN_DIMENSIONS[1] - rect.height

    def newFly(self):
        self.flies.append(FlyingNPC(os.path.join(IMAGE_DIR, 'small_fly.png')))

    def run(self):
        # create the background
        self.features.append(Feature(100, 400, os.path.join(IMAGE_DIR, 'grass.png')))
        self.features.append(Feature(300, 500, os.path.join(IMAGE_DIR, 'grass.png')))
        self.features.append(Feature(500, 600, os.path.join(IMAGE_DIR, 'grass.png')))
        self.features.append(Feature(200, 700, os.path.join(IMAGE_DIR, 'grass.png')))
        self.features.append(Feature(300, 200, os.path.join(IMAGE_DIR, 'grass.png')))


        # create frog and the first fly
        self.frog = Character(SCREEN_DIMENSIONS[0] / 2, SCREEN_DIMENSIONS[1] /2,
                              os.path.join(IMAGE_DIR, 'small_frog.png'))
        self.newFly()
        self.running = True

        countDownToNextFly = random.randrange(30, 300)
        while self.running:
            self.clock.tick(30)

            # generate random flies
            countDownToNextFly -= 1
            if countDownToNextFly <= 0:
                self.newFly()
                countDownToNextFly = random.randrange(30, 300)

            # Watch for keyboard and mouse events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    sys.exit()
                if  event.type == pygame.KEYDOWN :
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_LEFT]:
                        self.frog.jumpLeft(self.frog.onGround())
                    if keys[pygame.K_RIGHT]:
                        self.frog.jumpRight(self.frog.onGround())
                    if (keys[pygame.K_UP] or keys[pygame.K_SPACE]) and self.frog.onGround():
                        self.frog.jumpUp()

            # what if the frog about to hit the ground or a feature?
            clamp = [0,SCREEN_DIMENSIONS[1],SCREEN_DIMENSIONS[0],0]
            frog_rect = self.frog.rect()
            halo = frog_rect.inflate(0, 0)
            if self.frog.movingDown() or self.frog.movingUp():
                halo.inflate_ip(0, 100)
            if self.frog.movingLeft() or self.frog.movingRight():
                halo.inflate_ip(100, 0)

            for feature in self.features:
                if feature.rect().colliderect(halo):
                    if self.frog.movingDown() and frog_rect.y + frog_rect.height <= feature.rect().y:
                        clamp[1] = feature.rect().y
                    if self.frog.movingUp() and frog_rect.y >= feature.rect().y + feature.rect().height:
                        clamp[3] = feature.rect().y + feature.rect().height
                    if self.frog.movingLeft() and frog_rect.x + frog_rect.width <= feature.rect().x:
                        clamp[2] = feature.rect().x
                    if self.frog.movingRight() and frog_rect.x >= feature.rect().x + feature.rect().width:
                        clamp[0] = feature.rect().x + feature.rect().width

            clamprect = pygame.Rect(clamp[0], clamp[3], clamp[2] - clamp[0], clamp[1] - clamp[3])

            # update the frog position
            self.frog.move(clamprect)

            # move the flies
            for fly in self.flies:
                fly.move()

            # detect collisions
            eaten = []
            for idx, fly in enumerate(self.flies):
                if fly.rect().colliderect(self.frog.rect()):
                    eaten.append(idx)
                    self.score += 1

            # delete eaten flies
            for idx in reversed(eaten):
                del self.flies[idx]

            # if we have zero flies, create a fly
            if len(self.flies) < 1:
                self.newFly()

            self.refreshScreen()


game = Game(screen)
game.run()
