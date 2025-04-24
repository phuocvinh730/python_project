from setting import *
from sprite import *
from player import *
from allsprites import *
from enemies import *

class level:
    def __init__(self, tmx_map, level_frames):
        self.level_display = pygame.display.get_surface()
        self.level_frames = level_frames
        self.all_tile = allsprites()
        self.collision_tile = pygame.sprite.Group()
        self.semi_collision_tile = pygame.sprite.Group()
        self.damage_tile = pygame.sprite.Group()
        self.tooth_tile = pygame.sprite.Group()
        self.bullet_tile = pygame.sprite.Group()
        self.enemy_tile = pygame.sprite.Group()
        self.destructible_tile = pygame.sprite.Group()  # chướng ngại vật có thể phá

        self.setup(tmx_map, level_frames)

    def setup(self, tmx_map, level_frames):
        for layer_name in ['BG', 'FG', "Terrain", 'Platforms']:
            for x, y, surf in tmx_map.get_layer_by_name(layer_name).tiles():
                group = [self.all_tile]
                group.append(self.collision_tile) if layer_name == "Terrain" else None
                group.append(self.semi_collision_tile) if layer_name == 'Platforms' else None
                match layer_name:
                    case "BG": z_layer = Z['background_tiles']
                    case "FG": z_layer = Z['fg']
                    case _: z_layer = Z['main']
                sprite((x * tile_size, y * tile_size), surf, group, z_layer)

        for obj in tmx_map.get_layer_by_name("Objects"):
            if obj.name == 'player':
                self.player = player((obj.x, obj.y), self.all_tile, self.collision_tile, self.semi_collision_tile, level_frames['player'])
            else:
                if obj.name in ['barrel', 'crate']:
                    sprite((obj.x, obj.y), obj.image, (self.all_tile, self.collision_tile))
                else:
                    if 'palm' not in obj.name:
                        frames = level_frames[obj.name]
                        animation_sprite((obj.x, obj.y), frames, self.all_tile)

        for obj in tmx_map.get_layer_by_name("Moving Objects"):
            if obj.name == 'spike':
                spike_obj = spike((obj.x + obj.width / 2, obj.y + obj.height / 2), level_frames['spike'],
                                  (self.all_tile, self.damage_tile), obj.properties['radius'], obj.properties['speed'],
                                  obj.properties['start_angle'], obj.properties['end_angle'])
                self.destructible_tile.add(spike_obj)  # thêm vào group phá được

                for i in range(0, obj.properties['radius'], 20):
                    spike((obj.x + obj.width / 2, obj.y + obj.height / 2), level_frames['spike_chain'],
                          (self.all_tile), i, obj.properties['speed'],
                          obj.properties['start_angle'], obj.properties['end_angle'], Z['background_details'])

            else:
                frames = level_frames[obj.name]
                groups = (self.all_tile, self.semi_collision_tile) if obj.properties['platform'] else (self.all_tile, self.damage_tile, obj.properties['flip'])
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

                    if obj.name == 'saw':
                        if axis == 'x':
                            y = start[1] - level_frames['saw_chain'].get_height() / 2
                            left, right = int(start[0]), int(end[0])
                            for x in range(left, right, 20):
                                sprite((x, y), level_frames['saw_chain'], self.all_tile, Z['background_details'])
                        else:
                            x = start[0] - level_frames['saw_chain'].get_width() / 2
                            top, bottom = int(start[1]), int(end[1])
                            for y in range(top, bottom, 20):
                                sprite((x, y), level_frames['saw_chain'], self.all_tile, Z['background_details'])

        for obj in tmx_map.get_layer_by_name("Enemies"):
            if obj.name == 'tooth':
                tooth((obj.x, obj.y), level_frames['tooth'],
                      (self.all_tile, self.damage_tile, self.enemy_tile, self.tooth_tile),
                      self.collision_tile)
            if obj.name == 'shell':
                shell((obj.x, obj.y), level_frames['shell'],
                      (self.all_tile, self.collision_tile, self.enemy_tile),
                      obj.properties['reverse'], self.player)

        # Gán nhóm cho player
        self.player.enemy_group = self.enemy_tile
        self.player.destructible_group = self.destructible_tile

    def run(self, fps):
        self.level_display.fill(color_blue)

        if not self.player.dead:
            self.all_tile.update(fps)
        else:
            self.player.update(fps)

        self.all_tile.draw(self.player.hit_box_rect)

        if not self.player.dead:
            if pygame.sprite.spritecollide(self.player, self.damage_tile, False, pygame.sprite.collide_rect_ratio(0.7)):
                self.player.dead = True
