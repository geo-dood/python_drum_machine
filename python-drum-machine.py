# Importing PyGame & the Mixer, initializing it.
import pygame
from pygame import mixer

pygame.init()

WIDTH = 1400
HEIGHT = 800

black = (0, 0, 0)
white = (255, 255, 255)
gray = (128, 128, 128)
red = (220, 20, 60)
dark_gray = (90, 90, 90)
cream = (255, 253, 208)
bright_red = (255, 0, 0)
green = (0, 255, 127)

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Simple Python Drum Machine by George Maysack')
caption_font = pygame.font.Font('freesansbold.ttf', 32)
medium_font = pygame.font.Font('freesansbold.ttf', 24)

fps = 60
timer = pygame.time.Clock()
beats = 8
instruments = 6
boxes = []
clicked = [[-1 for _ in range(beats)] for _ in range(instruments)]
bpm = 240
playing = True
active_length = 0
active_beat = 1
beat_changed = True

# Loading in drum sounds
snare = mixer.Sound('Drum Sounds\snare.wav')
kick = mixer.Sound('Drum Sounds\kick.wav')
knock = mixer.Sound('Drum Sounds\knock.wav')
closed_hat = mixer.Sound('Drum Sounds\closed_hat.wav')
open_hat = mixer.Sound('Drum Sounds\open_hat.wav')
clap = mixer.Sound('Drum Sounds\clap.wav')
pygame.mixer.set_num_channels(instruments * 3)


def play_notes():
    for i in range(len(clicked)):
        if clicked[i][active_beat] == 1:
            if i == 0:
                snare.play()
            if i == 1:
                kick.play()
            if i == 2:
                knock.play()
            if i == 3:
                closed_hat.play()
            if i == 4:
                open_hat.play()
            if i == 5:
                clap.play()


def draw_grid(clicks, beat):
    left_box = pygame.draw.rect(screen, gray, [0, 0, 200, HEIGHT - 200], 5)
    bottom_box = pygame.draw.rect(screen, gray, [0, HEIGHT - 200, WIDTH, 200], 5)
    boxes = []
    colors = [gray, white, gray]
    snare_text = caption_font.render('Snare', True, black)
    screen.blit(snare_text, (10, 30))
    kick_text = caption_font.render('Kick', True, black)
    screen.blit(kick_text, (10, 130))
    knock_text = caption_font.render('Knock', True, black)
    screen.blit(knock_text, (10, 230))
    closed_hat_text = caption_font.render('Closed Hat', True, black)
    screen.blit(closed_hat_text, (10, 330))
    open_hat_text = caption_font.render('Open Hat', True, black)
    screen.blit(open_hat_text, (10, 430))
    clap_text = caption_font.render('Clap', True, black)
    screen.blit(clap_text, (10, 530))
    for i in range(instruments):
        pygame.draw.line(screen, gray, (0, (i * 100) + 100), (200, (i * 100) + 100), 3)

    for i in range(beats):
        for j in range(instruments):
            if clicks[j][i] == -1:
                color = gray
            else:
                color = red
            rect = pygame.draw.rect(screen, color,
                                    [i * ((WIDTH - 200) // beats) + 205, (j * 100) + 5, ((WIDTH - 200) // beats) - 10,
                                     ((HEIGHT - 200) // instruments) - 10], 0, 3)
            pygame.draw.rect(screen, dark_gray,
                             [i * ((WIDTH - 200) // beats) + 200, (j * 100), ((WIDTH - 200) // beats),
                              ((HEIGHT - 200) // instruments)], 5, 5)
            pygame.draw.rect(screen, black,
                             [i * ((WIDTH - 200) // beats) + 200, (j * 100), ((WIDTH - 200) // beats),
                              ((HEIGHT - 200) // instruments)], 2, 5)
            boxes.append((rect, (i, j)))

        active = pygame.draw.rect(screen, bright_red, [beat * ((WIDTH - 200)//beats) + 200, 0, ((WIDTH - 200)//beats), instruments * 100], 5, 3,)
    return boxes


run = True
while run:
    timer.tick(fps)
    screen.fill(cream)
    boxes = draw_grid(clicked, active_beat)
    # lower menu buttons
    play_pause = pygame.draw.rect(screen, gray, [50, HEIGHT - 150, 200, 100], 0, 5)
    play_text = caption_font.render('Play/Pause', True, white)
    screen.blit(play_text, (70, HEIGHT - 130))
    if playing:
        play_text2 = medium_font.render('Playing', True, green)
    else:
        play_text2 = medium_font.render('Paused', True, red)
    screen.blit(play_text2, (70, HEIGHT - 95))

    if beat_changed:
        play_notes()
        beat_changed = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(len(boxes)):
                if boxes[i][0].collidepoint(event.pos):
                    coords = boxes[i][1]
                    clicked[coords[1]][coords[0]] *= -1
        if event.type == pygame.MOUSEBUTTONUP:
            if play_pause.collidepoint(event.pos):
                if playing:
                    playing = False
                elif not playing:
                    playing = True

    beat_length = 3600 // bpm

    if playing:
        if active_length < beat_length:
            active_length += 1
        else:
            active_length = 0
            if active_beat < beats - 1:
                active_beat += 1
                beat_changed = True
            else:
                active_beat = 0
                beat_changed = True

    pygame.display.flip()
pygame.quit()

# REACHED 55:00
