from setting import *
from level import *

class Game :
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(game_title)
        self.game_display=pygame.display.set_mode((game_width,game_height))
        self.game_map={0:load_pygame(join('data','levels','omni.tmx'))}
        self.game_level=level(self.game_display,self.game_map[0])
        self.game_run=True
        self.clock=pygame.time.Clock()

    def run(self) :
        fps=self.clock.tick(60)/1000
        while self.game_run :
            for evt in pygame.event.get() :
                if evt.type==pygame.QUIT :
                    pygame.quit()
                    self.game_run=False

            self.game_level.run(fps)

            pygame.display.update()

if __name__=='__main__' :
    game=Game()
    game.run()    