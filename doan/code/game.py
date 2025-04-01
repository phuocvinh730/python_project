import pygame

from values import *
from player import *
from level import *
from conversation import *
from load_map import *
from camera import camera

pygame.init()

clock=pygame.time.Clock()

GAME=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption(GAME_NAME)

tilemap = map("../map/test1.tmx")
camera=camera(1200,600,2560,544)

run=True
while run :
    for event in pygame.event.get() :
        if event.type==pygame.QUIT :
            run=False
            
    keys=pygame.key.get_pressed()
    PLAYER.move(keys,tilemap.collision_blocks(GAME,camera),2400)
    camera.update(PLAYER)
    
    GAME.blit(BACKGROUND_1,(0,0))
    tilemap.draw_map(GAME,camera)
    camera.apply(PLAYER)
    PLAYER.draw(GAME)           
            
    clock.tick(60)
    pygame.display.flip()






pygame.quit()