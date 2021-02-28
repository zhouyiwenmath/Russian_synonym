#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  7 08:15:35 2021

@author: yiwen
"""


import pygame
import time
import numpy as np
import random


def find_index(x, y):
    row = y // (config['font_size'] + config['margin'])
    col = x // (config['font_size'] * 10 + config['margin'])
    return (row, col)


def isin_margin(x, y):
    row = y % (config['font_size'] + config['margin'])
    col = x % (config['font_size'] * 10 + config['margin'])
    return (row < config['margin']) or (col < config['margin'])

# read words synonym from file
with open(r'synonym.txt') as f:
    content = f.readlines()

words = dict()
count = dict()

for line in content:
    tp = line[:line.find('\n')].split('\t')
    words[tp[0]] = tp[1:]
    count[tp[0]] = len(tp[1:])


# read configuration from file
with open(r'config.txt') as f:
    content = f.readlines()

config = dict()

for line in content:
    tp = line[:line.find('\n')].split(':')
    config[tp[0]] = int(tp[1])
config['screen_size'] = (config['font_size'] + config['margin']) * config['pairs_of_words'] + config['margin']


# Displays
start_time = time.time()

pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont(pygame.font.get_default_font(), config['font_size'])

print(pygame.font.get_default_font())

pygame.display.set_caption('русские_синонимы ')
screen = pygame.display.set_mode((config['font_size'] * 20 + 3 * config['margin'], config['screen_size']))

selected_pword = np.random.permutation(len(words))[:config['pairs_of_words']]

words_left = []
words_right = []
for i in selected_pword:
    words_left.append(random.choice(words["{}".format(i)]))
    words["{}".format(i)].remove(words_left[-1])
    words_right.append(random.choice(words["{}".format(i)]))
    
index_left = np.random.permutation(config['pairs_of_words'])
index_right = np.random.permutation(config['pairs_of_words'])

running = True
last_row, last_col = (-1, -1)
row, col = (-1, -1)
paired = False

while running:
    current_events = pygame.event.get()
    for e in current_events:
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                running = False
        if e.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            
            if paired:
                if last_col == 0:
                    words_left[index_left[last_row]] = ""
                    words_right[index_right[row]] = ""
                elif last_col == 1:
                    words_right[index_right[last_row]] = ""
                    words_left[index_left[row]] = ""
                paired = False
                last_row = -1
                last_col = -1
            if not isin_margin(mouse_x, mouse_y):
                row, col = find_index(mouse_x, mouse_y)
                if last_row == -1 and last_col == -1:
                    last_row = row
                    last_col = col
                elif row == last_row and col == last_col:
                    last_row = -1
                    last_col = -1
                elif last_col == col:
                    last_row = row
                elif last_col == 0:
                    if index_left[last_row] == index_right[row]:
                        paired = True
                    else:
                        last_row = -1
                        last_col = -1
                elif last_col == 1:
                    if index_right[last_row] == index_left[row]:
                        paired = True
                    else:
                        last_row = -1
                        last_col = -1
            
    screen.fill((0, 0, 0))
                    
    if paired:   
        for i in range(config['pairs_of_words']):
            if (last_col == 0 and i == last_row) or (last_col == 1 and i == row):
                textsurface_1 = myfont.render(words_left[index_left[i]], False, (255, 153, 204))
            else:
                textsurface_1 = myfont.render(words_left[index_left[i]], False, (255, 255, 255))
            if (last_col == 1 and i == last_row) or (last_col == 0 and i == row):
                textsurface_2 = myfont.render(words_right[index_right[i]], False, (255, 153, 204))
            else:
                textsurface_2 = myfont.render(words_right[index_right[i]], False, (255, 255, 255))
            screen.blit(textsurface_1, (config['margin'], config['margin'] + i * (config['font_size'] + config['margin'])))
            screen.blit(textsurface_2, (config['margin'] + 10 * (config['font_size']), config['margin'] + i * (config['font_size'] + config['margin'])))
            
    else:    
        for i in range(config['pairs_of_words']):
            if last_col == 0 and i == last_row:
                textsurface_1 = myfont.render(words_left[index_left[i]], False, (102, 204, 255))
            else:
                textsurface_1 = myfont.render(words_left[index_left[i]], False, (255, 255, 255))
            if last_col == 1 and i == last_row:
                textsurface_2 = myfont.render(words_right[index_right[i]], False, (102, 204, 255))
            else:
                textsurface_2 = myfont.render(words_right[index_right[i]], False, (255, 255, 255))
            screen.blit(textsurface_1, (config['margin'], config['margin'] + i * (config['font_size'] + config['margin'])))
            screen.blit(textsurface_2, (config['margin'] + 10 * (config['font_size']), config['margin'] + i * (config['font_size'] + config['margin'])))
        
    pygame.display.flip()
            
print(time.time() - start_time)
