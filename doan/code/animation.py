import pygame

class animation :
    def __init__(self,img,num_frames,frame_delay) :
        self.sprite_sheet=img
        self.num_frames=num_frames
        self.frame_delay=frame_delay
        self.frames=[]
        self.index_frame=0
        self.last_update=pygame.time.get_ticks()
        self.is_update=True
        self.finish=False 
        
        width = self.sprite_sheet.get_width() // num_frames
        height = self.sprite_sheet.get_height()
        
        for i in range(num_frames) :
            frame = self.sprite_sheet.subsurface(pygame.Rect(i * width, 0, width, height))
            self.frames.append(frame)
            
    def update(self,loop=True):
        if self.is_update :
            now = pygame.time.get_ticks()  
            if now - self.last_update > self.frame_delay:  
                self.index_frame = (self.index_frame + 1)  
                self.last_update = now
                if self.index_frame>=len(self.frames) :
                    if loop :
                        self.index_frame=0
                    else :
                        self.index_frame=len(self.frames)-1

    def get_frame(self):
        return self.frames[self.index_frame]
    
    
    
    
    
    
    