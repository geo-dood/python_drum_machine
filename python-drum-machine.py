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
huge_font = pygame.font.Font('freesansbold.ttf', 42)


fps = 60
timer = pygame.time.Clock()
beats = 8
instruments = 6
boxes = []
clicked = [[-1 for _ in range(beats)] for _ in range(instruments)]
active_list = [1 for _ in range(instruments)]
bpm = 180
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
        if clicked[i][active_beat] == 1 and active_list[i] == 1:
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


def draw_grid(clicks, beat, actives):
    left_box = pygame.draw.rect(screen, gray, [0, 0, 200, HEIGHT - 200], 5)
    bottom_box = pygame.draw.rect(screen, gray, [0, HEIGHT - 200, WIDTH, 200], 5)
    boxes = []
    colors = [gray, black, gray]
    snare_text = caption_font.render('Snare', True, colors[actives[0]])
    screen.blit(snare_text, (10, 30))
    kick_text = caption_font.render('Kick', True, colors[actives[1]])
    screen.blit(kick_text, (10, 130))
    knock_text = caption_font.render('Knock', True, colors[actives[2]])
    screen.blit(knock_text, (10, 230))
    closed_hat_text = caption_font.render('Closed Hat', True, colors[actives[3]])
    screen.blit(closed_hat_text, (10, 330))
    open_hat_text = caption_font.render('Open Hat', True, colors[actives[4]])
    screen.blit(open_hat_text, (10, 430))
    clap_text = caption_font.render('Clap', True, colors[actives[5]])
    screen.blit(clap_text, (10, 530))
    for i in range(instruments):
        pygame.draw.line(screen, gray, (0, (i * 100) + 100), (200, (i * 100) + 100), 3)
    for i in range(beats):
        for j in range(instruments):
            if clicks[j][i] == -1:
                color = gray
            else:
                if actives[j] == 1:
                    color = red
                else:
                    color = dark_gray

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
    boxes = draw_grid(clicked, active_beat, active_list)
    # lower menu buttons
    play_pause = pygame.draw.rect(screen, gray, [50, HEIGHT - 150, 200, 100], 0, 5)
    play_text = caption_font.render('Play/Pause:', True, white)
    screen.blit(play_text, (59, HEIGHT - 140))
    if playing:
        play_text2 = medium_font.render('Playing', True, green)
    else:
        play_text2 = medium_font.render('Paused', True, red)
    screen.blit(play_text2, (59, HEIGHT - 95))
    # bpm functionality
    bpm_rect = pygame.draw.rect(screen, gray, [280, HEIGHT - 150, 220, 100], 0, 5)
    bpm_text = medium_font.render('Beats Per Minute:', True, white)
    screen.blit(bpm_text, (285, HEIGHT - 140))
    bpm_text2 = caption_font.render(f'{bpm} bpm', True, white)
    screen.blit(bpm_text2, (320, HEIGHT - 100))
    bpm_add_rect = pygame.draw.rect(screen, gray, [505, HEIGHT - 147, 45, 45], 0, 5)
    bpm_sub_rect = pygame.draw.rect(screen, gray, [505, HEIGHT - 98, 45, 45], 0, 5)
    add_text = caption_font.render('+', True, white)
    sub_text = huge_font.render('-', True, white)
    screen.blit(add_text, (518, HEIGHT - 143))
    screen.blit(sub_text, (520, HEIGHT - 97))
    # Adding/Subtracting beat functionality
    beats_rect = pygame.draw.rect(screen, gray, [580, HEIGHT - 150, 220, 100], 0, 5)
    beats_text = medium_font.render('Total Beats:', True, white)
    screen.blit(beats_text, (618, HEIGHT - 140))
    beats_text2 = caption_font.render(f'{beats}', True, white)
    screen.blit(beats_text2, (685, HEIGHT - 100))
    beats_add_rect = pygame.draw.rect(screen, gray, [805, HEIGHT - 147, 45, 45], 0, 5)
    beats_sub_rect = pygame.draw.rect(screen, gray, [805, HEIGHT - 98, 45, 45], 0, 5)
    add_text2 = caption_font.render('+', True, white)
    sub_text2 = huge_font.render('-', True, white)
    screen.blit(add_text2, (818, HEIGHT - 143))
    screen.blit(sub_text2, (820, HEIGHT - 97))
    # Instrument/Track Control Buttons
    instrument_rects = []
    for i in range(instruments):
        rect = pygame.rect.Rect((0, i * 100), (200, 100))
        instrument_rects.append(rect)


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
            elif bpm_add_rect.collidepoint(event.pos):
                bpm += 5
            elif bpm_sub_rect.collidepoint(event.pos):
                bpm -= 5
            elif beats_add_rect.collidepoint(event.pos):
                beats += 1
                for i in range(len(clicked)):
                    clicked[i].append(-1)
            elif beats_sub_rect.collidepoint(event.pos):
                beats -= 1
                for i in range(len(clicked)):
                    clicked[i].pop(-1)
            for i in range(len(instrument_rects)):
                if instrument_rects[i].collidepoint(event.pos):
                    active_list[i] *= -1

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

# BAR:GJRAGLAVAR:GUVEGLBAR
