from setting import *
from sprite import *
from player import *
from allsprites import *

class level :
    def __init__(self,game_display,tmx_map) :
        self.level_display=game_display
        self.all_tile=allsprites()
        self.collision_tile=pygame.sprite.Group()
        self.semi_collision_tile=pygame.sprite.Group()
        self.setup(tmx_map)

    def setup(self,tmx_map) :
        for x,y,surf in tmx_map.get_layer_by_name("Terrain").tiles() :
            sprite((x*tile_size,y*tile_size),surf,(self.all_tile,self.collision_tile,self.semi_collision_tile))
        for obj in tmx_map.get_layer_by_name("Objects") :
            if obj.name=='player' :
                self.player=player((obj.x,obj.y),self.all_tile,self.collision_tile,self.semi_collision_tile)
        for obj in tmx_map.get_layer_by_name("Moving Objects") :
            if obj.name=='helicopter' :
                if obj.width>obj.height :
                    axis='x'
                    start=(obj.x,obj.y+obj.height/2)
                    end=(obj.x+obj.width,obj.y+obj.height/2)
                else :
                    axis='y'
                    start=(obj.x+obj.width/2,obj.y)
                    end=(obj.x+obj.width/2,obj.y+obj.height)
                speed=obj.properties['speed']
                movingsprite((self.all_tile,self.semi_collision_tile),start,end,axis,speed)

    def run(self,fps) :
        self.level_display.fill(color_blue)
        self.all_tile.update(fps)
        self.all_tile.draw(self.player.hit_box_rect)