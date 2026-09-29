import pygame
import random
import sys
import math
import array

# ============================================================
# INITIALIZATION
# ============================================================

pygame.init()
pygame.mixer.init()

WIDTH = 900
HEIGHT = 700

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()
FPS = 60


# ============================================================
# COLORS
# ============================================================

BACKGROUND = (15, 18, 25)
GRID_COLOR = (30, 35, 45)

WHITE = (245, 245, 245)
GRAY = (150, 155, 165)

GREEN = (70, 210, 100)
DARK_GREEN = (35, 140, 65)

RED = (230, 70, 75)
YELLOW = (245, 210, 70)

BLUE = (70, 150, 240)
BUTTON = (55, 60, 80)
BUTTON_HOVER = (75, 82, 110)


# ============================================================
# FONTS
# ============================================================

title_font = pygame.font.Font(None, 80)
large_font = pygame.font.Font(None, 60)
medium_font = pygame.font.Font(None, 40)
small_font = pygame.font.Font(None, 28)


# ============================================================
# SOUND GENERATOR
# ============================================================

def create_sound(frequency, duration):

    sample_rate = 44100

    samples = int(sample_rate * duration)

    buffer = array.array("h")

    for i in range(samples):

        value = int(
            16000 *
            math.sin(
                2 * math.pi *
                frequency *
                i /
                sample_rate
            )
        )

        buffer.append(value)

    return pygame.mixer.Sound(buffer=buffer)


eat_sound = create_sound(900, 0.08)
move_sound = create_sound(350, 0.03)
game_over_sound = create_sound(180, 0.35)
click_sound = create_sound(600, 0.08)
countdown_sound = create_sound(700, 0.12)
win_sound = create_sound(1000, 0.25)


# ============================================================
# GAME SETTINGS
# ============================================================

CELL_SIZE = 25

GRID_WIDTH = 32
GRID_HEIGHT = 20

GAME_WIDTH = GRID_WIDTH * CELL_SIZE
GAME_HEIGHT = GRID_HEIGHT * CELL_SIZE

GAME_X = 50
GAME_Y = 150


# ============================================================
# GAME STATES
# ============================================================

game_state = "menu"

# menu
# countdown
# playing
# paused
# game_over


# ============================================================
# BUTTONS
# ============================================================

play_button = pygame.Rect(
    300, 300, 300, 70
)

quit_button = pygame.Rect(
    300, 400, 300, 70
)

restart_button = pygame.Rect(
    250, 500, 180, 65
)

menu_button = pygame.Rect(
    470, 500, 180, 65
)


# ============================================================
# GAME VARIABLES
# ============================================================

snake = []

direction = (1, 0)
next_direction = (1, 0)

food = None

score = 0
high_score = 0

snake_speed = 8

last_move_time = 0

countdown_start = 0
countdown = 3


# ============================================================
# TEXT FUNCTION
# ============================================================

def draw_text(
    text,
    font,
    color,
    x,
    y,
    center=True
):

    surface = font.render(
        text,
        True,
        color
    )

    if center:

        rect = surface.get_rect(
            center=(x, y)
        )

    else:

        rect = surface.get_rect(
            topleft=(x, y)
        )

    screen.blit(
        surface,
        rect
    )


# ============================================================
# BUTTON FUNCTION
# ============================================================

def draw_button(
    rect,
    text,
    mouse_pos
):

    if rect.collidepoint(mouse_pos):

        color = BUTTON_HOVER

    else:

        color = BUTTON

    pygame.draw.rect(
        screen,
        color,
        rect,
        border_radius=15
    )

    pygame.draw.rect(
        screen,
        WHITE,
        rect,
        2,
        border_radius=15
    )

    draw_text(
        text,
        medium_font,
        WHITE,
        rect.centerx,
        rect.centery
    )


# ============================================================
# CREATE FOOD
# ============================================================

def create_food():

    while True:

        x = random.randint(
            0,
            GRID_WIDTH - 1
        )

        y = random.randint(
            0,
            GRID_HEIGHT - 1
        )

        position = (x, y)

        if position not in snake:

            return position


