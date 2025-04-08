from setting import *
from timer import Timer

class player(pygame.sprite.Sprite) :
    def __init__(self,pos,group,collision_tile):
        super().__init__(group)
        self.image=pygame.Surface((64,64))
        self.image.fill(color_yellow)
        self.rect=self.image.get_frect(topleft=pos)
        self.hit_box_rect=self.rect.inflate(-76,-36)
        self.old_rect=self.hit_box_rect.copy()

        self.direction=Vector2()
        self.speed=player_speed
        self.gravity=player_gravity

        self.jump_height=player_jump_height
        self.is_jump=False
        self.is_on_surface={'floor':False,"left":False,"right":False}
        self.platform=None

        self.collision_tile=collision_tile
        self.semi_collition_tile=collision_tile
        self.display=pygame.display.get_surface()

        self.timers={
            'wall_jump':Timer(400),
            'wall_slide_block':Timer(250),
            'platform_skip':Timer(200)
        }

    def input(self) :
        keys=pygame.key.get_pressed()
        self.direction=Vector2()
        if not self.timers["wall_jump"].active:
            if keys[pygame.K_a] :
                self.direction.x-=1
            if keys[pygame.K_d] :
                self.direction.x+=1
            if keys[pygame.K_s] :
                self.timers['platform_skip'].activate()
            if self.direction : self.direction.x=self.direction.normalize().x
        if keys[pygame.K_w] :
            self.is_jump=True
    
    def move(self,fps) :
        self.hit_box_rect.x+=self.direction.x*self.speed*fps
        self.collision('x')
        if not self.is_on_surface["floor"] and (self.is_on_surface["right"] or self.is_on_surface["left"]) and not self.timers['wall_slide_block'].active :
             self.direction.y=0
             self.direction.y+=self.gravity/10*fps
        else :
            self.direction.y+=self.gravity/2*fps
            self.hit_box_rect.y+=self.direction.y*fps
            self.direction.y+=self.gravity/2*fps
        if self.is_jump :
            if self.is_on_surface['floor'] :
                self.direction.y=-self.jump_height
                self.timers["wall_slide_block"].activate()
                self.hit_box_rect.bottom=-1
            elif self.is_on_surface['left'] or self.is_on_surface['right'] and not self.timers['wall_slide_block'].active :
                self.timers["wall_jump"].activate()
                self.direction.y=-self.jump_height
                self.direction.x=1 if self.is_on_surface['left'] else -1
            self.is_jump=False    
        self.collision('y')
        self.semi_collision()
        self.rect.center=self.hit_box_rect.center
        
    def collision(self,axis) :
        for tile in self.collision_tile :
            if tile.rect.colliderect(self.hit_box_rect) :
                if axis=='x' :
                    if self.hit_box_rect.left<=tile.rect.right and int(self.old_rect.left)>=tile.rect.right:
                        self.hit_box_rect.left=tile.rect.right
                    if self.hit_box_rect.right>=tile.rect.left and int(self.old_rect.right)<=tile.rect.left :
                        self.hit_box_rect.right=tile.rect.left
                else :
                    if self.hit_box_rect.top<=tile.rect.bottom and int(self.old_rect.top)>=tile.rect.bottom :
                        self.hit_box_rect.top=tile.rect.bottom
                        if hasattr(tile,"moving") :
                            self.hit_box_rect.top+=6
                    if self.hit_box_rect.bottom>=tile.rect.top and int(self.old_rect.bottom)<=tile.rect.top :
                        self.hit_box_rect.bottom=tile.rect.top
                    self.direction.y=0

    def check_surface(self) :
        right=pygame.FRect(self.hit_box_rect.topright+Vector2(0,self.hit_box_rect.height/4),(2,self.hit_box_rect.height/2))
        left=pygame.FRect(self.hit_box_rect.topleft+Vector2(-2,self.hit_box_rect.height/4),(2,self.hit_box_rect.height/2))
        bottom=pygame.FRect(self.hit_box_rect.bottomleft,(self.hit_box_rect.width,2))
        collision_block=[tile.rect for tile in self.collision_tile]
        semi_collision_block=[tile.rect for tile in self.semi_collition_tile]
        self.is_on_surface['right']=True if right.collidelist(collision_block)>=0 else False
        self.is_on_surface['left']=True if left.collidelist(collision_block)>=0 else False
        self.is_on_surface['floor']=True if bottom.collidelist(collision_block)>=0 or bottom.collidelist(semi_collision_block) and self.direction.y>0 else False
        self.platform=None
        sprites=self.collision_tile.sprites()+self.semi_collition_tile.sprites()
        for sprite in [sprite for sprite in sprites if hasattr(sprite,"moving")] :
            if bottom.colliderect(sprite) :
                self.platform=sprite

    def update_timer(self) :
        for timer in self.timers.values() :
            timer.update()

    def platform_move(self,fps) :
        if self.platform :
            self.hit_box_rect.topleft+=self.platform.direction*self.platform.speed*fps

    def semi_collision(self) :
        if self.timers['platform_skip'].active :
            for tile in self.semi_collition_tile :
                if tile.rect.colliderect(self.hit_box_rect) :
                    if self.hit_box_rect.bottom>=tile.rect.top and int(self.old_rect.bottom)<=tile.rect.top :
                            self.hit_box_rect.bottom=tile.rect.top
                            if self.direction.y>0:
                                self.direction.y=0

    def update(self,fps) :
        self.old_rect=self.hit_box_rect.copy()
        self.update_timer()
        self.input()
        self.move(fps)
        self.platform_move(fps)
        self.check_surface()
        print(self.is_on_surface)