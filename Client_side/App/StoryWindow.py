import pygame


class StoryWindow:
    def __init__(self,screen, full_text, font_path="../font.ttf"):
        self.window_width = screen.get_width()
        self.window_height = screen.get_height()
        self.full_text = full_text
        self.font_path = font_path
        self.font = pygame.font.Font(self.font_path, 32)
        self.wrapped_text = self.wrap_text(full_text)
        self.scroll_y = 200  # Start further down for centering

    def wrap_text(self, text):
        """Wrap the text into multiple lines to fit within the screen width."""
        wrapped_text = []
        lines = text.split('\n')  # Split by newline
        for line in lines:
            words = line.split()  # Split each line into words
            wrapped_line = ""
            for word in words:
                if self.font.size(wrapped_line + word)[0] < 1600:  # Adjusted width for better centering
                    wrapped_line += word + " "
                else:
                    wrapped_text.append(wrapped_line.strip())
                    wrapped_line = word + " "
            wrapped_text.append(wrapped_line.strip())
        return wrapped_text

    def handle_events(self, button_rect):
        """Handle events like key presses or mouse clicks."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.scroll_y -= 40
                elif event.key == pygame.K_UP:
                    self.scroll_y += 40
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    return False  # Close the story window
        return True

    def render(self, screen, button_rect):
        """Render the story window with the text and the back button."""
        screen.fill((255, 255, 255))

        # Draw story text (centered)
        y = self.scroll_y
        for line in self.wrapped_text:
            text_surface = self.font.render(line, True, (0, 0, 0))
            text_x = (self.window_width - text_surface.get_width()) // 2  # Center the text
            screen.blit(text_surface, (text_x, y))
            y += text_surface.get_height() + 10

        # Draw "Back" button
        pygame.draw.rect(screen, (200, 0, 0), button_rect, border_radius=10)
        button_text = self.font.render("Back", True, (255, 255, 255))
        screen.blit(button_text, (button_rect.x + (button_rect.width - button_text.get_width()) // 2,
                                  button_rect.y + (button_rect.height - button_text.get_height()) // 2))

        pygame.display.flip()

    def run(self, screen):
        """Run the story window in a loop until closed by user."""
        button_rect = pygame.Rect(self.window_width // 2 - 100, self.window_height - 100, 200, 60)  # Back button position
        running = True

        while running:
            running = self.handle_events(button_rect)
            self.render(screen, button_rect)


