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


class BaseObject:
    def __init__(self, x, y, imagefile, z=250, collision_rect=None):
        self._imagefile = imagefile
        self._x = x
        self._y = y
        self._z = z
        self._image = pygame.image.load(self._imagefile).convert_alpha()
        self._rect = self._image.get_rect()
        self._collision_rect = self._rect
        self._rect.move_ip(self._x, self._y)
        self._type = "object"

    def move_to(self, x, y):
        self._rect.move_ip(-self._x, -self._y)
        self._x = x
        self._y = y
        self._rect.move_ip(self._x, self._y)

    def move_by(self, x, y):
        self._x += x
        self._y += y
        self._rect.move_ip(x, y)

    def draw(self, screen):
        screen.blit(self._image, self._rect)

    def rect(self):
        return self._rect

    def z_order(self):
        return self._z

    def type(self):
        return self._type


class Character(BaseObject):
    def __init__(self, x, y, imagefile):
        super().__init__(x, y, imagefile, z=500)
        self._vertical_speed = 30
        self._horizontal_speed = 0
        self._on_the_ground = False
        self._type = "character"

    def move(self, limit_rect):
        x = self._horizontal_speed
        y = self._vertical_speed

        self.move_by(x, y)

        clamp = False
        # At the bottom edge
        if self.rect().y + self.rect().height >= limit_rect.y + limit_rect.height:
            clamp = True
            self._horizontal_speed = 0
            self._vertical_speed = 0
            self._on_the_ground = True
        else:
            self._on_the_ground = False

        # At the top edge
        if self.rect().y < limit_rect.y:
            clamp = True
            self._horizontal_speed = 0
            self._vertical_speed = 0

        # At the left edge
        if self.rect().x < limit_rect.x:
            clamp = True
            self._horizontal_speed = 0
            if self._vertical_speed < 0:
                self._vertical_speed = 0

        # At the right edge
        if self.rect().x + self.rect().width > limit_rect.x + limit_rect.width:
            clamp = True
            self._horizontal_speed = 0
            if self._vertical_speed < 0:
                self._vertical_speed = 0

        if clamp:
            self._rect.clamp_ip(limit_rect)

        if self._vertical_speed < 50:
            self._vertical_speed += 3

    def boost(self, horizontal, vertical):
        self._vertical_speed = vertical
        self._horizontal_speed = horizontal

    def move_up(self):
        self._vertical_speed = -20

    def jump_up(self):
        self._vertical_speed = -40

    def jump_left(self, onGround):
        if onGround:
            self._vertical_speed = -5
        self._horizontal_speed = -10

    def jump_right(self, onGround):
        if onGround:
            self._vertical_speed = -5
        self._horizontal_speed = 10

    def on_ground(self):
        return self._on_the_ground

    def moving_up(self):
        return self._vertical_speed < 0

    def moving_down(self):
        return self._vertical_speed > 0

    def moving_left(self):
        return self._horizontal_speed < 0

    def moving_right(self):
        return self._horizontal_speed > 0


class FlyingNPC(BaseObject):
    def __init__(self, imagefile, objecttype="flying"):
        super().__init__(0, 0, imagefile)
        self._position = self.__choose_random_position()
        self.move_to(self._position[0], self._position[1])
        self._speed = random.randint(10, 30)
        self._nextpos = self.__choose_random_position()
        self.__calculate_xy_speed()
        self._type = objecttype

    def __choose_random_position(self):
        x = random.randint(int(self.rect().width / 2), SCREEN_DIMENSIONS[0] - int(self.rect().width / 2))
        y = random.randint(int(self.rect().height / 2), SCREEN_DIMENSIONS[1] - int(self.rect().height / 2))
        return (x, y)

    def __calculate_xy_speed(self):
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
            self._nextpos = self.__choose_random_position()
            self.__calculate_xy_speed()


