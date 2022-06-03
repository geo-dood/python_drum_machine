# Simple Drum Machine Application
# Author: George Maysack-Schlueter

# ----------------------------------------------------------------------------------------------------------------------

# Importing PyGame & the Mixer, initializing it.
import pygame

# import mixer
pygame.init()

# ----------------------------------------------------------------------------------------------------------------------

# Variable Library:

# Setting up window dimensions - can be adjusted, but should be wider than it is tall.
WIDTH = 1400
HEIGHT = 800

# Defining colors we will be using.
black = (0, 0, 0)
white = (255, 255, 255)
gray = (128, 128, 128)
red = (208, 22, 22)
dark_gray = (88, 83, 83)
cream = (255, 253, 208)

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Simple Python Drum Machine by George Maysack')
caption_font = pygame.font.Font('freesansbold.ttf', 32)

fps = 60
timer = pygame.time.Clock()
beats = 8
instruments = 6
boxes = []
clicked = [[-1 for _ in range(beats)] for _ in range(instruments)]

def draw_grid(clicks):
    left_box = pygame.draw.rect(screen, gray, [0, 0, 200, HEIGHT - 200], 5)
    bottom_box = pygame.draw.rect(screen, gray, [0, HEIGHT - 200, WIDTH, 200], 5)
    boxes = []
    colors = [gray, white, gray]
    hi_hat_text = caption_font.render('Hi-Hat', True, black)
    screen.blit(hi_hat_text, (30, 30))
    snare_text = caption_font.render('Snare', True, black)
    screen.blit(snare_text, (30, 130))
    kick_text = caption_font.render('Kick', True, black)
    screen.blit(kick_text, (30, 230))
    crash_text = caption_font.render('Crash', True, black)
    screen.blit(crash_text, (30, 330))
    clap_text = caption_font.render('Clap', True, black)
    screen.blit(clap_text, (30, 430))
    tom_text = caption_font.render('Tom', True, black)
    screen.blit(tom_text, (30, 530))
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
    return boxes


run = True
while run:
    timer.tick(fps)
    screen.fill(cream)
    boxes = draw_grid(clicked)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(len(boxes)):
                if boxes[i][0].collidepoint(event.pos):
                    coords = boxes[i][1]
                    clicked[coords[1]][coords[0]] *= -1

    pygame.display.flip()
pygame.quit()

# REACHED 37:15 IN TUTORIAL!!!
