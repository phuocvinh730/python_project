import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Ví dụ Hội Thoại")
clock = pygame.time.Clock()

# Tạo font để hiển thị văn bản
font = pygame.font.SysFont("arial", 24)

# Hàm vẽ văn bản lên surface
def draw_text(surface, text, pos, color=(255, 255, 255)):
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, pos)

# Danh sách các dòng hội thoại
dialogues = [
    "Chào bạn, đây là trò chơi của tôi.",
    "Bạn đã sẵn sàng chưa?",
    "Hãy nhấn phím SPACE để tiếp tục.",
    "Cảm ơn bạn đã chơi!"
]

dialogue_index = 0  # Vị trí dòng hội thoại hiện tại
dialogue_box_rect = pygame.Rect(50, 450, 700, 120)  # Kích thước và vị trí hộp thoại

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Chuyển sang dòng hội thoại tiếp theo khi nhấn SPACE
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                dialogue_index += 1
                if dialogue_index >= len(dialogues):
                    dialogue_index = 0  # Quay lại dòng đầu tiên hoặc có thể dừng trò chơi

    # Vẽ nền
    screen.fill((0, 0, 0))
    
    # Vẽ hộp thoại
    pygame.draw.rect(screen, (50, 50, 50), dialogue_box_rect)  # Màu nền hộp thoại
    pygame.draw.rect(screen, (255, 255, 255), dialogue_box_rect, 2)  # Viền hộp thoại

    # Vẽ văn bản hội thoại hiện tại
    if dialogue_index < len(dialogues):
        draw_text(screen, dialogues[dialogue_index], (dialogue_box_rect.x + 10, dialogue_box_rect.y + 10))
    
    pygame.display.flip()
    clock.tick(60)
