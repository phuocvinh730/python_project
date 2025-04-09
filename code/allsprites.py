from setting import *

class allsprites(pygame.sprite.Group) :
    def __init__(self):
        super().__init__()
        self.surf=pygame.display.get_surface()
        self.offset=Vector2()

    def draw(self, pos):
        self.offset.x=-(pos[0]-game_width/2)
        self.offset.y=-(pos[1]-game_height/2)
        for tile in self :
            pos=tile.rect.topleft+self.offset
            self.surf.blit(tile.image,pos)
