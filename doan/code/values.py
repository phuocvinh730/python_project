import pygame

from player import *
from enemy_skeleton import *

# game size
WIDTH = 1200
HEIGHT = 600

# game name
GAME_NAME="DaRk_PriNcEsS"

# game background
BACKGROUND_1=pygame.image.load("../img/windrise-background-4k.png")
BACKGROUND_1=pygame.transform.smoothscale(BACKGROUND_1,(1200,600))



# sprite sheet animation player
idle=pygame.image.load('../img/p1/_Idle.png')
run=pygame.image.load('../img/p1/_Run.png')
jump=pygame.image.load('../img/p1/_Jump.png')
attack=pygame.image.load('../img/Soldier-Walk.png')
ANIMATION_TYPE={"idle":idle,"run":run,"jump":jump,"attack":attack}

# sprite sheet animation enemy skeleton
idle_skeleton=pygame.image.load('../img/SkeletonIdle.png')
run_skeleton=pygame.image.load('../img/Skeleton Walk.png')
attack_skeleton=pygame.image.load('../img/SkeletonAttack.png')
hit_skeleton=pygame.image.load('../img/SkeletonHit.png')
death_skeleton=pygame.image.load('../img/SkeletonDead.png')
ANIMATION_SKELETON_TYPE={"idle":idle_skeleton,"run":run_skeleton,"attack":attack_skeleton,"hit":hit_skeleton,"death":death_skeleton}


# color
COLOR_RED=(255,0,0)
COLOR_WHITE   = (255, 255, 255)  # Trắng
COLOR_BLACK   = (0, 0, 0)        # Đen
COLOR_GREEN   = (0, 255, 0)      # Xanh lá
COLOR_BLUE    = (0, 0, 255)      # Xanh dương
COLOR_YELLOW  = (255, 255, 0)    # Vàng
COLOR_CYAN    = (0, 255, 255)    # Xanh cyan
COLOR_MAGENTA = (255, 0, 255)    # Hồng tím

# player
PLAYER_POSITION={"X" : 100 , "Y" : 100} 
PLAYER=Player(PLAYER_POSITION["X"],PLAYER_POSITION["Y"])

# enemy
ENEMY_SKELETON=skeleton(100,400)

# gravity
GRAVITY=1





print(" DA CAP NHAT ")

