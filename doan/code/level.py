import pygame

from values import *
from enemy_skeleton import *

SKELETON_ARRAY=[]
last_spam=pygame.time.get_ticks()

#y=−1.0306×W/H×x+1.198×H

street=[pygame.Rect((0,450),(900,150))]

def spam_skeleton(SKELETON_ARRAY,keys,last_spam,delay_time=5000) :
    from game import GAME
    from values import PLAYER
    now=pygame.time.get_ticks()
    if now-last_spam>=delay_time :
        last_spam=now
        temp=skeleton(100,400)
        SKELETON_ARRAY.append(temp)
    for i in SKELETON_ARRAY :
        i.draw(GAME)
        i.AI(PLAYER.rect.x,keys)
    return last_spam
   
    

# def level_1() :
#     from game import GAME
#     global last_spam,SKELETON_ARRAY
#     keys=pygame.key.get_pressed()
#     GAME.blit(BACKGROUND_1,(0,0))
#     last_spam=spam_skeleton(SKELETON_ARRAY,keys,last_spam)
#     PLAYER_POSITION["Y"]=HEIGHT*0.855-300
#     road_1=pygame.draw.line(GAME,COLOR_RED,(0,HEIGHT*0.855),(WIDTH*0.333,HEIGHT*0.855),1)
#     road_2=pygame.draw.line(GAME,COLOR_GREEN,(WIDTH*0.333,HEIGHT*0.855),(WIDTH*0.4867,HEIGHT*0.657),1)
#     road_3=pygame.draw.line(GAME,COLOR_GREEN,(WIDTH*0.4867,HEIGHT*0.657),(WIDTH,HEIGHT*0.657),1)
#     ENEMY_SKELETON.draw(GAME)
#     ENEMY_SKELETON.AI(PLAYER.rect.x,keys)
#     PLAYER.move(keys,ROAD_LEVEL_1,ROAD_POINT_LEVEL_1)
#     PLAYER.draw(GAME)
#     
# def level_2() :
#     from game import GAME
#     GAME.blit(BACKGROUND_2,(0,0))

def level_1(GAME,WIDTH,HEIGHT) :
    global street
    background=pygame.image.load("../ShineOnSprites/BackgroundImages/ForestBG2.png")
    background=pygame.transform.smoothscale(background,(WIDTH,HEIGHT))
    GAME.blit(background,(0,0))
    ground=pygame.image.load("../ShineOnSprites/GrassyPlatforms/GrassyPlatform2.png")
    ground = pygame.transform.scale2x(ground)
    ground = pygame.transform.scale2x(ground)
    ground_size=64
    for x in range(0, WIDTH, ground_size):
        GAME.blit(ground, (x, 450))
    #road_1=pygame.draw.rect(GAME,COLOR_RED,street[0])
    rock=pygame.image.load("../ShineOnSprites/RockyTiles/RockyTile7.png")
    rock = pygame.transform.scale2x(rock)
    rock = pygame.transform.scale2x(rock)
    rock_size=64
    for x in range(0, WIDTH, rock_size):
        GAME.blit(rock, (x, 450+64))
    keys=pygame.key.get_pressed()
    
    PLAYER.move(keys,street)
    PLAYER.draw(GAME)




print(" DA CAP NHAT ")