# ============================================================
# RESET GAME
# ============================================================

def reset_game():

    global snake
    global direction
    global next_direction
    global food
    global score
    global snake_speed
    global game_state
    global countdown_start
    global countdown

    snake = [
        (10, 10),
        (9, 10),
        (8, 10)
    ]

    direction = (1, 0)
    next_direction = (1, 0)

    food = create_food()

    score = 0

    snake_speed = 8

    countdown = 3

    countdown_start = pygame.time.get_ticks()

    game_state = "countdown"


# ============================================================
# DRAW GRID
# ============================================================

def draw_grid():

    for x in range(GRID_WIDTH + 1):

        pygame.draw.line(
            screen,
            GRID_COLOR,
            (
                GAME_X + x * CELL_SIZE,
                GAME_Y
            ),
            (
                GAME_X + x * CELL_SIZE,
                GAME_Y + GAME_HEIGHT
            )
        )

    for y in range(GRID_HEIGHT + 1):

        pygame.draw.line(
            screen,
            GRID_COLOR,
            (
                GAME_X,
                GAME_Y + y * CELL_SIZE
            ),
            (
                GAME_X + GAME_WIDTH,
                GAME_Y + y * CELL_SIZE
            )
        )


# ============================================================
# DRAW SNAKE
# ============================================================

def draw_snake():

    for index, segment in enumerate(snake):

        x, y = segment

        rect = pygame.Rect(
            GAME_X + x * CELL_SIZE + 2,
            GAME_Y + y * CELL_SIZE + 2,
            CELL_SIZE - 4,
            CELL_SIZE - 4
        )

        if index == 0:

            color = GREEN

        else:

            color = DARK_GREEN

        pygame.draw.rect(
            screen,
            color,
            rect,
            border_radius=7
        )

    # Draw eyes on snake head

    head_x, head_y = snake[0]

    center_x = (
        GAME_X +
        head_x * CELL_SIZE +
        CELL_SIZE // 2
    )

    center_y = (
        GAME_Y +
        head_y * CELL_SIZE +
        CELL_SIZE // 2
    )

    eye_radius = 3

    if direction == (1, 0):

        eye_positions = [
            (center_x + 6, center_y - 5),
            (center_x + 6, center_y + 5)
        ]

    elif direction == (-1, 0):

        eye_positions = [
            (center_x - 6, center_y - 5),
            (center_x - 6, center_y + 5)
        ]

    elif direction == (0, -1):

        eye_positions = [
            (center_x - 5, center_y - 6),
            (center_x + 5, center_y - 6)
        ]

    else:

        eye_positions = [
            (center_x - 5, center_y + 6),
            (center_x + 5, center_y + 6)
        ]

    for eye in eye_positions:

        pygame.draw.circle(
            screen,
            WHITE,
            eye,
            eye_radius
        )


# ============================================================
# DRAW FOOD
# ============================================================

def draw_food():

    x, y = food

    center_x = (
        GAME_X +
        x * CELL_SIZE +
        CELL_SIZE // 2
    )

    center_y = (
        GAME_Y +
        y * CELL_SIZE +
        CELL_SIZE // 2
    )

    # Apple body

    pygame.draw.circle(
        screen,
        RED,
        (
            center_x,
            center_y + 2
        ),
        8
    )

    # Apple leaf

    pygame.draw.ellipse(
        screen,
        GREEN,
        (
            center_x + 3,
            center_y - 11,
            8,
            5
        )
    )

    # Stem

    pygame.draw.line(
        screen,
        DARK_GREEN,
        (
            center_x,
            center_y - 7
        ),
        (
            center_x + 2,
            center_y - 13
        ),
        2
    )


# ============================================================
# DRAW SCORE
# ============================================================

def draw_score():

    draw_text(
        f"Score: {score}",
        medium_font,
        WHITE,
        150,
        80
    )

    draw_text(
        f"High Score: {high_score}",
        medium_font,
        YELLOW,
        450,
        80
    )

    draw_text(
        f"Speed: {snake_speed}",
        medium_font,
        BLUE,
        750,
        80
    )


