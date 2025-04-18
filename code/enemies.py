from setting import *
from timer import Timer

class tooth(pygame.sprite.Sprite) :
    def __init__(self, pos,frames,groups,collision_tile):
        super().__init__(groups)
        self.frames=frames
        self.frames_index=0
        self.image=self.frames[self.frames_index]
        self.rect=self.image.get_frect(topleft=pos)
        self.z=Z['main']
        self.direction=1
        self.collision_tile=[tile.rect for tile in collision_tile]
        self.speed=50

    def comeback(self) :
        right=pygame.FRect(self.rect.bottomright,(1,1,))
        left=pygame.FRect(self.rect.bottomleft,(-1,1,))
        self.direction=1 if left.collidelist(self.collision_tile)<0 and self.direction<0 else -1 if right.collidelist(self.collision_tile)<0 and self.direction>0 else self.direction

    def update(self,fps) :
        self.frames_index+=animation_speed*fps
        self.image=self.frames[int(self.frames_index%len(self.frames))]
        self.image=pygame.transform.flip(self.image,True,False) if self.direction<0 else self.image
        self.rect.x+=self.direction*self.speed*fps
        self.comeback()

class shell(pygame.sprite.Sprite) :
    def __init__(self,pos,frames, groups,reverse,player):
        super().__init__(groups)
        self.bullet_direction=-1 if reverse else 1
        self.frames={state:[pygame.transform.flip(surf,True,False) for surf in surfs] for state,surfs in frames.items()} if reverse else frames
        self.frames_index=0
        self.state='idle'
        self.image=self.frames[self.state][self.frames_index]
        self.rect=self.image.get_frect(topleft=pos)
        self.old_rect=self.rect.copy()
        self.z=Z['main']
        self.player=player
        self.reload_bullet=Timer(3000)
        self.fired=False

    def attack(self) :
        player_pos=Vector2(self.player.hit_box_rect.center)
        shell_pos=Vector2(self.rect.center)
        near=player_pos.distance_to(shell_pos)<500
        level=abs(player_pos.y-shell_pos.y)<30
        front=shell_pos.x<player_pos.x if self.bullet_direction>0 else shell_pos.x>player_pos.x
        if near and level and front and not self.reload_bullet.active:
            self.reload_bullet.activate()
            self.state='fire'
            self.frames_index=0

    def animated(self,fps) :
        self.frames_index+=animation_speed*fps
        if self.frames_index<len(self.frames[self.state]) :
            self.image=self.frames[self.state][int(self.frames_index)]
            if self.state=='fire' and int(self.frames_index)==3 and not self.fired :
                self.fired=True    
        else :
            self.frames_index=0
            if self.state=='fire' :
                self.state='idle'
                self.fired=False
        
    def update(self,fps) :
        self.reload_bullet.update()
        self.attack()
        self.animated(fps)
    
class bullet(pygame.sprite.Sprite) :
    def __init__(self,pos,groups,surf,direction,speed) :
        super().__init__(groups)
        self.image=surf
        self.rect=self.image.get_frect(center=pos)
        self.direction=direction
        self.speed=speed
        self.x=Z['main']
