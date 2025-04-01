import pygame

class camera :
    def __init__(self,width,height,map_width,map_height) :
        self.camera_rect=pygame.Rect((0,0),(width,height))
        self.width=width
        self.height=height
        self.map_width=map_width
        self.map_height=map_height
        
    def apply(self,entity) :
        if isinstance(entity,pygame.Rect) :
            return entity.move(self.camera_rect.topleft)
        return entity.rect.move(self.camera_rect.topleft)
    
    def update(self, player):
        """ Cập nhật vị trí camera dựa trên người chơi """
        x = -player.rect.centerx + self.width // 2
        y = -player.rect.centery + self.height // 2

        # Giới hạn camera không ra ngoài map
        x = max(-(self.map_width - self.width), min(0, x))
        y = max(-(self.map_height - self.height), min(0, y))

        self.camera_rect.topleft = (x, y)
