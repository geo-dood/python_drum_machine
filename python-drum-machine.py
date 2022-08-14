# Importing PyGame & the Mixer, initializing it.
from typing import Union

import pygame
from pygame import mixer
from pygame.rect import Rect, RectType

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
caption_font = pygame.font.Font('Fonts/VT323/VT323-Regular.ttf', 32)
medium_font = pygame.font.Font('Fonts/VT323/VT323-Regular.ttf', 24)
huge_font = pygame.font.Font('Fonts/VT323/VT323-Regular.ttf', 42)

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
save_menu = False
load_menu = False
saved_beats = []
file = open('saved_beats.txt', 'r')
for line in file:
    saved_beats.append(line)

# Loading in drum sounds
snare = mixer.Sound('Drum Sounds/snare.wav')
kick = mixer.Sound('Drum Sounds/kick.wav')
closed_hat = mixer.Sound('Drum Sounds/closed_hat.wav')
shaker = mixer.Sound('Drum Sounds/shaker.wav')
bell = mixer.Sound('Drum Sounds/bell.wav')
bass = mixer.Sound('Drum Sounds/bass.wav')
pygame.mixer.set_num_channels(instruments * 3)


def play_notes():
    for I in range(len(clicked)):
        if clicked[I][active_beat] == 1 and active_list[I] == 1:
            if I == 0:
                snare.play()
            if I == 1:
                kick.play()
            if I == 2:
                closed_hat.play()
            if I == 3:
                shaker.play()
            if I == 4:
                bell.play()
            if I == 5:
                bass.play()


