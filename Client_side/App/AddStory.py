import pygame
from Client_side.App.Button import Button


class AddStory:
    def __init__(self, screen, client, player_pos_x, player_pos_y):
        self.screen = screen
        self.client = client
        self.player_pos_x = player_pos_x
        self.player_pos_y = player_pos_y
        self.running = True
        self.story_title = ""
        self.story_content = ""
        self.font = pygame.font.Font("../font.ttf", 24)
        self.title_font = pygame.font.Font("../font.ttf", 48)
        self.window_width, self.window_height = self.screen.get_size()
        self.bg_image = pygame.transform.scale(pygame.image.load("../assets/story.png"),
                                               (self.window_width, self.window_height))

        # Calculate center positions
        self.input_box_title = pygame.Rect((self.window_width - 500) // 2, self.window_height //  2 - 150, 500, 50)
        self.input_box_content = pygame.Rect((self.window_width - 500) // 2, self.input_box_title.y + 75, 500, 150)

        # Calculate button positions
        self.buttons = [
            Button("submit", self.window_width // 2 - 75, self.window_height // 2 + 100, 150, 50, (0, 128, 0),
                             (0, 255, 0), "Submit", border_radius=10, num_of_side=4),
            Button("back", self.window_width // 2 - 75, self.window_height // 2 + 170, 150, 50, (128, 0, 0),
                           (255, 0, 0), "Back", border_radius=10, num_of_side=4)
        ]

        self.active_input = None

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if self.active_input:
                    # Check for backspace
                    if event.key == pygame.K_BACKSPACE:
                        if self.active_input == 'title':
                            self.story_title = self.story_title[:-1]
                        elif self.active_input == 'content':
                            self.story_content = self.story_content[:-1]
                    # Check for space
                    elif event.key == pygame.K_SPACE:
                        if self.active_input == 'title':
                            self.story_title += ' '  # Add space to title
                        elif self.active_input == 'content':
                            self.story_content += ' '  # Add space to content
                    # Handle other keys
                    else:
                        if self.active_input == 'title':
                            self.story_title += event.unicode
                        elif self.active_input == 'content':
                            self.story_content += event.unicode
                    print(f"Story Title: {self.story_title}")
                    print(f"Story Content: {self.story_content}")

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the mouse click is within the title or content input box
                if self.input_box_title.collidepoint(event.pos):
                    self.active_input = 'title'
                    # If the title input box is selected, reset the title to empty string
                    self.story_title = self.story_title or ''
                elif self.input_box_content.collidepoint(event.pos):
                    self.active_input = 'content'
                    # If the content input box is selected, reset the content to empty string
                    self.story_content = self.story_content or ''
                else:
                    # Deselect if click is outside both boxes
                    self.active_input = None

                # Handle button clicks
                for button in self.buttons:
                    if button.on_click(event.pos):
                        if button.button_name == 'submit':
                            self.submit_story()
                        if button.button_name == 'back':
                            self.running = False

    def render(self):
        self.screen.blit(self.bg_image, (0, 0))

        # Title Text (Reverse the Hebrew text if it's in Hebrew)
        title_text = self.reverse_words_and_letters_in_text("הוסף סיפור")
        title_text = self.title_font.render(title_text, True, (0, 0, 0))
        title_rect = title_text.get_rect(center=(self.window_width // 2, self.input_box_title.y - 75))
        self.screen.blit(title_text, title_rect)

        # Render input boxes and text
        pygame.draw.rect(self.screen, (255, 255, 255) if self.active_input == 'title' else (200, 200, 200),
                         self.input_box_title, border_radius=5)
        pygame.draw.rect(self.screen, (255, 255, 255) if self.active_input == 'content' else (200, 200, 200),
                         self.input_box_content, border_radius=5)

        # Render Title (Right to left for Hebrew, Left to right for English)
        self.wrap_and_render_text(self.story_title, self.input_box_title)

        # Render Content Text (Right to left for Hebrew, Left to right for English)
        self.wrap_and_render_text(self.story_content, self.input_box_content)

        # Render buttons
        for button in self.buttons:
            button.render(self.screen)

        is_hover = False
        for button in self.buttons:
            if button.is_hovered:
                is_hover = True
                break

        if is_hover:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        pygame.display.flip()

    def submit_story(self):
        if self.story_title and self.story_content:
            self.client.add_story(self.story_title, "- " + self.story_content, self.client.get_user(),
                                  self.player_pos_x, self.player_pos_y)
            print("Story submitted:", self.story_title, self.story_content, self.player_pos_x, self.player_pos_y)
            self.running = False

    def wrap_and_render_text(self, text, rect):
        # Check if the text contains Hebrew characters
        is_hebrew = any(0x0590 <= ord(char) <= 0x05FF for char in text)

        if is_hebrew:
            # Reverse the text if it's Hebrew
            text = self.reverse_words_and_letters_in_text(text)

        words = text.split(' ')  # Split the text by spaces to preserve spaces
        lines = []
        current_line = ""

        for word in words:
            # Add word and check if it fits in the available width
            if self.font.size(current_line + ' ' + word)[0] <= rect.width - 20:
                if current_line:
                    current_line += ' ' + word
                else:
                    current_line = word
            else:
                # Add current line to lines list and start a new line
                lines.append(current_line)
                current_line = word

        if current_line:
            lines.append(current_line)  # Add last line if it exists

        y_offset = rect.y + 5  # Start rendering from the top of the input box
        if is_hebrew:
            # Reverse the order of lines for Hebrew (to display from bottom to top)
            lines = lines[::-1]

        for line in lines:
            rendered_text = self.font.render(line, True, (0, 0, 0))
            # Check if the line contains Hebrew text
            if any(0x0590 <= ord(char) <= 0x05FF for char in line):
                # Reverse the order of words for Hebrew text (right-to-left)
                line = ' '.join(reversed(line.split(' ')))

                # Render right to left for Hebrew text
                self.screen.blit(rendered_text, (rect.right - rendered_text.get_width() - 10, y_offset))
            else:
                # Render left to right for English or other languages
                self.screen.blit(rendered_text, (rect.x + 10, y_offset))

            y_offset += 30  # Adjust vertical spacing for each line

    def run(self):
        while self.running:
            self.handle_events()
            self.render()

    def reverse_words_and_letters_in_text(self, text):
        """Reverse the order of words and the letters in each word if it's Hebrew"""
        words = text.split()  # Split the text into words
        reversed_words = []

        for word in words[::-1]:  # Reverse the word order
            if any(0x0590 <= ord(char) <= 0x05FF for char in word):  # Check if word is Hebrew
                reversed_words.append(word[::-1])  # Reverse the letters of the word
            else:
                reversed_words.append(word)  # Leave non-Hebrew words as they are

        return ' '.join(reversed_words)
