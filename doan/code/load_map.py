import pytmx
import pygame

class map :
    def __init__(self,file_map,map_width=1200) :
        self.map_width=map_width
        self.file_map=pytmx.load_pygame(file_map, pixelalpha=True)
        
    def collision_blocks(self,GAME,camera) :
        COLLISION_BLOCK=[]
        for layer in self.file_map.visible_layers :
            if isinstance(layer,pytmx.TiledTileLayer) :
                for x,y,gid in layer :
                    if gid==0 : continue
                    gid_properties=self.file_map.get_tile_properties_by_gid(gid)
                    if gid_properties and gid_properties.get("collision")==True :
                        rect=pygame.Rect(x*self.file_map.tilewidth,y*self.file_map.tileheight,self.file_map.tilewidth,self.file_map.tileheight)
                        camera.apply(rect)
                        COLLISION_BLOCK.append(rect)
        return COLLISION_BLOCK           
    
    def draw_map(self,GAME,camera) :
        for layer in self.file_map.visible_layers :
            if isinstance(layer,pytmx.TiledTileLayer) :
                for x,y,gid in layer :
                    if gid==0 : continue
                    img=self.file_map.get_tile_image_by_gid(gid)
                    tile_rect=pygame.Rect(x*self.file_map.tilewidth,y*self.file_map.tileheight,self.file_map.tilewidth,self.file_map.tileheight)
                    rect=camera.apply(tile_rect)
                    GAME.blit(img,tile_rect)
        
                    