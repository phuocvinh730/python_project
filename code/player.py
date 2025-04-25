import pygame
from pygame.math import Vector2
from setting import *
from timer import Timer

class player(pygame.sprite.Sprite):
    def __init__(self, pos, group, collision_tile, semi_collision_tile, frames):
        super().__init__(group)
        self.frames = frames
        self.frames_index = 0
        self.state = 'idle'
        self.facing_right = True
        self.image = self.frames[self.state][self.frames_index]

        self.rect = self.image.get_frect(topleft=pos)
        self.hit_box_rect = self.rect.inflate(-76, -36)
        self.old_rect = self.hit_box_rect.copy()

        self.direction = Vector2()
        self.speed = 300        
        self.gravity = 2000     
        self.jump_height = 600  

        self.is_on_surface = {'floor': False, "left": False, "right": False}
        self.platform = None
        self.jump_pressed = False  
        self.dead = False           

        self.collision_tile = collision_tile
        self.semi_collition_tile = semi_collision_tile
        self.display = pygame.display.get_surface()
        self.z = Z['main']

        self.attacking = False
        self.enemy_group = None
        self.destructible_group = None  # Nhóm chướng ngại có thể phá

        self.timers = {
            'wall_jump': Timer(400),
            'wall_slide_block': Timer(250),
            'platform_skip': Timer(200),
            'attack': Timer(500)
        }

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = 0
        if not self.timers["wall_jump"].active:
            if keys[pygame.K_LEFT]:
                self.direction.x -= 1
                self.facing_right = False
            if keys[pygame.K_RIGHT]:
                self.direction.x += 1
                self.facing_right = True
            if keys[pygame.K_DOWN]:
                self.timers['platform_skip'].activate()
            if keys[pygame.K_SPACE]:
                self.attack()

        if keys[pygame.K_UP]:
            if self.is_on_surface['floor'] and not self.jump_pressed:
                self.direction.y = -self.jump_height
                self.jump_pressed = True
        else:
            self.jump_pressed = False

    def move(self, fps):
        self.hit_box_rect.x += self.direction.x * self.speed * fps
        self.collision('x')
        self.direction.y += self.gravity * fps
        self.hit_box_rect.y += self.direction.y * fps
        self.collision('y')
        self.semi_collision()
        self.rect.center = self.hit_box_rect.center

    def collision(self, axis):
        for tile in self.collision_tile:
            if tile.rect.colliderect(self.hit_box_rect):
                if axis == 'x':
                    if self.hit_box_rect.left <= tile.rect.right and int(self.old_rect.left) >= int(tile.old_rect.right):
                        self.hit_box_rect.left = tile.rect.right
                    if self.hit_box_rect.right >= tile.rect.left and int(self.old_rect.right) <= int(tile.old_rect.left):
                        self.hit_box_rect.right = tile.rect.left
                else:
                    if self.hit_box_rect.top <= tile.rect.bottom and int(self.old_rect.top) >= int(tile.old_rect.bottom):
                        self.hit_box_rect.top = tile.rect.bottom
                        if hasattr(tile, "moving"):
                            self.hit_box_rect.top += 6
                    if self.hit_box_rect.bottom >= tile.rect.top and int(self.old_rect.bottom) <= int(tile.old_rect.top):
                        self.hit_box_rect.bottom = tile.rect.top
                        self.direction.y = 0  

    def check_surface(self):
        bottom = pygame.Rect(self.hit_box_rect.bottomleft, (self.hit_box_rect.width, 2))
        collision_block = [tile.rect for tile in self.collision_tile]
        semi_collision_block = [tile.rect for tile in self.semi_collition_tile]
        self.is_on_surface['floor'] = (
            bottom.collidelist(collision_block) >= 0 or
            (bottom.collidelist(semi_collision_block) >= 0 and self.direction.y > 0)
        )

    def update_timer(self):
        for timer in self.timers.values():
            timer.update()

    def platform_move(self, fps):
        if self.platform:
            self.hit_box_rect.topleft += self.platform.direction * self.platform.speed * fps

    def semi_collision(self):
        if not self.timers['platform_skip'].active:
            for tile in self.semi_collition_tile:
                if tile.rect.colliderect(self.hit_box_rect):
                    if self.hit_box_rect.bottom >= tile.rect.top and int(self.old_rect.bottom) <= tile.old_rect.top:
                        self.hit_box_rect.bottom = tile.rect.top
                        if self.direction.y > 0:
                            self.direction.y = 0

    def animated(self, fps):
        self.frames_index += animation_speed * fps
        if self.state == 'attack' and self.frames_index >= len(self.frames[self.state]):
            self.state = 'idle'
        self.image = self.frames[self.state][int(self.frames_index) % len(self.frames[self.state])]
        self.image = self.image if self.facing_right else pygame.transform.flip(self.image, True, False)
        if self.attacking and self.frames_index >= len(self.frames[self.state]):
            self.attacking = False

    def what_state(self):
        if self.is_on_surface['floor']:
            self.state = 'attack' if self.attacking else 'idle' if self.direction.x == 0 else 'run'
        else:
            self.state = 'air_attack' if self.attacking else 'jump' if self.direction.y < 0 else 'fall'

    def attack(self):
        if not self.timers['attack'].active:
            self.attacking = True
            self.frames_index = 0
            self.timers['attack'].activate()
            self.hit_enemy()

    def hit_enemy(self):
        try:
            if self.enemy_group is not None:
                # Vùng tấn công phía trước
                if self.facing_right:
                    attack_rect = pygame.Rect(self.hit_box_rect.right, self.hit_box_rect.top, 60, self.hit_box_rect.height)
                else:
                    attack_rect = pygame.Rect(self.hit_box_rect.left - 60, self.hit_box_rect.top, 60, self.hit_box_rect.height)

                # DEBUG: Vẽ vùng chém ra màn hình để test
                pygame.draw.rect(self.display, (255, 0, 0), attack_rect, 2)

                for enemy in self.enemy_group.copy():  # Sử dụng copy() để tránh lỗi khi xóa
                    if attack_rect.colliderect(enemy.rect):
                        print("Enemy hit!")
                        enemy.kill()

            if self.destructible_group is not None:
                for obj in self.destructible_group.copy():
                    if self.hit_box_rect.colliderect(obj.rect):
                        obj.kill()

        except Exception as e:
            print("LỖI trong hit_enemy:", e)



    def update(self, fps):
        self.old_rect = self.hit_box_rect.copy()
        self.update_timer()
        self.input()

        if not self.dead:
            self.move(fps)
            self.platform_move(fps)
            self.check_surface()
            self.what_state()
            self.animated(fps)

        if self.rect.top > game_height + 100:
            self.dead = True

        if self.dead:
            # Vẽ div nền trắng bo góc ở giữa
            box_width, box_height = 500, 100
            box_rect = pygame.Rect(
                (game_width - box_width) // 2,
                (game_height - box_height) // 2,
                box_width,
                box_height
            )
            pygame.draw.rect(self.display, (255, 255, 255), box_rect, border_radius=15)  # nền trắng
            pygame.draw.rect(self.display, (0, 200, 0), box_rect, 4, border_radius=15)    # viền xanh lá

            # Hiển thị chữ màu xanh
            font = pygame.font.SysFont('arial', 36)
            message = 'Game Over! Press R to restart.'
            text_surf = font.render(message, True, (0, 128, 0))  # chữ xanh lá
            text_rect = text_surf.get_rect(center=box_rect.center)
            self.display.blit(text_surf, text_rect)