class Feature(BaseObject):
    def __init__(self, x, y, imagefile, z=250, objecttype="feature"):
        super().__init__(x, y, imagefile,z=z)
        self._type = objecttype
        self._collision_directions = [True, True, True, True]

    def set_collision_directions(self, top=False, bottom=False, left=False, right=False):
        self._collision_directions = [left, bottom, right, top]
        return self

    def set_collision_rect(self, left=0, top=0, width=0, height=0):
        self._collision_rect = pygame.Rect(left, top, width, height)
        self._collision_rect.move_ip(self._x, self._y)
        return self

    def collision_rect(self):
        return self._collision_rect

    def collisions_top(self):
        return self._collision_directions[3]

    def collisions_bottom(self):
        return self._collision_directions[1]

    def collisions_left(self):
        return self._collision_directions[0]

    def collisions_right(self):
        return self._collision_directions[2]


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
        self._running = False
        self._score = 0
        self._character = None
        self._flying = []
        self._features = []

        self._screen = screen
        self._clock = pygame.time.Clock()
        self._font = pygame.font.SysFont('Comic Sans MS', 50)

        self._collisionHandler = None

    def set_collision_handler(self, handler):
        self._collisionHandler = handler

    def refresh_screen(self):
        # refresh the display
        self._screen.fill((255, 255, 255))

        all_objects = [self._character, ]
        all_objects.extend(self._features)
        all_objects.extend(self._flying)

        all_objects.sort(key=lambda object: object.z_order())

        for object in all_objects:
            object.draw(self._screen)

        text = self._font.render('%d' % self._score, False, (32, 128, 32))
        self._screen.blit(text, (15, 15))

        pygame.display.update()

    def set_character(self, character):
        self._character = character

    def character(self):
        return self._character

    def add_feature(self, feature):
        self._features.append(feature)

    def delete_feature(self, feature):
        self._features.remove(feature)
        del feature

    def add_flying(self, flying):
        self._flying.append(flying)

    def delete_flying(self, flying):
        self._flying.remove(flying)
        del flying

    def increment_score(self):
        self._score += 1

    def run(self):
        self._running = True

        while self._running:
            self._clock.tick(30)

            # Watch for keyboard and mouse events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_LEFT]:
                        self._character.jump_left(self._character.on_ground())
                    if keys[pygame.K_RIGHT]:
                        self._character.jump_right(self._character.on_ground())
                    if keys[pygame.K_UP] and self._character.on_ground():
                        self._character.move_up()
                    if keys[pygame.K_SPACE] and self._character.on_ground():
                        self._character.jump_up()

            # what if the frog about to hit the ground or a feature?
            clamp = [0, SCREEN_DIMENSIONS[1], SCREEN_DIMENSIONS[0], 0]
            frog_rect = self._character.rect()
            halo = frog_rect.inflate(0, 0)
            if self._character.moving_down() or self._character.moving_up():
                halo.inflate_ip(0, 100)
            if self._character.moving_left() or self._character.moving_right():
                halo.inflate_ip(100, 0)

            for feature in self._features:
                if self._collisionHandler is not None and feature.collision_rect().colliderect(frog_rect):
                    self._collisionHandler(self, feature)

                if feature.collision_rect().colliderect(halo):
                    if (self._character.moving_down() and feature.collisions_top() and
                            frog_rect.y + frog_rect.height <= feature.collision_rect().y):
                        clamp[1] = feature.collision_rect().y
                    if (self._character.moving_up() and feature.collisions_bottom() and
                            frog_rect.y >= feature.collision_rect().y + feature.collision_rect().height):
                        clamp[3] = feature.collision_rect().y + feature.collision_rect().height
                    if (self._character.moving_left() and feature.collisions_right() and
                            frog_rect.x + frog_rect.width <= feature.collision_rect().x):
                        clamp[2] = feature.collision_rect().x
                    if (self._character.moving_right() and feature.collisions_left() and
                            frog_rect.x >= feature.collision_rect().x + feature.collision_rect().width):
                        clamp[0] = feature.collision_rect().x + feature.collision_rect().width

            clamprect = pygame.Rect(clamp[0], clamp[3], clamp[2] - clamp[0], clamp[1] - clamp[3])

            # update the character position
            self._character.move(clamprect)

            # move the flying NPCs
            for fly in self._flying:
                fly.move()

            # detect collisions with the flying NPCs
            for idx, fly in enumerate(self._flying):
                if self._collisionHandler is not None and fly.rect().colliderect(self._character.rect()):
                    self._collisionHandler(self, fly)

            self.refresh_screen()


################## GAME SPECIFIC CODE BELOW HERE #####################

