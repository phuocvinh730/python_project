        # SUBMIT với style bo góc, nền trắng, viền xanh
        pygame.draw.rect(screen, (255, 255, 255), submit_button, border_radius=12)  # nền trắng
        pygame.draw.rect(screen, (0, 200, 0), submit_button, 4, border_radius=12)  # viền xanh
        submit_label = small_font.render("SUBMIT", True, (0, 200, 0))
        screen.blit(submit_label, (submit_button.centerx - submit_label.get_width()//2,
                                submit_button.centery - submit_label.get_height()//2))