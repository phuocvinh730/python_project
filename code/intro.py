import pygame
import sys
from level import level
from setting import FPS
import pytmx
from support import load_frames  # nếu bạn có hàm này để load frame


# Khởi tạo
pygame.init()
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Meet The Team")

# Màu sắc
ORANGE = (255, 140, 0)
BLUE = (30, 144, 255)
WHITE = (255, 255, 255)
LIGHT_BLUE = (135, 206, 250)
pink = (255, 100, 180)

# Font đẹp (không cần file .ttf)
title_font = pygame.font.SysFont("Arial", 52)
name_font = pygame.font.SysFont("Arial", 28)
button_font = pygame.font.SysFont("Arial", 28)

# Load ảnh nền
background = pygame.image.load("bg.jpeg")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Hàm load avatar nhỏ lại + bo góc
def load_and_scale_avatar(path):
    img = pygame.image.load(path).convert_alpha()
    img = pygame.transform.scale(img, (140, 160))  # nhỏ lại
    # Tạo mask hình tròn bo góc
    mask = pygame.Surface((140, 160), pygame.SRCALPHA)
    pygame.draw.rect(mask, (255, 255, 255, 255), (0, 0, 140, 160), border_radius=30)
    img.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
    return img

avatars = {
    "Khang": load_and_scale_avatar("khang.png"),
    "Đăng": load_and_scale_avatar("dang.png"),
    "Vinh": load_and_scale_avatar("vinh.png"),
    "Nhi": load_and_scale_avatar("nhi.png")
}

# Vẽ button
def draw_button(text, x, y, w, h, color, hover_color, mouse_pos):
    if x < mouse_pos[0] < x + w and y < mouse_pos[1] < y + h:
        pygame.draw.rect(screen, hover_color, (x, y, w, h), border_radius=12)
    else:
        pygame.draw.rect(screen, color, (x, y, w, h), border_radius=12)
    label = button_font.render(text, True, WHITE)
    screen.blit(label, (x + w//2 - label.get_width()//2, y + h//2 - label.get_height()//2))

# Main loop
def run_game_level():
    tmx_map = pytmx.load_pygame("level1.tmx")  # tên bản đồ Tiled của bạn
    level_frames = load_frames()               # hàm tự viết để load sprite animation
    game_level = level(tmx_map, level_frames)

    clock = pygame.time.Clock()
    running = True
    while running:
        dt = clock.tick(FPS) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        game_level.run(dt)
        pygame.display.update()

    pygame.quit()
    sys.exit()
running = True
while running:
    mouse_pos = pygame.mouse.get_pos()
    screen.blit(background, (0, 0))

    # Tiêu đề
    title = title_font.render("", True, WHITE)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 30))

    # Hiển thị thành viên
    names = list(avatars.keys())
    for i, name in enumerate(names):
        x = 100 + i * 220
        y = 120
        # Avatar
        screen.blit(avatars[name], (x, y))
        # Ô chứa tên
        pygame.draw.rect(screen, LIGHT_BLUE, (x, y + 170, 140, 40), border_radius=15)
        label = name_font.render(name.upper(), True, pink)
        screen.blit(label, (x + 70 - label.get_width()//2, y + 190 - label.get_height()//2))

    # Các nút
    draw_button("SCORES", 250, 500, 120, 50, ORANGE, BLUE, mouse_pos)
    draw_button("START", 400, 500, 120, 50, ORANGE, BLUE, mouse_pos)
    draw_button("QUIT", 550, 500, 120, 50, ORANGE, BLUE, mouse_pos)

    # Sự kiện
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if 250 < mouse_pos[0] < 370 and 500 < mouse_pos[1] < 550:
                print("SCORES button clicked")  # xử lý sau nếu bạn muốn
            elif 400 < mouse_pos[0] < 520 and 500 < mouse_pos[1] < 550:
                run_game_level()  # chạy game
            elif 550 < mouse_pos[0] < 670 and 500 < mouse_pos[1] < 550:
                running = False


    pygame.display.flip()


pygame.quit()
sys.exit()