# noinspection PyShadowingNames,PyUnusedLocal
def draw_grid(clicks, beat, actives):
    left_box = pygame.draw.rect(screen, gray, [0, 0, 200, HEIGHT - 200], 5)
    pygame.draw.rect(screen, gray, [0, HEIGHT - 200, WIDTH, 200], 5)
    boxes = []
    colors = [gray, black, gray]
    snare_text = caption_font.render('Snare', True, colors[actives[0]])
    screen.blit(snare_text, (10, 30))
    kick_text = caption_font.render('Kick', True, colors[actives[1]])
    screen.blit(kick_text, (10, 130))
    closed_hat_text = caption_font.render('Closed Hat', True, colors[actives[2]])
    screen.blit(closed_hat_text, (10, 230))
    shaker_text = caption_font.render('Shaker', True, colors[actives[3]])
    screen.blit(shaker_text, (10, 330))
    bell_text = caption_font.render('Bell', True, colors[actives[4]])
    screen.blit(bell_text, (10, 430))
    bass_text = caption_font.render('Bass', True, colors[actives[5]])
    screen.blit(bass_text, (10, 530))
    for I in range(instruments):
        pygame.draw.line(screen, gray, (0, (I * 100) + 100), (200, (I * 100) + 100), 3)
    for I in range(beats):
        for j in range(instruments):
            if clicks[j][I] == -1:
                color = gray
            else:
                if actives[j] == 1:
                    color = red
                else:
                    color = dark_gray

            rect = pygame.draw.rect(screen, color,
                                    [I * ((WIDTH - 200) // beats) + 205, (j * 100) + 5, ((WIDTH - 200) // beats) - 10,
                                     ((HEIGHT - 200) // instruments) - 10], 0, 3)
            pygame.draw.rect(screen, dark_gray,
                             [I * ((WIDTH - 200) // beats) + 200, (j * 100), ((WIDTH - 200) // beats),
                              ((HEIGHT - 200) // instruments)], 5, 5)
            pygame.draw.rect(screen, black,
                             [I * ((WIDTH - 200) // beats) + 200, (j * 100), ((WIDTH - 200) // beats),
                              ((HEIGHT - 200) // instruments)], 2, 5)
            boxes.append((rect, (I, j)))

        active = pygame.draw.rect(screen, bright_red,
                                  [beat * ((WIDTH - 200) // beats) + 200, 0, ((WIDTH - 200) // beats),
                                   instruments * 100], 5, 3, )
    return boxes


# noinspection DuplicatedCode
def draw_save_menu():
    # noinspection DuplicatedCode
    pygame.draw.rect(screen, black, [0, 0, WIDTH, HEIGHT])
    exit_btn = pygame.draw.rect(screen, black, [WIDTH - 200, HEIGHT - 100, 180, 90], 0, 5)
    exit_text = caption_font.render('Close', True, white)
    screen.blit(exit_text, (WIDTH - 160, HEIGHT - 70))
    return exit_btn


def draw_load_menu():
    # noinspection DuplicatedCode
    pygame.draw.rect(screen, black, [0, 0, WIDTH, HEIGHT])
    exit_btn: Union[Rect, RectType] = pygame.draw.rect(screen, black, [WIDTH - 200, HEIGHT - 100, 180, 90], 0, 5)
    exit_text = caption_font.render('Close', True, white)
    screen.blit(exit_text, (WIDTH - 160, HEIGHT - 70))
    return exit_btn


run = True
while run:
    timer.tick(fps)
    screen.fill(cream)
    boxes = draw_grid(clicked, active_beat, active_list)
    # lower menu buttons
    play_pause = pygame.draw.rect(screen, black, [50, HEIGHT - 150, 200, 100], 0, 5)
    play_text = caption_font.render('Play/Pause:', True, white)
    screen.blit(play_text, (80, HEIGHT - 140))
    if playing:
        play_text2 = medium_font.render('Playing', True, green)
    else:
        play_text2 = medium_font.render('Paused', True, red)
    screen.blit(play_text2, (113, HEIGHT - 105))
    # bpm functionality
    bpm_rect = pygame.draw.rect(screen, black, [280, HEIGHT - 150, 220, 100], 0, 5)
    bpm_text = medium_font.render('Beats Per Minute:', True, white)
    screen.blit(bpm_text, (307, HEIGHT - 136))
    bpm_text2 = caption_font.render(f'{bpm} bpm', True, white)
    screen.blit(bpm_text2, (345, HEIGHT - 108))
    bpm_add_rect = pygame.draw.rect(screen, black, [505, HEIGHT - 147, 45, 45], 0, 5)
    bpm_sub_rect = pygame.draw.rect(screen, black, [505, HEIGHT - 98, 45, 45], 0, 5)
    add_text = huge_font.render('+', True, white)
    sub_text = huge_font.render('-', True, white)
    screen.blit(add_text, (519, HEIGHT - 147))
    screen.blit(sub_text, (519, HEIGHT - 98))
    # Adding/Subtracting beat functionality
    beats_rect = pygame.draw.rect(screen, black, [580, HEIGHT - 150, 220, 100], 0, 5)
    beats_text = medium_font.render('Total Beats:', True, white)
    screen.blit(beats_text, (635, HEIGHT - 140))
    beats_text2 = caption_font.render(f'{beats}', True, white)
    screen.blit(beats_text2, (685, HEIGHT - 106))
    beats_add_rect = pygame.draw.rect(screen, black, [805, HEIGHT - 147, 45, 45], 0, 5)
    beats_sub_rect = pygame.draw.rect(screen, black, [805, HEIGHT - 98, 45, 45], 0, 5)
    add_text2 = huge_font.render('+', True, white)
    sub_text2 = huge_font.render('-', True, white)
    screen.blit(add_text2, (818, HEIGHT - 147))
    screen.blit(sub_text2, (819, HEIGHT - 98))
    # Instrument/Track Control Buttons
    instrument_rects = []
    for i in range(instruments):
        rect = pygame.rect.Rect((0, i * 100), (200, 100))
        instrument_rects.append(rect)
    # save and load buttons
    save_button = pygame.draw.rect(screen, black, [875, HEIGHT - 150, 200, 48], 0, 5)
    save_text = caption_font.render('Save Beat', True, white)
    screen.blit(save_text, (917, HEIGHT - 144))
    load_button = pygame.draw.rect(screen, black, [875, HEIGHT - 100, 200, 48], 0, 5)
    load_text = caption_font.render('Load Beat', True, white)
    screen.blit(load_text, (917, HEIGHT - 94))
    # Clear Grid
    clear_button = pygame.draw.rect(screen, black, [1100, HEIGHT - 150, 200, 100], 0, 5)
    clear_button_text = caption_font.render('Clear Grid', True, white)
    screen.blit(clear_button_text, (1132, HEIGHT - 117))
    # Drawing Menu Screens
    if save_menu:
        exit_button = draw_save_menu()
    if load_menu:
        exit_button = draw_load_menu()

    if beat_changed:
        play_notes()
        beat_changed = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and not save_menu and not load_menu:
            for i in range(len(boxes)):
                if boxes[i][0].collidepoint(event.pos):
                    coords = boxes[i][1]
                    clicked[coords[1]][coords[0]] *= -1
        if event.type == pygame.MOUSEBUTTONUP and not save_menu and not load_menu:
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
            elif clear_button.collidepoint(event.pos):
                clicked = [[-1 for _ in range(beats)] for _ in range(instruments)]
            elif save_button.collidepoint(event.pos):
                save_menu = True
            elif load_button.collidepoint(event.pos):
                load_menu = True
            for i in range(len(instrument_rects)):
                if instrument_rects[i].collidepoint(event.pos):
                    active_list[i] *= -1
        elif event.type == pygame.MOUSEBUTTONUP:
            # noinspection PyUnboundLocalVariable
            if exit_button.collidepoint(event.pos):
                save_menu = False
                load_menu = False
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
