import pygame
from Client_side.App.Button import Button  # Assuming the Button class is in Button.py


class StoryWindow:
    def __init__(self, screen, full_text, bg_image_path="../assets/storywin.png", font_path="../font.ttf"):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        self.window_width = screen.get_width()
        self.window_height = screen.get_height()
        self.full_text = full_text
        self.font_path = font_path
        self.font = pygame.font.Font(self.font_path, 32)
        self.small_font = pygame.font.Font(self.font_path, 24)
        from_font = pygame.font.Font(self.font_path, 26)
        from_font.set_italic(True)  # Makes the font italic
        title_font = pygame.font.Font(self.font_path, 40)
        title_font.set_underline(True)  # Makes the font underlined
        self.wrapped_text = self.wrap_text(full_text, self.font, from_font, title_font)
        self.scroll_y = 200  # Start further down for centering

        # Load the background image
        self.bg_image = pygame.image.load(bg_image_path)
        self.bg_image = pygame.transform.scale(self.bg_image, (self.window_width, self.window_height))  # Scale it to fit the screen

        # Create the back button using the Button class
        self.back_button = Button(
            button_name="Back",
            x=self.window_width // 2 - 100,
            y=self.window_height - 150,
            width=200,
            height=60,
            color=(210, 148, 34),
            hover_color=(255, 171, 15),
            text="Back",
            border_radius=10,
            num_of_side=4,  # Rectangle shape
            text_size=32
        )

    def wrap_text(self, text, font, from_font, title_font):
        """Wrap the text into multiple lines to fit within the screen width."""
        wrapped_text = []
        lines = text.split('\n')  # Split by newline

        for idx, line in enumerate(lines):
            words = line.split()  # Split each line into words
            wrapped_line = ""

            # Use different fonts based on the line index and line length
            if idx == 0:
                line_font = from_font  # Use from_font for the first line
            elif idx == 1:
                line_font = title_font  # Use title_font for the second line
            else:
                if len(line) > 100:  # Check if the line exceeds 100 characters
                    line_font = self.small_font  # Use small font for longer lines
                else:
                    line_font = font  # Use regular font for shorter lines

            for word in words:
                if line_font.size(wrapped_line + word)[
                    0] < self.window_width // 2:  # Adjusted width for better centering
                    wrapped_line += word + " "
                else:
                    wrapped_text.append((wrapped_line.strip(), line_font))  # Store wrapped line with font
                    wrapped_line = word + " "

            wrapped_text.append((wrapped_line.strip(), line_font))  # Store the last wrapped line with font

        # Reverse the order of lines starting from the third one
        if len(wrapped_text) > 2:
            wrapped_text[2:] = wrapped_text[2:][::-1]

        return wrapped_text

    def handle_events(self):
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
                if self.back_button.on_click(event.pos):
                    return False  # Close the story window
        return True

    def render(self, screen):
        """Render the story window with the text and the back button."""
        screen.fill((255, 255, 255))

        # Draw the background image
        screen.blit(self.bg_image, (0, 0))  # Draw the background

        # Draw story text (centered)
        y = self.scroll_y
        for line, line_font in self.wrapped_text:  # Unpack the line and its corresponding font
            text_surface = line_font.render(line, True, (69, 78, 48))  # Use the correct font for each line
            text_x = (self.window_width - text_surface.get_width()) // 2  # Center the text
            screen.blit(text_surface, (text_x, y))
            y += text_surface.get_height() + 10

        if self.back_button.is_hovered:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        # Render the back button
        self.back_button.render(screen)

        pygame.display.flip()

    def run(self, screen):
        """Run the story window in a loop until closed by user."""
        running = True

        while running:
            running = self.handle_events()
            self.render(screen)
