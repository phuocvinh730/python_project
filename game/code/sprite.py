from setting import *

class sprite(pygame.sprite.Sprite) :
    def __init__(self, pos, surf=pygame.Surface((tile_size,tile_size)), groups=None):
        super().__init__(groups)
        self.image=surf
        self.image.fill(color_pink)
        self.rect=self.image.get_frect(topleft=pos)
        self.old_rect=self.rect.copy()

class movingsprite(sprite) :
    def __init__(self, groups, start, end,axis,speed):
        surf=pygame.Surface((200,50))
        super().__init__(start, surf, groups)
        if axis=='x' :
            self.rect.midleft=start
        else :
            self.rect.midtop=start
        self.start=start
        self.end=end
        self.axis=axis
        self.speed=speed
        self.direction=Vector2(1,0) if axis=='x' else Vector2(0,1)
        self.moving=True
    
    def update(self,fps) :
        self.old_rect=self.rect.copy()
        self.rect.topleft+=self.direction*self.speed*fps
        self.comeback()

    def comeback(self) :
        if self.axis=='x' :
            if self.rect.right>=self.end[0] and self.direction.x==1 :
                self.direction.x=-1
                self.rect.right=self.end[0]
            if self.rect.left<=self.start[0] and self.direction.x==-1 :
                self.direction.x=1
                self.rect.left=self.start[0]
        else :
            if self.rect.bottom>=self.end[1] and self.direction.y==1 :
                self.direction.y=-1
                self.rect.bottom=self.end[1]
            if self.rect.top<=self.start[1] and self.direction.y==-1 :
                self.direction.y=1
                self.rect.top=self.start[1]