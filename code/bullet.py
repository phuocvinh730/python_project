import pygame
from setting import *

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, direction, player):
        super().__init__()
        self.image = pygame.Surface((20, 8))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect(center=pos)
        self.direction = direction
        self.speed = 600
        self.player = player  # Truyền player vào để biết camera

    def update(self, fps):
        self.rect.x += self.direction * self.speed * fps

        # Tính vị trí theo camera
        offset_x = -self.player.hit_box_rect.x + game_width // 2
        offset_y = -self.player.hit_box_rect.y + game_height // 2
        screen_pos = self.rect.move(offset_x, offset_y)

        # Nếu ra ngoài màn hình thì kill
        if screen_pos.right < 0 or screen_pos.left > game_width:
            self.kill()