def handleCollisions(game, item):
    if item.type() == "flying":
        game.delete_flying(item)
        game.increment_score()
        game.add_flying(FlyingNPC(os.path.join(IMAGE_DIR, 'small_fly.png')))

    if item.type() == "coin":
        game.delete_feature(item)
        game.increment_score()

    if item.type() == "boost":
        game.character().boost(0,-50)

    if item.type() == "portal":
        game.character().move_to(750,100)

# create the blank game
game = Game(screen)

# create the frog in the centre of the screen
game.set_character(Character(350, 100, os.path.join(IMAGE_DIR, 'small_frog.png')))

# create the platforms
game.add_feature( Feature(100, 400, os.path.join(IMAGE_DIR, 'grass.png')).set_collision_rect(10, 15, 116, 50))
game.add_feature( Feature(300, 500, os.path.join(IMAGE_DIR, 'grass.png')).set_collision_rect(10, 15, 116, 50))
game.add_feature( Feature(200, 700, os.path.join(IMAGE_DIR, 'grass.png')).set_collision_rect(10, 15, 116, 50))
game.add_feature( Feature(300, 200, os.path.join(IMAGE_DIR, 'grass.png')).set_collision_rect(10, 15, 116, 50))
game.add_feature( Feature(500, 600, os.path.join(IMAGE_DIR, 'grass.png')).set_collision_rect(10, 15, 116, 50))
game.add_feature( Feature(1000, 400, os.path.join(IMAGE_DIR, 'grass.png')).set_collision_rect(10, 15, 116, 50))
game.add_feature( Feature(700, 100, os.path.join(IMAGE_DIR, 'grass.png')).set_collision_rect(10, 15, 116, 50))

# create the ladder
game.add_feature( Feature(550, 540, os.path.join(IMAGE_DIR, 'ladder.png')).set_collision_directions(top=True, left=True, right=True))
game.add_feature( Feature(550, 492, os.path.join(IMAGE_DIR, 'ladder.png')).set_collision_directions(top=True, left=True, right=True))
game.add_feature( Feature(550, 444, os.path.join(IMAGE_DIR, 'ladder.png')).set_collision_directions(top=True, left=True, right=True))

# add the coins
game.add_feature( Feature(500, 570, os.path.join(IMAGE_DIR, 'coin.png'), objecttype="coin").set_collision_directions())
game.add_feature( Feature(350, 470, os.path.join(IMAGE_DIR, 'coin.png'), objecttype="coin").set_collision_directions())
game.add_feature( Feature(250, 670, os.path.join(IMAGE_DIR, 'coin.png'), objecttype="coin").set_collision_directions())
game.add_feature( Feature(150, 370, os.path.join(IMAGE_DIR, 'coin.png'), objecttype="coin").set_collision_directions())
game.add_feature( Feature(1000, 370, os.path.join(IMAGE_DIR, 'coin.png'), objecttype="coin").set_collision_directions())
game.add_feature( Feature(1050, 370, os.path.join(IMAGE_DIR, 'coin.png'), objecttype="coin").set_collision_directions())
game.add_feature( Feature(1100, 370, os.path.join(IMAGE_DIR, 'coin.png'), objecttype="coin").set_collision_directions())
game.add_feature( Feature(720, 80, os.path.join(IMAGE_DIR, 'coin.png'), objecttype="coin").set_collision_directions())
game.add_feature( Feature(770, 80, os.path.join(IMAGE_DIR, 'coin.png'), objecttype="coin").set_collision_directions())

# add the up booster
game.add_feature( Feature(900, 720, os.path.join(IMAGE_DIR, 'up.png'), objecttype="boost").set_collision_directions())

# add the portal
game.add_feature( Feature(1000, 700, os.path.join(IMAGE_DIR, 'portal.png'), z=200,objecttype="portal").set_collision_directions().set_collision_rect(30, 30, 40, 70))
game.add_feature( Feature(715, 10, os.path.join(IMAGE_DIR, 'portal_end.png'), z=200, objecttype="portal_end").set_collision_directions())

# create the first fly
game.add_flying(FlyingNPC(os.path.join(IMAGE_DIR, 'small_fly.png')))

# set collision callback
game.set_collision_handler(handleCollisions)

# start the game
game.run()
