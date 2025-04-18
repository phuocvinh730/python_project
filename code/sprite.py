from setting import *

class sprite(pygame.sprite.Sprite) :
    def __init__(self, pos, surf=pygame.Surface((tile_size,tile_size)), groups=None,z_layer=Z['main']):
        super().__init__(groups)
        self.image=surf
        self.rect=self.image.get_frect(topleft=pos)
        self.old_rect=self.rect.copy()
        self.z=z_layer

class animation_sprite(sprite) :
    def __init__(self, pos, frames, groups=None, z_layer=Z['main'],animation_speed=animation_speed):
        self.frames=frames
        self.frames_index=0
        super().__init__(pos,self.frames[self.frames_index], groups, z_layer)
        self.animation_speed=animation_speed

    def animated(self,fps) :
        self.frames_index+=self.animation_speed*fps
        self.image=self.frames[int(self.frames_index)%len(self.frames)]

    def update(self,fps) :
        self.animated(fps)

class movingsprite(animation_sprite) :
    def __init__(self,frames, groups, start, end,axis,speed,flip=False):
        super().__init__(start,frames, groups)
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
        self.flip=flip
        self.check_xy={'x':False,'y':False}
    
    def update(self,fps) :
        self.old_rect=self.rect.copy()
        self.rect.topleft+=self.direction*self.speed*fps
        self.comeback()
        self.animated(fps)
        if self.flip :
            self.image=pygame.transform.flip(self.image,self.check_xy['x'],self.check_xy['y'])


    def comeback(self) :
        if self.axis=='x' :
            if self.rect.right>=self.end[0] and self.direction.x==1 :
                self.direction.x=-1
                self.rect.right=self.end[0]
            if self.rect.left<=self.start[0] and self.direction.x==-1 :
                self.direction.x=1
                self.rect.left=self.start[0]
            self.check_xy['x']=True if self.direction.x<0 else False
        else :
            if self.rect.bottom>=self.end[1] and self.direction.y==1 :
                self.direction.y=-1
                self.rect.bottom=self.end[1]
            if self.rect.top<=self.start[1] and self.direction.y==-1 :
                self.direction.y=1
                self.rect.top=self.start[1]
            self.check_xy['y']=True if self.direction.y>0 else False

class spike(sprite) :
    def __init__(self, pos, surf, groups, radius,speed,start,end,z=Z['main']):
        self.center=pos
        self.radius=radius
        self.speed=speed
        self.start=start
        self.end=end
        self.angle=self.start
        self.direction=1
        self.circle=True if self.end==-1 else False
        y=self.center[1]+sin(radians(self.angle))*self.radius
        x=self.center[0]+cos(radians(self.angle))*self.radius
        super().__init__((x,y),surf,groups,z)

    def update(self,fps) :
        self.angle+=self.direction*self.speed*fps
        if not self.circle : self.direction=-1 if self.angle>=self.end else 1 if self.angle<=self.start else self.direction
        y=self.center[1]+sin(radians(self.angle))*self.radius
        x=self.center[0]+cos(radians(self.angle))*self.radius
        self.rect.center=(x,y)