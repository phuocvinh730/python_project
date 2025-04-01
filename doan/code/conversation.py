import pygame
import  sys

from values import *

pygame.init()

font = pygame.font.SysFont("vnarialgv", 30)

text_level_1=["ban la mot hiep si","ban la 2 hiep si","ban la 3 hiep si","ban la 4 hiep si"]

conversation_frame=pygame.Rect((10,500,WIDTH-20,100))
keys=pygame.key.get_pressed()
text_index=0

def draw_text(screen,text,pos,color) :
    text_surface=font.render(text,True,color)
    screen.blit(text_surface,pos)

def next_text(text,keys) :
    global text_index
    if text_index>=len(text) :
        return False 
    if keys[pygame.K_SPACE] :
        text_index+=1
        return True

def conversation(text,fill=False ) :
    from game import GAME
    global conversation_frame,keys
    if fill :
        GAME.fill(COLOR_BLACK)
    next_text(text,keys) 
    draw_text(GAME,text[text_index],(conversation_frame.x+10,conversation_frame.y+10),COLOR_WHITE)
    next_text(text,keys) 
    draw_text(GAME,text[text_index],(conversation_frame.x+10,conversation_frame.y+10),COLOR_WHITE)

def conversation_fill_background(text,text_index) :
    from game import GAME
    pygame.draw.rect(GAME,COLOR_RED,conversation_frame,5)
    
    
    
    
    
    
    
    
    
    