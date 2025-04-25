from setting import *
from sprite import *
from player import *
from allsprites import *
from enemies import *

class level:
    def __init__(self, tmx_map, level_frames,player_name):
        self.level_display = pygame.display.get_surface()
        self.player_name = player_name

        self.level_frames = level_frames
        
        self.bg_surface = pygame.transform.scale(
            self.level_frames['bg_forest'], (game_width, game_height)
        )
        
        self.all_tile = allsprites()
        self.collision_tile = pygame.sprite.Group()
        self.semi_collision_tile = pygame.sprite.Group()
        self.damage_tile = pygame.sprite.Group()
        self.tooth_tile = pygame.sprite.Group()
        self.bullet_tile = pygame.sprite.Group()
        self.enemy_tile = pygame.sprite.Group()
        self.destructible_tile = pygame.sprite.Group()
        self.setup(tmx_map, level_frames)
        self.enemy_group = self.enemy_tile 

    def setup(self, tmx_map, level_frames):
        for layer_name in ['BG', 'FG', "Terrain", 'Platforms']:
            for x, y, surf in tmx_map.get_layer_by_name(layer_name).tiles():
                group = [self.all_tile]
                if layer_name == "Terrain":
                    group.append(self.collision_tile)
                if layer_name == "Platforms":
                    group.append(self.semi_collision_tile)
                match layer_name:
                    case "BG":
                        z_layer = Z['background_tiles']
                    case "FG":
                        z_layer = Z['fg']
                    case _:
                        z_layer = Z['main']
                sprite((x * tile_size, y * tile_size), surf, group, z_layer)

        for obj in tmx_map.get_layer_by_name("Objects"):
            if obj.name == 'player':
                self.player = player(
                    (obj.x, obj.y),
                    self.all_tile,
                    self.collision_tile,
                    self.semi_collision_tile,
                    level_frames['player'],
                    self.player_name
                )
            else:
                if obj.name in ['barrel', 'crate']:
                    sprite((obj.x, obj.y), obj.image, (self.all_tile, self.collision_tile))
                elif 'palm' not in obj.name:
                    frames = level_frames[obj.name]
                    animation_sprite((obj.x, obj.y), frames, self.all_tile)

        for obj in tmx_map.get_layer_by_name("Moving Objects"):
            if obj.name == 'spike':
                spike_obj = spike((obj.x + obj.width / 2, obj.y + obj.height / 2), level_frames['spike'],
                                  (self.all_tile, self.damage_tile), obj.properties['radius'], obj.properties['speed'],
                                  obj.properties['start_angle'], obj.properties['end_angle'])
                self.destructible_tile.add(spike_obj)  # thêm vào group phá được

                for i in range(0, obj.properties['radius'], 20):
                    spike(
                        (obj.x + obj.width / 2, obj.y + obj.height / 2),
                        level_frames['spike_chain'],
                        (self.all_tile,),
                        i,
                        obj.properties['speed'],
                        obj.properties['start_angle'],
                        obj.properties['end_angle'],
                        Z['background_details']
                    )
            else:
                frames = level_frames[obj.name]
                groups = (self.all_tile, self.semi_collision_tile) if obj.properties.get('platform', False) else (self.all_tile, self.damage_tile)

                if obj.name == 'helicopter':
                    if obj.width > obj.height:
                        axis = 'x'
                        start = (obj.x, obj.y + obj.height / 2)
                        end = (obj.x + obj.width, obj.y + obj.height / 2)
                    else:
                        axis = 'y'
                        start = (obj.x + obj.width / 2, obj.y)
                        end = (obj.x + obj.width / 2, obj.y + obj.height)

                    speed = obj.properties['speed']
                    movingsprite(frames, groups, start, end, axis, speed)

        for obj in tmx_map.get_layer_by_name("Enemies"):
            if obj.name == 'tooth':
                tooth(
                    (obj.x, obj.y),
                    level_frames['tooth'],
                    (self.all_tile, self.damage_tile, self.enemy_tile, self.tooth_tile),
                    self.collision_tile
                )

            if obj.name == 'shell':
                shell((obj.x, obj.y), level_frames['shell'],
                      (self.all_tile, self.collision_tile, self.enemy_tile),
                      obj.properties['reverse'], self.player)

        # Gán nhóm cho player
        self.player.enemy_group = self.enemy_tile
        self.player.destructible_group = self.destructible_tile


    def run(self, fps):
        self.level_display.blit(self.bg_surface, (0, 0))

        if not self.player.dead:
            self.all_tile.update(fps)
            self.player.bullet_group.update(fps)
        else:
            self.player.update(fps)

        # --- Tính offset camera ---
        offset_x = -self.player.hit_box_rect.x + game_width // 2
        offset_y = -self.player.hit_box_rect.y + game_height // 2

        # --- Vẽ tile ---
        self.all_tile.draw(self.player.hit_box_rect)

        # --- Vẽ bullet ---
        for bullet in self.player.bullet_group:
            bullet_rect = bullet.rect.move(offset_x, offset_y)
            self.level_display.blit(bullet.image, bullet_rect)

        # --- Vẽ tên player trên đầu ---
        self.player.draw_name(offset_x, offset_y)

        # --- Kiểm tra bullet trúng enemy ---
        for bullet in self.player.bullet_group.copy():
            hits = pygame.sprite.spritecollide(bullet, self.enemy_group, True)
            if hits:
                bullet.kill()

        # --- Update player ---
        self.player.update(fps)

        # --- Kiểm tra player chết bởi tile nguy hiểm ---
        if not self.player.dead:
            if pygame.sprite.spritecollide(self.player, self.damage_tile, False, pygame.sprite.collide_rect_ratio(0.7)):
                self.player.dead = True

        # --- Vẽ điểm số ---
        score_font = pygame.font.SysFont('Arial', 48)
        score_surface = score_font.render(f"Score: {self.player.score}", True, (255, 255, 255))
        self.level_display.blit(score_surface, (20, 20))