# ============================================================
# MOVE SNAKE
# ============================================================

def move_snake():

    global snake
    global food
    global score
    global snake_speed
    global game_state
    global high_score

    head_x, head_y = snake[0]

    dx, dy = next_direction

    new_head = (
        head_x + dx,
        head_y + dy
    )

    # Wall collision

    if (
        new_head[0] < 0
        or
        new_head[0] >= GRID_WIDTH
        or
        new_head[1] < 0
        or
        new_head[1] >= GRID_HEIGHT
    ):

        game_over()

        return

    # Self collision

    if new_head in snake:

        game_over()

        return

    snake.insert(
        0,
        new_head
    )

    # Food collision

    if new_head == food:

        score += 1

        eat_sound.play()

        if score > high_score:

            high_score = score

        # Increase speed

        snake_speed = min(
            20,
            8 + score // 2
        )

        food = create_food()

    else:

        snake.pop()


# ============================================================
# GAME OVER
# ============================================================

def game_over():

    global game_state

    game_state = "game_over"

    game_over_sound.play()


# ============================================================
# START COUNTDOWN
# ============================================================

def start_game():

    global game_state

    reset_game()

    click_sound.play()


# ============================================================
# UPDATE COUNTDOWN
# ============================================================

def update_countdown():

    global countdown
    global game_state

    current_time = pygame.time.get_ticks()

    elapsed = (
        current_time -
        countdown_start
    ) / 1000

    countdown = 3 - int(elapsed)

    if elapsed >= 3:

        game_state = "playing"


# ============================================================
# DRAW GAME AREA
# ============================================================

def draw_game_area():

    pygame.draw.rect(
        screen,
        (22, 25, 34),
        (
            GAME_X,
            GAME_Y,
            GAME_WIDTH,
            GAME_HEIGHT
        )
    )

    draw_grid()


# ============================================================
# MAIN GAME LOOP
# ============================================================

running = True

