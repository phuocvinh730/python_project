from setting import *
from level import *
from support import *
import pygame, sys

def show_score_screen(screen):
    WIDTH, HEIGHT = game_width, game_height

    background = pygame.image.load("code/bg.jpeg")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    font = pygame.font.Font(None, 50)
    small_font = pygame.font.Font(None, 32)

    # ====== Layout dạng bảng ======
    center_x = WIDTH // 2
    top_y = 240

    label_x = center_x - 240
    label_y = top_y

    input_rect = pygame.Rect(label_x + 260, label_y, 220, 50)  # input box

    back_button = pygame.Rect(center_x - 130, top_y + 100, 120, 50)
    submit_button = pygame.Rect(center_x + 10, top_y + 100, 120, 50)

    # === LABEL (sửa để cao bằng button: 50px)
    label_text = "ENTER SCORE:"
    label_surf = small_font.render(label_text, True, (0, 150, 255))

    label_width = label_surf.get_width() + 24
    label_height = 50  # giống với button height
    label_rect = pygame.Rect(label_x, label_y, label_width, label_height)

    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')

    active = False
    text = ''
    submitted = False
    group_score = 0
    valid = False
    running = True

    while running:
        mouse_pos = pygame.mouse.get_pos()
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                active = input_rect.collidepoint(mouse_pos)

                if submit_button.collidepoint(mouse_pos) and text.strip():
                    try:
                        group_score = int(text)
                        submitted = True
                        valid = 1 <= group_score <= 10
                    except ValueError:
                        submitted = True
                        valid = False

                if back_button.collidepoint(mouse_pos):
                    running = False

            elif event.type == pygame.KEYDOWN and active:
                if event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    pass
                elif len(text) < 5 and event.unicode.isdigit():
                    text += event.unicode

        # ====== Vẽ LABEL ======
        pygame.draw.rect(screen, (255, 255, 255), label_rect, border_radius=16)
        pygame.draw.rect(screen, (0, 150, 255), label_rect, 2, border_radius=16)
        screen.blit(label_surf, (
            label_rect.centerx - label_surf.get_width() // 2,
            label_rect.centery - label_surf.get_height() // 2))  # căn giữa

        # ====== INPUT ======
        pygame.draw.rect(screen, (255, 255, 255), input_rect, border_radius=16)
        border_color = color_active if active else color_inactive
        pygame.draw.rect(screen, border_color, input_rect, 2, border_radius=16)
        txt_surface = small_font.render(text, True, (0, 0, 0))
        screen.blit(txt_surface, (input_rect.x + 10, input_rect.y + 10))

        # ====== BACK ======
        pygame.draw.rect(screen, (255, 255, 255), back_button, border_radius=16)
        pygame.draw.rect(screen, (120, 120, 120), back_button, 2, border_radius=16)
        back_label = small_font.render("BACK", True, (120, 120, 120))
        screen.blit(back_label, (
            back_button.centerx - back_label.get_width() // 2,
            back_button.centery - back_label.get_height() // 2))

        # ====== SUBMIT ======
        pygame.draw.rect(screen, (255, 255, 255), submit_button, border_radius=16)
        pygame.draw.rect(screen, (0, 180, 0), submit_button, 2, border_radius=16)
        submit_label = small_font.render("SUBMIT", True, (0, 180, 0))
        screen.blit(submit_label, (
            submit_button.centerx - submit_label.get_width() // 2,
            submit_button.centery - submit_label.get_height() // 2))

        # ====== KẾT QUẢ ======
        if submitted:
            if valid:
                result = font.render(f"GROUP SCORE: {group_score} pts", True, (255, 255, 0))
            else:
                result = small_font.render(
                    "Invalid score. Please enter a number between 1 and 10.",
                    True, (255, 50, 50))
            screen.blit(result, (WIDTH // 2 - result.get_width() // 2, top_y + 160))

        pygame.display.flip()

def show_intro_menu():
    WIDTH, HEIGHT = game_width, game_height
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("")

    # Màu sắc
    ORANGE = (255, 140, 0)
    BLUE = (30, 144, 255)
    WHITE = (255, 255, 255)
    LIGHT_BLUE = (135, 206, 250)
    PINK = (255, 100, 180)

    # Font
    title_font = pygame.font.SysFont("Arial", 52)
    name_font = pygame.font.SysFont("Arial", 28)
    button_font = pygame.font.SysFont("Arial", 28)

    # Load background
    background = pygame.image.load("code/bg.jpeg")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    # Load avatar
    def load_and_scale_avatar(path):
        img = pygame.image.load(path).convert_alpha()
        img = pygame.transform.scale(img, (140, 160))
        mask = pygame.Surface((140, 160), pygame.SRCALPHA)
        pygame.draw.rect(mask, (255, 255, 255, 255), (0, 0, 140, 160), border_radius=30)
        img.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
        return img

    avatars = {
        "Khang": load_and_scale_avatar("code/khang.png"),
        "Đăng": load_and_scale_avatar("code/dang.png"),
        "Vinh": load_and_scale_avatar("code/vinh.png"),
        "Nhi": load_and_scale_avatar("code/nhi.png")
    }

    # Vẽ nút
    def draw_button(text, x, y, w, h, color, hover_color, mouse_pos):
        if x < mouse_pos[0] < x + w and y < mouse_pos[1] < y + h:
            pygame.draw.rect(screen, hover_color, (x, y, w, h), border_radius=12)
        else:
            pygame.draw.rect(screen, color, (x, y, w, h), border_radius=12)
        label = button_font.render(text, True, WHITE)
        screen.blit(label, (x + w//2 - label.get_width()//2, y + h//2 - label.get_height()//2))

    # Vòng lặp menu
    while True:
        mouse_pos = pygame.mouse.get_pos()
        screen.blit(background, (0, 0))

        # Tiêu đề
        title = title_font.render("", True, WHITE)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 30))

        # Hiển thị avatar và tên
        names = list(avatars.keys())
        for i, name in enumerate(names):
            x = 100 + i * 220
            y = 120
            screen.blit(avatars[name], (x, y))
            pygame.draw.rect(screen, LIGHT_BLUE, (x, y + 170, 140, 40), border_radius=15)
            label = name_font.render(name.upper(), True, PINK)
            screen.blit(label, (x + 70 - label.get_width()//2, y + 190 - label.get_height()//2))

        # Các nút
        draw_button("SCORES", 250, 500, 120, 50, ORANGE, BLUE, mouse_pos)
        draw_button("START", 400, 500, 120, 50, ORANGE, BLUE, mouse_pos)
        draw_button("QUIT", 550, 500, 120, 50, ORANGE, BLUE, mouse_pos)

        # Sự kiện
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if 400 < mouse_pos[0] < 520 and 500 < mouse_pos[1] < 550:
                    return  # Bắt đầu game
                elif 550 < mouse_pos[0] < 670 and 500 < mouse_pos[1] < 550:
                    pygame.quit()
                    sys.exit()
                elif 250 < mouse_pos[0] < 370 and 500 < mouse_pos[1] < 550:
                    show_score_screen(screen)


        pygame.display.flip()


# ========== GAME CLASS ==========
class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(game_title)
        self.game_display = pygame.display.set_mode((game_width, game_height))
        self.import_assets()
        try:
            self.game_map = {0: load_pygame(join('data', 'levels', 'omni.tmx'))}
            self.load_level()
        except FileNotFoundError:
            print("Lỗi: Không tìm thấy tệp 'data/levels/omni.tmx'. Vui lòng kiểm tra thư mục hoặc cung cấp tệp bản đồ.")
            pygame.quit()
            exit()
        self.clock = pygame.time.Clock()
        self.game_run = True

    def import_assets(self):
        self.level_frames = {
            'flag': import_folder('graphics', 'level', 'flag'),
            'saw': import_folder('graphics', 'enemies', 'saw', 'animation'),
            'floor_spike': import_folder('graphics', 'enemies', 'floor_spikes'),
            'palms': import_sub_folders('graphics', 'level', 'palms'),
            'candle': import_folder('graphics', 'level', 'candle'),
            'window': import_folder('graphics', 'level', 'window'),
            'big_chain': import_folder('graphics', 'level', 'big_chains'),
            'small_chain': import_folder('graphics', 'level', 'small_chains'),
            'candle_light': import_folder('graphics', 'level', 'candle light'),
            'player': import_sub_folders('graphics', 'player'),
            'saw_chain': import_image('graphics', 'enemies', 'saw', 'saw_chain'),
            'helicopter': import_folder('graphics', 'level', 'helicopter'),
            'boat': import_folder('graphics', 'objects', 'boat'),
            'spike': import_image('graphics', 'enemies', 'spike_ball', 'Spiked Ball'),
            'spike_chain': import_image('graphics', 'enemies', 'spike_ball', 'spiked_chain'),
            'tooth': import_folder('graphics', 'enemies', 'tooth', 'run'),
            'shell': import_sub_folders('graphics', 'enemies', 'shell'),
            'pearl': import_image('graphics', 'enemies', 'bullets', 'pearl'),
            'items': import_sub_folders('graphics', 'items'),
            'particle': import_folder('graphics', 'effects', 'particle'),
            'water_top': import_folder('graphics', 'level', 'water', 'top'),
            'water_body': import_image('graphics', 'level', 'water', 'body'),
            'bg_tiles': import_folder_dict('graphics', 'level', 'bg', 'tiles'),
            'cloud_small': import_folder('graphics', 'level', 'clouds', 'small'),
            'cloud_large': import_image('graphics', 'level', 'clouds', 'large_cloud'),
            'bg_forest': import_image('graphics', 'backgrounds', 'forest'),
        }

    def load_level(self):
        if hasattr(self, 'game_level'):
            del self.game_level
        self.game_level = level(self.game_map[0], self.level_frames)

    def run(self):
        while self.game_run:
            fps = self.clock.tick(60) / 1000
            for evt in pygame.event.get():
                if evt.type == pygame.QUIT:
                    self.game_run = False
                if evt.type == pygame.KEYDOWN and evt.key == pygame.K_r and self.game_level.player.dead:
                    self.load_level()  # Reset lại level khi thua và nhấn R

            self.game_level.run(fps)
            pygame.display.update()

# ========== CHẠY CHƯƠNG TRÌNH ==========
if __name__ == '__main__':
    pygame.init()
    show_intro_menu()  # hiển thị menu đầu tiên
    game = Game()
    game.run()