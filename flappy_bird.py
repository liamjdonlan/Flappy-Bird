import pygame
import sys
import random


def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 400))
    screen.blit(floor_surface, (floor_x_pos + 288, 400))


def create_pipe():
    random_pipe_pos = random.choice(pipe_locations)
    bottom_pipe = pipe_surface.get_rect(midtop=(340, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom=(340, random_pipe_pos - 150))
    return bottom_pipe, top_pipe


def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= PIPE_SPEED
    return pipes


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 512:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)


def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            return False

        if bird_rect.top <= -100 or bird_rect.bottom >= 400:
            death_sound.play()
            return False

    return True


def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 5, 1)
    return new_bird


def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center=(50, bird_rect.centery))
    return new_bird, new_bird_rect


def score_display(game_state):
    if game_state == "main_game":
        score_surface = game_front.render(
            f"Score: {int(score)}", True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(144, 50))
        screen.blit(score_surface, score_rect)
    elif game_state == "game_over":
        score_surface = game_front.render(
            f"Score: {int(score)}", True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(144, 50))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_front.render(
            f"High Score: {int(high_score)}", True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(144, 75))
        screen.blit(high_score_surface, high_score_rect)


def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score


pygame.init()

screen = pygame.display.set_mode((288, 512))
clock = pygame.time.Clock()
game_front = pygame.font.Font("04B_19__.TTF", 20)

# Game constants
GRAVITY = 0.1
FLAP_HEIGHT = 4
FLOOR_SPEED = 2
PIPE_SPEED = 1.5

# Game variables
score = 0
high_score = 0
bird_movement = 0
game_active = True

bg_surface = pygame.image.load("sprites/background-day.png").convert()

floor_surface = pygame.image.load("sprites/base.png").convert()
floor_x_pos = 0

bird_downflap = pygame.image.load(
    "sprites/yellowbird-downflap.png").convert_alpha()
bird_midflap = pygame.image.load(
    "sprites/yellowbird-midflap.png").convert_alpha()
bird_upflap = pygame.image.load(
    "sprites/yellowbird-upflap.png").convert_alpha()
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 2
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center=(50, 256))

BIRD_FLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRD_FLAP, 200)

# bird_surface = pygame.image.load("sprites/yellowbird-midflap.png").convert_alpha()
# bird_rect = bird_surface.get_rect(center=(50, 256))

pipe_surface = pygame.image.load("sprites/pipe-green.png").convert()
pipe_list = []
SPAWN_PIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWN_PIPE, 1200)
pipe_locations = [225, 290, 350]

game_over_surface = pygame.image.load("sprites/message.png").convert_alpha()
game_over_rect = game_over_surface.get_rect(center=(144, 256))

flap_sound = pygame.mixer.Sound("audio/wing.ogg")
death_sound = pygame.mixer.Sound("audio/hit.ogg")
score_sound = pygame.mixer.Sound("audio/point.ogg")

score_countdown = 100

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active == True:
                bird_movement = 0
                bird_movement -= FLAP_HEIGHT
                flap_sound.play()

            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (50, 246)
                bird_movement = -FLAP_HEIGHT
                score = 0

        if event.type == SPAWN_PIPE:
            pipe_list.extend(create_pipe())

        if event.type == BIRD_FLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0

            bird_surface, bird_rect = bird_animation()

    screen.blit(bg_surface, (0, 0))

    if game_active:
        # Bird
        bird_movement += GRAVITY
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)
        game_active = check_collision(pipe_list)

        # Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        # Score
        score += 0.01
        score_display("main_game")
        score_countdown -= 1
        if score_countdown <= 0:
            score_sound.play()
            score_countdown = 100
    else:
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_display("game_over")

    # Floor
    floor_x_pos -= FLOOR_SPEED
    draw_floor()
    if floor_x_pos <= -288:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(120)
