from setting import *
from level import *
from support import *

class Game :
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(game_title)
        self.game_display=pygame.display.set_mode((game_width,game_height))
        self.import_assets()
        self.game_map={0:load_pygame(join('data','levels','omni.tmx'))}
        self.game_level=level(self.game_map[0],self.level_frames)
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

    def import_assets(self):
        self.level_frames={
            'flag':import_folder('graphics','level','flag'),
            'saw':import_folder('graphics','enemies','saw','animation'),
            'floor_spike':import_folder('graphics','enemies','floor_spikes'),
            'palms': import_sub_folders('graphics', 'level', 'palms'),
			'candle': import_folder('graphics','level', 'candle'),
			'window': import_folder('graphics','level', 'window'),
			'big_chain': import_folder('graphics','level', 'big_chains'),
			'small_chain': import_folder('graphics','level', 'small_chains'),
			'candle_light': import_folder('graphics','level', 'candle light'),
			'player': import_sub_folders('graphics','player'),
			'saw': import_folder('graphics', 'enemies', 'saw', 'animation'),
			'saw_chain': import_image('graphics', 'enemies', 'saw', 'saw_chain'),
			'helicopter': import_folder('graphics', 'level', 'helicopter'),
			'boat': import_folder( 'graphics', 'objects', 'boat'),
			'spike': import_image('graphics', 'enemies', 'spike_ball', 'Spiked Ball'),
			'spike_chain': import_image('graphics', 'enemies', 'spike_ball', 'spiked_chain'),
			'tooth': import_folder('graphics','enemies', 'tooth', 'run'),
			'shell': import_sub_folders('graphics','enemies', 'shell'),
			'pearl': import_image( 'graphics', 'enemies', 'bullets', 'pearl'),
			'items': import_sub_folders('graphics', 'items'),
			'particle': import_folder( 'graphics', 'effects', 'particle'),
			'water_top': import_folder('graphics', 'level', 'water', 'top'),
			'water_body': import_image('graphics', 'level', 'water', 'body'),
			'bg_tiles': import_folder_dict('graphics', 'level', 'bg', 'tiles'),
			'cloud_small': import_folder('graphics','level', 'clouds', 'small'),
			'cloud_large': import_image('graphics','level', 'clouds', 'large_cloud'),
        }


if __name__=='__main__' :
    game=Game()
    game.run()    