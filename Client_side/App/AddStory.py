import pygame


class AddStory:
    def __init__(self, screen, client, player_pos_x, player_pos_y):
        self.screen = screen
        self.client = client
        self.player_pos_x = player_pos_x
        self.player_pos_y = player_pos_y
        self.running = True
        self.story_title = ""
        self.story_content = ""

        # Load custom font
        self.font = pygame.font.Font("../font.ttf", 24)  # Replace with your actual font path
        self.title_font = pygame.font.Font("../font.ttf", 48)  # Larger font for title

        # Get the window size
        self.window_width = self.screen.get_width()
        self.window_height = self.screen.get_height()

        # Load background image (it won't be resized)
        self.bg_image = pygame.image.load(
            "../assets/story.png")  # Replace with actual background image path
        self.bg_image = pygame.transform.scale(self.bg_image, (self.window_width, self.window_height))

        # UI element sizes and positions
        self.input_box_title = pygame.Rect(0, 0, 500, 50)  # Title input box
        self.input_box_content = pygame.Rect(0, 0, 500, 150)  # Content input box
        self.submit_button = pygame.Rect(0, 0, 150, 50)  # Submit button

        self.active_input = None  # No active input at the beginning
        self.inactive_color = (200, 200, 200)
        self.active_color = (255, 255, 255)

        # Calculate vertical spacing to center all elements
        total_height = self.input_box_title.height + self.input_box_content.height + self.submit_button.height + 100  # Space for title text
        vertical_padding = (self.window_height - total_height) // 2

        # Adjust the positions of all elements
        self.input_box_title.x = (self.window_width - self.input_box_title.width) // 2  # Center horizontally
        self.input_box_title.y = vertical_padding  # Center vertically

        self.input_box_content.x = (self.window_width - self.input_box_content.width) // 2
        self.input_box_content.y = self.input_box_title.y + self.input_box_title.height + 10

        self.submit_button.x = (self.window_width - self.submit_button.width) // 2
        self.submit_button.y = self.input_box_content.y + self.input_box_content.height + 20

    def handle_events(self):
        """Handle events inside the AddStory window."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and self.active_input:  # Check if an input field is active
                if event.key == pygame.K_BACKSPACE:
                    if self.active_input == 'title':
                        self.story_title = self.story_title[:-1]
                    elif self.active_input == 'content':
                        self.story_content = self.story_content[:-1]
                else:
                    if self.active_input == 'title':
                        self.story_title += event.unicode
                    elif self.active_input == 'content':
                        self.story_content += event.unicode
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.input_box_title.collidepoint(event.pos):
                    self.active_input = 'title'
                elif self.input_box_content.collidepoint(event.pos):
                    self.active_input = 'content'
                elif self.submit_button.collidepoint(event.pos):
                    self.submit_story()

    def render(self):
        """Render the AddStory window."""
        # Draw background image
        self.screen.blit(self.bg_image, (0, 0))

        # Title text: Centered at the top
        title_text = self.title_font.render(self.reverse_words_and_letters_in_text("הוסף סיפור"), True, (0, 0, 0))
        title_x = (self.window_width - title_text.get_width()) // 2  # Center horizontally
        self.screen.blit(title_text, (title_x, self.input_box_title.y - 80))  # Positioned above the input boxes

        # Title input box with rounded corners and border color
        title_box_color = self.active_color if self.active_input == 'title' else self.inactive_color
        self.draw_rounded_rect(self.input_box_title, title_box_color, 5)
        # Right-align the title text (for Hebrew text)
        title_text = self.font.render(self.reverse_words_and_letters_in_text(self.story_title), True, (0, 0, 0))
        self.screen.blit(title_text, (self.input_box_title.x + 10, self.input_box_title.y + 5))

        # Content input box with rounded corners and border color
        content_box_color = self.active_color if self.active_input == 'content' else self.inactive_color
        self.draw_rounded_rect(self.input_box_content, content_box_color, 5)
        # Wrap the text for content
        self.wrap_and_render_text(self.story_content, self.input_box_content, self.font)

        # Submit button with gradient effect
        self.draw_gradient_button(self.submit_button, (0, 128, 0), (0, 255, 0))
        submit_text = self.font.render("Submit", True, (255, 255, 255))  # White text
        self.screen.blit(submit_text, (self.submit_button.x + 10, self.submit_button.y + 10))

        pygame.display.flip()

    def submit_story(self):
        """Submit the story to the server and close the AddStory window."""
        if self.story_title and self.story_content:
            # Submit the story to the server
            self.client.add_story(self.story_title, "- " + self.story_content, self.client.get_user(), self.player_pos_x, self.player_pos_y)
            print("Story submitted:", self.story_title, self.story_content, self.player_pos_x, self.player_pos_y)

            # Close the AddStory window
            self.running = False  # This will end the AddStory window loop

    def draw_rounded_rect(self, rect, color, radius):
        """Draw a rectangle with rounded corners."""
        pygame.draw.rect(self.screen, color, rect, border_radius=radius)

    def draw_gradient_button(self, rect, start_color, end_color):
        """Draw a gradient button."""
        surface = pygame.Surface((rect.width, rect.height))
        for i in range(rect.height):
            color = [int(start_color[j] + (end_color[j] - start_color[j]) * i / rect.height) for j in range(3)]
            pygame.draw.line(surface, color, (0, i), (rect.width, i))
        self.screen.blit(surface, rect.topleft)

    def wrap_and_render_text(self, text, rect, font):
        """Wrap the text to fit inside the content input box and render it."""
        max_width = rect.width - 20  # Padding
        wrapped_text = self.wrap_text(text, font, max_width)
        y_offset = rect.y + 5  # Start from the top of the content box

        for line in wrapped_text:
            line_text = font.render(self.reverse_words_and_letters_in_text(line), True, (0, 0, 0))
            self.screen.blit(line_text, (rect.x + 10, y_offset))
            y_offset += line_text.get_height() + 5

    def wrap_text(self, text, font, max_width):
        """Wrap text so that it fits within the input box."""
        words = text.split(' ')
        lines = []
        current_line = ""

        for word in words:
            # Check if the word fits in the current line
            test_line = f"{current_line} {word}".strip()
            test_line_width = font.size(test_line)[0]

            # If the line width exceeds the max width, break the word
            if test_line_width <= max_width:
                current_line = test_line
            else:
                # If the word itself is too long to fit in the box, break it
                if font.size(word)[0] > max_width:
                    # Break the word into smaller chunks
                    while font.size(word)[0] > max_width:
                        for i in range(len(word), 0, -1):
                            part = word[:i]
                            if font.size(part)[0] <= max_width:
                                lines.append(part)
                                word = word[i:]
                                break
                else:
                    if current_line:
                        lines.append(current_line)
                    current_line = word

        # Add the last line if there is one
        if current_line:
            lines.append(current_line)

        return lines
    def reverse_words_and_letters_in_text(self, text):
        """Reverse the order of words and the letters in each word if it's Hebrew."""
        words = text.split()  # Split the text into words
        reversed_words = []

        for word in words[::-1]:  # Reverse the word order
            if any(0x0590 <= ord(char) <= 0x05FF for char in word):  # Check if word is Hebrew
                reversed_words.append(word[::-1])  # Reverse the letters of the word
            else:
                reversed_words.append(word)  # Leave non-Hebrew words as they are

        return ' '.join(reversed_words)

    def run(self):
        """Main loop for the AddStory window."""
        while self.running:
            self.handle_events()
            self.render()
