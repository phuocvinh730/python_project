import pygame

from pytmx.util_pygame import load_pygame
from os.path import join
from pygame.math import Vector2

# thong so game
game_width=1200
game_height=700
game_title=""

# mau 
color_red=(255, 0, 0)
color_green=(0, 255, 0)
color_blue=(0, 0, 255)
color_yellow=(255, 255, 0)
color_orange=(255, 165, 0)
color_purple=(128, 0, 128)
color_pink=(255, 192, 203)
color_black=(0, 0, 0)
color_white=(255, 255, 255)
color_gray=(128, 128, 128)

# tile map
tile_size=64

# setting nhan vat
player_speed=50
player_gravity=1300
player_jump_height=30