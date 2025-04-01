import pygame

from animation import *

class skeleton :
    def __init__(self,x,y) :
        from values import ANIMATION_SKELETON_TYPE
        
        self.activity_type=ANIMATION_SKELETON_TYPE["attack"]
        self.num_frames=18
        self.delay=100
        
        self.ANIMATION=animation(self.activity_type,self.num_frames,self.delay)
        self.image=self.ANIMATION.get_frame()
        self.rect=self.image.get_rect(bottomleft=(x,y))
        
        self.speed = 2.5
        self.falling_velocity=0
        self.is_on_ground=True 
        self.facing_right=True
        self.being_hit=False
        
        self.health=100
        self.last_hit_time=0
    
    
    def resize(self,scale_factor) :
        return (int(self.image.get_width() * scale_factor), int(self.image.get_height() * scale_factor))
    
    def change_animation(self,activity_type,num_frames,delay) :   
        if activity_type!=self.activity_type :
            self.activity_type=activity_type
            self.num_frames=num_frames
            self.delay=delay
            self.ANIMATION=animation(self.activity_type,self.num_frames,self.delay)
    
    def draw(self,GAME) :
        if self.health<=0 :
            self.ANIMATION.update(False )
        else :
            self.ANIMATION.update()
        self.image=self.ANIMATION.get_frame()
        self.image=pygame.transform.smoothscale(self.image, self.resize(2.5))
        if not self.facing_right :
            self.image=pygame.transform.flip(self.image,True ,False )
        GAME.blit(self.image,self.rect)
    
    def chasing_player(self,player_x) :
        from values import ANIMATION_SKELETON_TYPE
        if self.rect.x>player_x+10 :
            self.change_animation(ANIMATION_SKELETON_TYPE["run"],13,100)
            self.rect.x-=self.speed
            self.facing_right=False
        elif self.rect.x<player_x-10 :
            self.change_animation(ANIMATION_SKELETON_TYPE["run"],13,100)
            self.rect.x+=self.speed
            self.facing_right=True
    
    def attacking_player(self,player_x) :
        from values import ANIMATION_SKELETON_TYPE
        if self.rect.x<=player_x+20 and self.rect.x>=player_x-20 and not self.being_hit :
            self.change_animation(ANIMATION_SKELETON_TYPE["attack"],18,100)
    
    def being_attacked(self,player_x,keys) :
        from values import ANIMATION_SKELETON_TYPE
        now=pygame.time.get_ticks()
        if self.rect.x<=player_x+20 and self.rect.x>=player_x-20 and keys[pygame.K_j] :
            if not self.being_hit :
                self.being_hit=True
                self.change_animation(ANIMATION_SKELETON_TYPE["hit"],8,100)
                if now-self.last_hit_time>1000 :
                    self.health-=20
                    self.last_hit_time=now
                    if self.health<=0 :
                        self.change_animation(ANIMATION_SKELETON_TYPE["death"],15,100)
        else :
            self.being_hit=False
    
    def AI(self,player_x,keys) :
        if self.health>0 :
            self.chasing_player(player_x)
            self.attacking_player(player_x)
            self.being_attacked(player_x,keys)
    
    
print(" DA CAP NHAT ")        
        
        