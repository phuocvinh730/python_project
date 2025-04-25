        # Vẽ input box với nền trắng + bo góc
        pygame.draw.rect(screen, (255, 255, 255), input_rect, border_radius=10)  # nền trắng
        border_color = color_active if active else color_inactive
        pygame.draw.rect(screen, border_color, input_rect, 2, border_radius=10)  # viền

        # Text màu hồng trong input
        txt_surface = small_font.render(text, True, (255, 100, 180))
        screen.blit(txt_surface, (input_rect.x + 10, input_rect.y + 10))