while running:

    mouse_pos = pygame.mouse.get_pos()

    # ========================================================
    # EVENTS
    # ========================================================

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False

        # ====================================================
        # KEYBOARD
        # ====================================================

        if event.type == pygame.KEYDOWN:

            # Pause

            if event.key == pygame.K_p:

                if game_state == "playing":

                    game_state = "paused"

                    click_sound.play()

                elif game_state == "paused":

                    game_state = "playing"

                    click_sound.play()

            # Restart

            if event.key == pygame.K_r:

                if (
                    game_state == "playing"
                    or
                    game_state == "paused"
                    or
                    game_state == "game_over"
                ):

                    reset_game()

            # Quit

            if event.key == pygame.K_ESCAPE:

                running = False

            # Snake movement

            if game_state == "playing":

                if (
                    event.key == pygame.K_UP
                    and
                    direction != (0, 1)
                ):

                    next_direction = (0, -1)

                elif (
                    event.key == pygame.K_DOWN
                    and
                    direction != (0, -1)
                ):

                    next_direction = (0, 1)

                elif (
                    event.key == pygame.K_LEFT
                    and
                    direction != (1, 0)
                ):

                    next_direction = (-1, 0)

                elif (
                    event.key == pygame.K_RIGHT
                    and
                    direction != (-1, 0)
                ):

                    next_direction = (1, 0)

        # ====================================================
        # MENU MOUSE EVENTS
        # ====================================================

        if game_state == "menu":

            if event.type == pygame.MOUSEBUTTONDOWN:

                if play_button.collidepoint(
                    event.pos
                ):

                    start_game()

                elif quit_button.collidepoint(
                    event.pos
                ):

                    running = False

        # ====================================================
        # GAME OVER EVENTS
        # ====================================================

        elif game_state == "game_over":

            if event.type == pygame.MOUSEBUTTONDOWN:

                if restart_button.collidepoint(
                    event.pos
                ):

                    reset_game()

                    click_sound.play()

                elif menu_button.collidepoint(
                    event.pos
                ):

                    game_state = "menu"

                    click_sound.play()

        # ====================================================
        # PAUSE EVENTS
        # ====================================================

        elif game_state == "paused":

            if event.type == pygame.MOUSEBUTTONDOWN:

                if menu_button.collidepoint(
                    event.pos
                ):

                    game_state = "menu"

                    click_sound.play()

    # ========================================================
    # GAME LOGIC
    # ========================================================

    if game_state == "countdown":

        update_countdown()

    elif game_state == "playing":

        current_time = pygame.time.get_ticks()

        move_delay = 1000 / snake_speed

        if (
            current_time -
            last_move_time
            >= move_delay
        ):

            direction = next_direction

            move_snake()

            last_move_time = current_time

    # ========================================================
    # DRAW BACKGROUND
    # ========================================================

    screen.fill(BACKGROUND)

    # ========================================================
    # MENU
    # ========================================================

    if game_state == "menu":

        draw_text(
            "SNAKE",
            title_font,
            GREEN,
            WIDTH // 2,
            150
        )

        draw_text(
            "CLASSIC PYTHON GAME",
            medium_font,
            GRAY,
            WIDTH // 2,
            220
        )

        draw_button(
            play_button,
            "PLAY",
            mouse_pos
        )

        draw_button(
            quit_button,
            "QUIT",
            mouse_pos
        )

        draw_text(
            "Arrow Keys = Move    P = Pause    R = Restart",
            small_font,
            GRAY,
            WIDTH // 2,
            550
        )

    # ========================================================
    # COUNTDOWN
    # ========================================================

    elif game_state == "countdown":

        draw_score()

        draw_game_area()

        draw_snake()

        draw_food()

        draw_text(
            str(max(1, countdown)),
            title_font,
            YELLOW,
            WIDTH // 2,
            620
        )

    # ========================================================
    # PLAYING
    # ========================================================

    elif game_state == "playing":

        draw_score()

        draw_game_area()

        draw_snake()

        draw_food()

    # ========================================================
    # PAUSED
    # ========================================================

    elif game_state == "paused":

        draw_score()

        draw_game_area()

        draw_snake()

        draw_food()

        # Transparent pause panel

        overlay = pygame.Surface(
            (WIDTH, HEIGHT),
            pygame.SRCALPHA
        )

        overlay.fill(
            (0, 0, 0, 130)
        )

        screen.blit(
            overlay,
            (0, 0)
        )

        draw_text(
            "PAUSED",
            title_font,
            WHITE,
            WIDTH // 2,
            250
        )

        draw_text(
            "Press P to continue",
            medium_font,
            GRAY,
            WIDTH // 2,
            330
        )

        draw_button(
            menu_button,
            "MAIN MENU",
            mouse_pos
        )

    # ========================================================
    # GAME OVER
    # ========================================================

    elif game_state == "game_over":

        draw_score()

        draw_game_area()

        draw_snake()

        draw_food()

        overlay = pygame.Surface(
            (WIDTH, HEIGHT),
            pygame.SRCALPHA
        )

        overlay.fill(
            (0, 0, 0, 160)
        )

        screen.blit(
            overlay,
            (0, 0)
        )

        draw_text(
            "GAME OVER",
            title_font,
            RED,
            WIDTH // 2,
            230
        )

        draw_text(
            f"Final Score: {score}",
            large_font,
            WHITE,
            WIDTH // 2,
            320
        )

        draw_text(
            f"High Score: {high_score}",
            medium_font,
            YELLOW,
            WIDTH // 2,
            380
        )

        draw_button(
            restart_button,
            "RESTART",
            mouse_pos
        )

        draw_button(
            menu_button,
            "MAIN MENU",
            mouse_pos
        )

    # ========================================================
    # UPDATE SCREEN
    # ========================================================

    pygame.display.update()

    clock.tick(FPS)


# ============================================================
# EXIT
# ============================================================

pygame.quit()
sys.exit()