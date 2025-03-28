import pygame
from Client_side.App.GameObject import *
from Client_side.App.Player import Player
from Client_side.App.Others import Others
from Client_side.App.Story import Story
from Client_side.App.Map import Map
from Client_side.App.StoryWindow import StoryWindow
from Client_side.App.AddStory import AddStory
from Client_side.App.User import User
from Client_side.App.Button import Button

class AppEngine:
    def __init__(self, client, status, width=1920, height=1080, title="Game Engine"):
        pygame.init()
        self.client = client
        self.status = status
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.running = True
        self.entities = []  # List of game entities
        self.background_color = (30, 30, 30)
        self.bStart = True
        self.player = None
        self.colliding_entity_info = None  # For collision info
        self.camera = pygame.Rect(0, 0, width, height)  # Camera view
        self.camera_speed = 5  # Speed of camera movement
        self.button_radius = 50  # Button settings
        self.read_more_button_rect = None  # Initialize it safely
        self.refresh_story = pygame.time.get_ticks()  # Track the last time stories were loaded
        self.refresh_user = pygame.time.get_ticks()  # Track the last time stories were loaded

    def add_entity(self, entity):
        """Add an entity to the game"""
        self.entities.append(entity)

    def handle_events(self):
        """Handle events like key presses or mouse clicks"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Handle button clicks
                self.handle_button_click(pygame.mouse.get_pos())

    def handle_button_click(self, mouse_pos):
        """Check if a story, the plus button, or the 'Read More' button was clicked."""
        print(f"Mouse clicked at: {mouse_pos}")  # Debugging

        # Handle Plus button click
        for entity in self.entities:
            if isinstance(entity, Button) and entity.on_click(mouse_pos):

                if entity.button_name == "add_story" :
                    self.add_story_window()

                if entity.button_name == "go_back" :
                    self.running = False



        # Check 'Read More' button click only if it exists
        if hasattr(self, 'read_more_button') and self.read_more_button.on_click(mouse_pos):
            if self.colliding_entity_info:
                self.open_story_window(self.colliding_entity_info)

    def open_story_window(self, story):
        """Open the story window for the clicked story."""
        if story:
            story_window = StoryWindow(self.screen, story.get_description())
            story_window.run(self.screen)  # Run the story window


    def add_story_window(self):
        """Start the AddStory window for adding new stories"""
        add_story_window = AddStory(self.screen, self.client, self.player.get_rect().x, self.player.get_rect().y)
        add_story_window.run()
        self.load_stories()

    def render_collision_info(self):
        """Render information about the collision on the screen"""
        if self.colliding_entity_info:
            entity_rect = self.colliding_entity_info.get_rect()
            text_x = entity_rect.centerx - self.camera.x
            text_y = entity_rect.top - 120 - self.camera.y

            # Draw info box
            info_box_width = 400
            info_box_height = 200
            corner_radius = 15
            pygame.draw.rect(self.screen, (255, 255, 255),
                             (text_x - info_box_width // 2, text_y - info_box_height // 2,
                              info_box_width, info_box_height),
                             border_radius=corner_radius)

            font = pygame.font.Font("../font.ttf", 24)
            title_font = pygame.font.Font("../font.ttf", 30)
            from_font = pygame.font.Font("../font.ttf", 20)
            preview = self.colliding_entity_info.get_description()[:35] + "..." if len(
                self.colliding_entity_info.get_description()) > 100 else self.colliding_entity_info.get_description()
            self.wrap_text_and_render(preview, font, (text_x, text_y), from_font, title_font)

            # Create the 'Read More' button dynamically
            self.read_more_button = Button("read_more", text_x - 60, text_y + 50, 120, 40, (29, 64, 99), (50, 90, 150),
                                           self.reverse_words_and_letters_in_text("קרא עוד"), border_radius=10,
                                           num_of_side=4)
            self.read_more_button.render(self.screen, self.camera)  # Draw the button

    def wrap_text_and_render(self, preview, font, text_position, from_font, title_font):
        """Wrap text to fit inside the info box and render it"""
        wrapped_lines = []
        for raw_line in preview.splitlines():
            words = raw_line.split()
            line = ""
            for word in words:
                if font.size(line + word)[0] < 400 - 50:
                    line += word + " "
                else:
                    wrapped_lines.append(line)
                    line = word + " "
            wrapped_lines.append(line)

        line_y = text_position[1] - 100
        for idx, line in enumerate(wrapped_lines):
            # Use title_font for the first line
            if idx == 0:
                line_font = from_font # Use larger font for the title or first line
            # Use secend_font for the second line
            elif idx == 1:
                line_font = title_font  # Use a different font for the second line
            else:
                line_font = font  # Use the regular font for subsequent lines

            text_surface = line_font.render(line, True, (0, 0, 0))
            self.screen.blit(text_surface, (text_position[0] - text_surface.get_width() // 2, line_y))
            line_y += text_surface.get_height() + 5


    def render(self):
        """Render all entities to the screen"""
        self.screen.fill(self.background_color)

        # Render all entities except the player
        for entity in self.entities:
            if entity is not self.player:
                entity.render(self.screen, self.camera)

        is_hover = False
        for entity in self.entities:
            if isinstance(entity, Button) and entity.is_hovered:
                is_hover = True
                break
            # Change the cursor to a hand on hover (this will now always be updated in the render)

        if is_hover or (hasattr(self, 'read_more_button') and self.read_more_button.is_hovered):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        # Render the player last to ensure it's on top
        if self.player:
            self.player.render(self.screen, self.camera)

        # Render collision info if any
        self.render_collision_info()

        pygame.display.flip()

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

    def start(self):
        """Start the game, load resources, and initialize objects"""
        print("Game is starting...")

        # Load the map
        map_entity = Map(-1920 * 2, -1080 * 2, 1920 * 5, 1080 * 5, "../assets/map.png")
        self.add_entity(map_entity)
        # Create the plus button and player
        add_story_b = Button("add_story", self.width/ 2, self.height - 60, 100, 100, (29, 64, 99), (70, 130, 180), "+", 100 / 2, 0, 75)
        self.add_entity(add_story_b)

        # Create the go back button and player
        go_back_b = Button("go_back",self.width - 200,  60, 150, 75, (29, 64, 99), (34, 72, 115), self.reverse_words_and_letters_in_text(">>יציאה"), 20, 4, 30)
        self.add_entity(go_back_b)

        self.player = Player(100, 100,  self.client.username, 50, 50, (0, 255, 0))  # Player as a green square
        self.add_entity(self.player)

        # Load and display stories from the client
        self.load_stories()

    def load_stories(self):
        """Load and place stories on the map with specific positions"""
        try:
            stories = self.client.receive_stories()
            print("Stories received:", stories)  # Debugging line

            if not stories:
                print("No stories received.")
                return

            titles, contents, usernames, positions_x, positions_y = stories

            for (title, username, content, x, y) in zip(titles, usernames, contents, positions_x, positions_y):
                print(f"Adding story at position: ({x}, {y})")  # Debugging print for positions
                story = Story(x, y, 100, 100, (255, 0, 0),
                              self.reverse_words_and_letters_in_text(f" מאת: {username}") + "\n"
                              + self.reverse_words_and_letters_in_text(title) + "\n"
                              + self.reverse_words_and_letters_in_text(content))
                self.add_entity(story)

        except Exception as e:
            print("Error while loading stories:", e)



    def update(self):
        """Update all entities in the game"""
        for entity in self.entities:
            entity.update()

        # Update camera position to follow the player
        self.camera.center = self.player.get_rect().center

        current_time = pygame.time.get_ticks()



        if current_time - self.refresh_user >= 1:  # 10 seconds
            self.create_player()
            self.refresh_user = current_time

        if current_time - self.refresh_story >= 10000:  # 10 seconds
            self.load_stories()
            self.refresh_story = current_time



    def create_player(self):
        try:
            # Send player data and receive the number of players and their details
            num_of_players, users = self.client.send_player_data(self.player.x, self.player.y)
            print(f"Number of players: {num_of_players}")

            if not users:  # Check if the list of users is empty or invalid
                print("Warning: No players found in the user list.")
                return  # Early exit if no users are present

            # First, remove entities that are no longer in the users list
            usernames_in_users = [user.username for user in users]
            self.entities = [entity for entity in self.entities if
                             not (isinstance(entity, Others) and entity.username not in usernames_in_users)]

            if num_of_players > 1:
                for user in users:
                    if not hasattr(user, 'username') or not hasattr(user, 'pos_x') or not hasattr(user, 'pos_y'):
                        print(f"Warning: Invalid user data found for {user}. Skipping.")
                        continue  # Skip this user if they don't have the expected properties

                    if user.username != self.client.username:
                        print(f"User {user.username} at position ({user.pos_x}, {user.pos_y})")

                        found = False  # Flag indicating whether the player already exists

                        for entity in self.entities:
                            if isinstance(entity, Others) and entity.username == user.username:
                                print(f"Updating {user.username}: pos_x={user.pos_x}, pos_y={user.pos_y}")
                                entity.x = user.pos_x
                                entity.y = user.pos_y
                                found = True
                                break

                        if not found:
                            # Add new player to the entities list
                            other = Others(self.player.get_rect().x, self.player.get_rect().y, user.username)
                            self.entities.append(other)
                            print(f"Added new player: {user.username}")

        except Exception as e:
            print(f"Error in create_player: {e}")



    def collide_handle(self, entities):
        """Check for collisions and store collision info for display"""
        self.colliding_entity_info = None  # Reset info on each frame
        for entity in entities:
            if isinstance(entity, Story) and self.player.get_rect().colliderect(entity.get_rect()):
                self.colliding_entity_info = entity  # Store the collided entity for rendering info

    def run(self, fps=60):
        """Main game loop"""
        if self.bStart:
            self.start()
            self.bStart = False

        try:
            while self.running and self.client.running:
                self.handle_events()
                self.update()
                self.collide_handle(self.entities)
                self.render()
                self.clock.tick(fps)
        except Exception as e:
            print("Unexpected error:", e)

        self.client.logout()
        self.status[0] = "Log_In"
        pygame.quit()
