import pygame

# Initialise pygame
pygame.init()

#The dimension of the game
display_width = 320
display_height = 240

#Class for the player
class Player(object):
    def __init__(self):
        self.rect = pygame.Rect(32, 32, 16, 16)

    def move(self, dx, dy):
        # Move each axis separately. Note that this checks for collisions both times.
        if dx != 0:
            self.move_single_axis(dx, 0)
        if dy != 0:
            self.move_single_axis(0, dy)

    def move_single_axis(self, dx, dy):
        # Move the rect
        self.rect.x += dx
        self.rect.y += dy

        # If you collide with a wall, move out based on velocity
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if dx > 0:  # Moving right; Hit the left side of the wall
                    self.rect.right = wall.rect.left
                if dx < 0:  # Moving left; Hit the right side of the wall
                    self.rect.left = wall.rect.right
                if dy > 0:  # Moving down; Hit the top side of the wall
                    self.rect.bottom = wall.rect.top
                if dy < 0:  # Moving up; Hit the bottom side of the wall
                    self.rect.top = wall.rect.bottom


# Class to hold a wall rect
class Wall(object):
    def __init__(self, pos):
        walls.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], 16, 16)


font = pygame.font.SysFont(None, 50)
def message_to_screen(msg,color):
    screen_text = font.render(msg, True, color)
    screen.blit(screen_text, [680/2, display_height/2])

# Set up the display
pygame.display.set_caption("Get to the red square!")
screen = pygame.display.set_mode((display_width, display_height))

clock = pygame.time.Clock()
walls = []  # List to hold the walls
player = None
end_rect = None


def reinit():
    global player, end_rect
    player = Player()  # Create the player
    # Holds the level layout in a list of strings.
    level = [
        "WWWWWWWWWWWWWWWWWWWW",
        "W                  W",
        "W         WWWWWWW  W",
        "W   WWWW        W  W",
        "W   W        WWWW  W",
        "W WWW  WWWW        W",
        "W   W     W W      W",
        "W   W     W   WWW WW",
        "W   WWW WWW   W W  W",
        "W     W   W   W W  W",
        "WWW   W   WWWWW W  W",
        "W W      WW        W",
        "W W   WWWW   WWW   W",
        "W     W        W   W",
        "WWWWWWWWWWWWEWWWWWWW",
    ]
    # Parse the level string above. W = wall, E = exit
    x = y = 0
    for row in level:
        for col in row:
            if col == "W":
                Wall((x, y))
            if col == "E":
                end_rect = pygame.Rect(x, y, 16, 16)
            x += 16
        y += 16
        x = 0
reinit()


bigfont = pygame.font.Font(None, 72)
smallfont = pygame.font.Font(None, 45)

def play_again():
    SCREEN_WIDTH = display_width
    SCREEN_HEIGHT = display_height
    textscreen = screen
    text = bigfont.render('Play again?', 13, (0, 0, 0))
    textx = SCREEN_WIDTH / 2 - text.get_width() / 2
    texty = SCREEN_HEIGHT / 2 - text.get_height() / 2
    textx_size = text.get_width()
    texty_size = text.get_height()
    pygame.draw.rect(textscreen, (255, 0, 0), ((textx - 5, texty - 5),
                                               (textx_size + 10, texty_size +
                                                10)))
    textscreen.blit(text, (SCREEN_WIDTH / 2 - text.get_width() / 2,
                       SCREEN_HEIGHT / 2 - text.get_height() / 2))
    #clock = pygame.time.Clock()
    pygame.display.flip() # Update the full display Surface to the screen
    in_main_menu = True
    while in_main_menu:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                in_main_menu = False
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                if x >= textx - 5 and x <= textx + textx_size + 5:
                    if y >= texty - 5 and y <= texty + texty_size + 5:
                        in_main_menu = False
                        return True


running = True
while running:

    clock.tick(60)

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            running = False

    # Move the player if an arrow key is pressed
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT]:
        player.move(-2, 0)
    if key[pygame.K_RIGHT]:
        player.move(2, 0)
    if key[pygame.K_UP]:
        player.move(0, -2)
    if key[pygame.K_DOWN]:
        player.move(0, 2)
    if player.rect.colliderect(end_rect):
        again = play_again()
        if again:
            reinit()
        else:
            raise SystemExit("You win!")

    # Draw the scene
    screen.fill((0, 0, 0))
    for wall in walls:
        pygame.draw.rect(screen, (255, 255, 255), wall.rect)
    pygame.draw.rect(screen, (255, 0, 0), end_rect)
    pygame.draw.rect(screen, (255, 200, 0), player.rect)
    pygame.display.flip()


    # https://www.daniweb.com/programming/threads/504827/maze-problem (“Play Again” text)
    # https://www.pygame.org/project-Rect+Collision+Response-1061-.html (background code with the algorithms)
