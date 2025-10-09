from game_core import *

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

# create the frog on the screen
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
