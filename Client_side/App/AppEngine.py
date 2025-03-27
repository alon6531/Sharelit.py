import pygame
from Client_side.App.GameObject import *
from Client_side.App.Player import Player
from Client_side.App.Others import Others
from Client_side.App.Story import Story
from Client_side.App.Map import Map
from Client_side.App.StoryWindow import StoryWindow
from Client_side.App.AddStory import AddStory
from Client_side.App.PlusButton import PlusButton
from Client_side.App.User import User

class AppEngine:
    def __init__(self, client, status, width=960, height=480, title="Game Engine"):
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
                self.client.logout()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Handle button clicks
                self.handle_button_click(pygame.mouse.get_pos())

    def handle_button_click(self, mouse_pos):
        """Check if a story, the plus button, or the 'Read More' button was clicked."""
        print(f"Mouse clicked at: {mouse_pos}")  # Debugging

        # Handle Plus button click
        for entity in self.entities:
            if isinstance(entity, PlusButton) and entity.on_click(mouse_pos):
                print("Plus button clicked!")  # Debugging
                self.add_story_window()

        # Check 'Read More' button click only if it exists
        if self.read_more_button_rect and self.read_more_button_rect.collidepoint(mouse_pos):
            print("Read More button clicked!")  # Debugging
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

            # Initialize button rect position only if needed
            self.read_more_button_rect = pygame.Rect(text_x - 60, text_y + 50, 120, 40)

            # Draw info box
            info_box_width = 400
            info_box_height = 200
            corner_radius = 15
            pygame.draw.rect(self.screen, (255, 255, 255),
                             (text_x - info_box_width // 2, text_y - info_box_height // 2,
                              info_box_width, info_box_height),
                             border_radius=corner_radius)

            font = pygame.font.Font("../font.ttf", 24)
            preview = self.colliding_entity_info.get_description()[:35] + "..." if len(
                self.colliding_entity_info.get_description()) > 100 else self.colliding_entity_info.get_description()
            self.wrap_text_and_render(preview, font, (text_x, text_y))

    def draw_read_more_button(self, text_position, font):
        """Draw the 'Read More' button and store its position"""
        if self.colliding_entity_info:
            self.read_more_button_rect = pygame.Rect(text_position[0] - 60, text_position[1] + 50, 120, 40)
            pygame.draw.rect(self.screen, (29, 64, 99), self.read_more_button_rect, border_radius=10)
            button_text = font.render(self.reverse_words_and_letters_in_text("קרא עוד"), True, (255, 255, 255))
            self.screen.blit(button_text, (self.read_more_button_rect.x + 15, self.read_more_button_rect.y + 5))

    def wrap_text_and_render(self, preview, font, text_position):
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
                    line = word + " "
            wrapped_lines.append(line)

        line_y = text_position[1] - 100
        for line in wrapped_lines:
            text_surface = font.render(line, True, (0, 0, 0))
            self.screen.blit(text_surface, (text_position[0] - text_surface.get_width() // 2, line_y))
            line_y += text_surface.get_height() + 5

        self.draw_read_more_button(text_position, font)

    def render(self):
        """Render all entities to the screen"""
        self.screen.fill(self.background_color)

        # Render all entities except the player
        for entity in self.entities:
            if entity is not self.player:
                entity.render(self.screen, self.camera)

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
        plus_button = PlusButton(self.width/ 2, self.height - 60, 100, 100)
        self.add_entity(plus_button)

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
                #self.add_entity(story)

        except Exception as e:
            print("Error while loading stories:", e)



    def update(self):
        """Update all entities in the game"""
        for entity in self.entities:
            entity.update()


        # Update camera position to follow the player
        self.camera.center = self.player.get_rect().center

        current_time = pygame.time.get_ticks()



        if current_time - self.refresh_user >= 100:  # 10 seconds
            self.client.update_player(self.player.x, self.player.y)
            #self.create_player()
            self.refresh_user = current_time

        if current_time - self.refresh_story >= 10000:  # 10 seconds
            #self.load_stories()
            self.refresh_story = current_time

    def create_player(self):
        num_of_players, users = self.client.receive_all_players()

        # First, remove entities that are no longer in the users list
        usernames_in_users = [user.username for user in users]
        self.entities = [entity for entity in self.entities if
                         not (isinstance(entity, Others) and entity.username not in usernames_in_users)]

        if num_of_players > 1:
            for user in users:
                if user.username != self.client.username:
                    print(user.print_all_users())

                    found = False  # Flag indicating whether the player already exists

                    for entity in self.entities:
                        if isinstance(entity, Others) and entity.username == user.username:
                            print(f"Updating {user.username}: pos_x={user.pos_x}, pos_y={user.pos_y}")
                            entity.x = user.pos_x
                            entity.y = user.pos_y
                            found = True
                            break

                    if not found:
                        other = Others(self.player.get_rect().x, self.player.get_rect().y, user.username)
                        self.entities.append(other)
                        print("Added new player:", user.username)




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
            while self.running:
                self.handle_events()
                self.update()
                self.collide_handle(self.entities)
                self.render()
                self.clock.tick(fps)
        except Exception as e:
            print("Unexpected error:", e)

        self.status[0] = "Log_In"
        pygame.quit()
