import pygame
from animation import *

class Player:
    def __init__(self, x, y):
        from values import ANIMATION_TYPE

        self.activity_type = ANIMATION_TYPE["idle"]
        self.num_frames = 10
        self.delay = 100

        self.ANIMATION = animation(self.activity_type, self.num_frames, self.delay)
        self.image=self.ANIMATION.get_frame()
        self.image = self.crop_image(self.image,50,50,10,10)
        self.rect = self.image.get_rect(center=(x, y))
        
        
        self.speed = 5
        self.falling_velocity = 0
        self.jump_power = -15
        self.is_on_ground = False  
        self.facing_right = True
        self.gravity = 1
    
    def crop_image(self,image, left, right, top, bottom):
        """Cắt ảnh với padding tùy chỉnh"""
        width, height = image.get_size()
        new_width = width - (left + right)
        new_height = height - (top + bottom)

        return image.subsurface(pygame.Rect(left, top, new_width, new_height)).copy()
    
    def change_animation(self, new_activity, num_frames, delay):
        """Thay đổi animation khi nhân vật di chuyển."""
        if self.activity_type != new_activity:
            self.activity_type = new_activity
            self.num_frames = num_frames
            self.delay = delay
            self.ANIMATION = animation(self.activity_type, self.num_frames, self.delay)

    def apply_gravity(self, road):
        """Áp dụng trọng lực và kiểm tra va chạm với mặt đất."""
        self.falling_velocity += self.gravity
        self.rect.y += self.falling_velocity
        self.is_on_ground = False

        for tile in road:
            if self.rect.colliderect(tile):
                if self.falling_velocity > 0:  # Nếu đang rơi xuống
                    self.rect.bottom = tile.top
                    self.falling_velocity = 0
                    self.is_on_ground = True
                elif self.falling_velocity < 0:  # Nếu đang nhảy lên
                    self.rect.top = tile.bottom
                    self.falling_velocity = 0

    def move(self, keys, road, screen_width):
        """Di chuyển nhân vật và kiểm tra va chạm."""
        from values import ANIMATION_TYPE

        dx = 0
        dy = self.falling_velocity

        # Kiểm tra phím di chuyển
        if keys[pygame.K_a] and self.rect.left > 0:
            dx = -self.speed
            self.facing_right = False
        if keys[pygame.K_d] and self.rect.right < screen_width:
            dx = self.speed
            self.facing_right = True
        if keys[pygame.K_w] and self.is_on_ground:
            self.falling_velocity = self.jump_power  # Áp dụng lực nhảy
            self.is_on_ground = False

        # Kiểm tra va chạm trục X (tránh bị kẹt vào tường)
        self.rect.x += dx
        for tile in road:
            if self.rect.colliderect(tile):
                if dx > 0:
                    self.rect.right = tile.left
                elif dx < 0:
                    self.rect.left = tile.right

        # Áp dụng trọng lực
        self.apply_gravity(road)

        # Cập nhật animation phù hợp
        if not self.is_on_ground:
            self.change_animation(ANIMATION_TYPE["jump"], 3, 100)
        elif dx != 0:
            self.change_animation(ANIMATION_TYPE["run"], 10, 100)
        else:
            self.change_animation(ANIMATION_TYPE["idle"], 10, 100)

    def draw(self, GAME):
        """Vẽ nhân vật lên màn hình và căn chỉnh hình ảnh."""
        self.ANIMATION.update()
        self.image = self.ANIMATION.get_frame()
    
        if not self.facing_right:
            self.image = pygame.transform.flip(self.image, True, False)

        GAME.blit(self.image, self.rect)
        pygame.draw.rect(GAME, (255, 0, 0), self.rect, 2)
  

print("ĐÃ CẬP NHẬT")
