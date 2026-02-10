import pygame
import sys
import random

pygame.init()

# =====================
# WINDOW
# =====================
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

# =====================
# GAME STATES
# =====================
START = "start"
PLAYING = "playing"
PAUSED = "paused"
GAME_OVER = "game_over"
game_state = START

# =====================
# LOAD ASSETS
# =====================
bg_img = pygame.transform.scale(
    pygame.image.load("assets/background-day.png"), (WIDTH, HEIGHT)
)

pipe_img = pygame.transform.scale(
    pygame.image.load("assets/pipe-green.png"), (60, 400)
)

bird_up = pygame.transform.scale(
    pygame.image.load("assets/bluebird-upflap.png"), (40, 30)
)
bird_mid = pygame.transform.scale(
    pygame.image.load("assets/bluebird-midflap.png"), (40, 30)
)
bird_down = pygame.transform.scale(
    pygame.image.load("assets/bluebird-downflap.png"), (40, 30)
)

gameover_img = pygame.transform.scale(
    pygame.image.load("assets/gameover.png"), (300, 80)
)


# =====================
# FONTS
# =====================
title_font = pygame.font.SysFont("arialblack", 48)
subtitle_font = pygame.font.SysFont("arial", 22)
ui_font = pygame.font.SysFont("arial", 28)
score_font = pygame.font.SysFont(None, 40)

# =====================
# BIRD
# =====================
bird_x = 100
bird_y = 300
bird_velocity = 0
gravity = 0.5
jump_strength = -8
bird_img = bird_mid

# =====================
# PIPES
# =====================
pipe_x = WIDTH
pipe_gap = 150
pipe_height = random.randint(200, 350)
pipe_speed = 3
pipe_width = 60

# =====================
# SCORE
# =====================
score = 0
high_score = 0
scored = False

# =====================
# UI ELEMENTS
# =====================
pause_rect = pygame.Rect(WIDTH - 40, 10, 30, 30)
restart_rect = pygame.Rect(100, 330, 200, 45)
quit_rect = pygame.Rect(100, 390, 200, 45)
BUTTON_COLOR = (40, 40, 40)
BUTTON_HOVER = (70, 70, 70)
TEXT_COLOR = (255, 255, 255)


# =====================
# RESET FUNCTION
# =====================
def reset_game():
    global bird_y, bird_velocity, pipe_x, pipe_height, score, scored
    bird_y = 300
    bird_velocity = 0
    pipe_x = WIDTH
    pipe_height = random.randint(200, 350)
    score = 0
    scored = False

# =====================
# MAIN LOOP
# =====================
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_state == START:
                    game_state = PLAYING
                    bird_velocity = jump_strength

                elif game_state == PLAYING:
                    bird_velocity = jump_strength

                elif game_state == GAME_OVER:
                    reset_game()
                    game_state = PLAYING

        if event.type == pygame.MOUSEBUTTONDOWN:
            if pause_rect.collidepoint(event.pos):
                if game_state == PLAYING:
                    game_state = PAUSED
                elif game_state == PAUSED:
                    game_state = PLAYING

            if game_state == GAME_OVER:
                if restart_rect.collidepoint(event.pos):
                    reset_game()
                    game_state = PLAYING
                if quit_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

    # =====================
    # DRAW BACKGROUND
    # =====================
    screen.blit(bg_img, (0, 0))

    # =====================
    # START SCREEN
    # =====================
    if game_state == START:
        title = title_font.render("FLAPPY BIRD", True, (255, 255, 255))
        subtitle = subtitle_font.render("Presented by HashLyfe", True, (255, 215, 0))
        hint = ui_font.render("Press SPACE to Start", True, (255, 255, 255))

        screen.blit(title, (WIDTH//2 - title.get_width()//2, 180))
        screen.blit(subtitle, (WIDTH//2 - subtitle.get_width()//2, 240))
        screen.blit(hint, (WIDTH//2 - hint.get_width()//2, 320))

    # =====================
    # PLAYING STATE
    # =====================
    if game_state == PLAYING:
        bird_velocity += gravity
        bird_y += bird_velocity

        pipe_x -= pipe_speed
        if pipe_x < -pipe_width:
            pipe_x = WIDTH
            pipe_height = random.randint(200, 350)
            scored = False

        if bird_velocity < -2:
            bird_img = bird_up
        elif bird_velocity > 2:
            bird_img = bird_down
        else:
            bird_img = bird_mid

        bird_rect = pygame.Rect(bird_x - 20, bird_y - 15, 40, 30)
        top_pipe_rect = pygame.Rect(pipe_x, pipe_height - 400, 60, 400)
        bottom_pipe_rect = pygame.Rect(pipe_x, pipe_height + pipe_gap, 60, 400)

        if bird_rect.colliderect(top_pipe_rect) or bird_rect.colliderect(bottom_pipe_rect):
            game_state = GAME_OVER
            high_score = max(high_score, score)


        if pipe_x + pipe_width < bird_x and not scored:
            score += 1
            scored = True

    # =====================
    # DRAW GAME ELEMENTS
    # =====================
    top_pipe_img = pygame.transform.flip(pipe_img, False, True)
    screen.blit(top_pipe_img, (pipe_x, pipe_height - 400))
    screen.blit(pipe_img, (pipe_x, pipe_height + pipe_gap))
    screen.blit(bird_img, (bird_x - 20, bird_y - 15))

    if game_state == PLAYING:
        score_text = score_font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (20, 20))

    # Draw pause button background
    pygame.draw.rect(screen, (30, 30, 30), pause_rect, border_radius=6)

    # Draw pause icon (two short vertical lines)
    line_width = 4
    line_height = 14
    line_gap = 4

    center_x = pause_rect.centerx
    center_y = pause_rect.centery

    left_line = pygame.Rect(
        center_x - line_gap - line_width,
        center_y - line_height // 2,
        line_width,
        line_height
    )

    right_line = pygame.Rect(
        center_x + line_gap,
        center_y - line_height // 2,
        line_width,
        line_height
    )

    pygame.draw.rect(screen, (255, 255, 255), left_line, border_radius=2)
    pygame.draw.rect(screen, (255, 255, 255), right_line, border_radius=2)

    # =====================
    # GAME OVER SCREEN
    # =====================
    if game_state == GAME_OVER:
        screen.blit(gameover_img, (WIDTH // 2 - gameover_img.get_width() // 2, 140))

        score_t = ui_font.render(f"Score: {score}", True, (255, 255, 255))
        high_t = ui_font.render(f"High Score: {high_score}", True, (255, 215, 0))

        screen.blit(score_t, (WIDTH // 2 - score_t.get_width() // 2, 230))
        screen.blit(high_t, (WIDTH // 2 - high_t.get_width() // 2, 265))

        mouse_pos = pygame.mouse.get_pos()


        def draw_button(rect, text):
            color = BUTTON_HOVER if rect.collidepoint(mouse_pos) else BUTTON_COLOR
            pygame.draw.rect(screen, color, rect, border_radius=8)
            txt = ui_font.render(text, True, TEXT_COLOR)
            screen.blit(
                txt,
                (rect.centerx - txt.get_width() // 2,
                 rect.centery - txt.get_height() // 2)
            )


        draw_button(restart_rect, "Restart")
        draw_button(quit_rect, "Quit")

    pygame.display.update()
    clock.tick(60)
