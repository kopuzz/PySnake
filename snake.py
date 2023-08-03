"""
*********************************************************************************
*    Copyright (c) 2023 TpoMad                                                  *
*    All rights reserved.                                                       *
*                                                                               *
*    This file is part of python-snake.py                                       *
*                                                                               *
*    python-snake is free software: you can redistribute it and/or modify       *
*    it under the terms of the GNU General Public License as published by       *
*    the Free Software Foundation, version 3 of the License.                    *
*                                                                               *
*    python-snake is distributed in the hope that it will be useful,            *
*    but WITHOUT ANY WARRANTY; without even the implied warranty of             *
*    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the               *
*    GNU General Public License for more details.                               *
*                                                                               *
*    You should have received a copy of the GNU General Public license          *
*    along with python-snake. If not, see <http://www.gnu.org/licenses/>.       *
*                                                                               *
*    You are required to maintain this copyright notice in all copies or        *
*    substantial portions of the software.                                      *
*********************************************************************************

++++++++++++++++++++
+       SNAKE      +
++++++++++++++++++++
|                  | < play field
|                  |
|                  |
|                  |
|__________________|
|__________________| < ui

"""


import sys
import time
import pygame
from pygame.locals import *
from random import randrange as rand

from pathlib import Path


def rect_collide(x1, y1, x2, y2, cellSize=10):
    return \
        x1 + cellSize > x2 and \
        x1 < x2 + cellSize and \
        y1 + cellSize > y2 and \
        y1 < y2 + cellSize


def snake():
    pygame.init()
    pygame.freetype.init()
    pygame.display.set_caption("Snake")
    FPS = 30.0
    WIN_WIDTH, WIN_HEIGHT = 420, 420
    UI_WIDTH, UI_HEIGHT = WIN_WIDTH, 50
    PLAY_WIDTH, PLAY_HEIGHT = WIN_WIDTH, WIN_HEIGHT - UI_HEIGHT
    CELL_SIZE = PLAY_WIDTH / 35 # 15 || 35 for smaller snake and bigger play area
    CELL_PADDING = 0
    UI_FONT = pygame.font.Font(Path("res", "font", "Fira_Code_Retina_450.ttf"), 16)
    UIT_SCORE = UI_FONT.render("Score:", True, (55, 155, 50))
    UIT_SPEED = UI_FONT.render("Speed:", True, (55, 155, 50))
    UIT_SPEED_MAX = UI_FONT.render("(MAX)", True, (155, 55, 50))
    UIT_SPACE_LEFT = UI_FONT.render("Space Left:", True, (55, 155, 50))
    UI_BG = Rect(0, PLAY_HEIGHT, UI_WIDTH, UI_HEIGHT)
    # directional velocities
    UP, DOWN = (0, -CELL_SIZE), (0, CELL_SIZE)
    LEFT, RIGHT = (-CELL_SIZE, 0), (CELL_SIZE, 0)

    MOVE_TIMER_MAX = 80.0
    move_timer_offset = 20.0 # lower is slower
    move_timer = 0.0

    food_coords = []
    for x in range(0, int(PLAY_WIDTH), int(CELL_SIZE)):
        for y in range(0, int(PLAY_HEIGHT), int(CELL_SIZE)):
            food_coords.append((x, y))

    coord_idx = rand(0, len(food_coords) - 1)
    food_xy = food_coords.pop(coord_idx)
    food_rect = Rect(food_xy[0], food_xy[1], CELL_SIZE, CELL_SIZE)
    food_surf = pygame.image.load(Path("res", "imgs", "cherry-16x16.png"))

    snake_rects = []
    snake_rects.append(Rect(
        CELL_SIZE*rand(2, 5),
        CELL_SIZE*rand(2, 5),
        CELL_SIZE, CELL_SIZE)
    )

    head_direction = (0, CELL_SIZE)
    snake_len = 1
    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == K_LEFT and head_direction != RIGHT:
                    head_direction = LEFT
                if event.key == K_RIGHT and head_direction != LEFT:
                    head_direction = RIGHT
                if event.key == K_UP and head_direction != DOWN:
                    head_direction = UP
                if event.key == K_DOWN and head_direction != UP:
                    head_direction = DOWN

        # check head collision with food
        if rect_collide(
            snake_rects[0].x, snake_rects[0].y,
            food_rect.x, food_rect.y, CELL_SIZE):

            snake_rects.append(Rect(
                snake_rects[snake_len-1].x,
                snake_rects[snake_len-1].y,
                CELL_SIZE, CELL_SIZE)
            )
            snake_len = len(snake_rects)

            # slightly increase move speed
            if snake_len % 2 == 0:
                move_timer_offset += .44

            # TODO: play sound ..

            # spawn food
            coord_idx = rand(0, len(food_coords) - 1)
            food_xy = food_coords.pop(coord_idx)
            food_rect = Rect(food_xy[0], food_xy[1], CELL_SIZE, CELL_SIZE)

        # check head collision with body   
        for i in range(1, snake_len - 1):
            if rect_collide(
                snake_rects[0].x, snake_rects[0].y,
                snake_rects[i].x, snake_rects[i].y, CELL_SIZE):

                running = False

        # check head collision with left and right screen sides
        if snake_rects[0].x < 0:
            snake_rects[0].x = PLAY_WIDTH - CELL_SIZE
        elif snake_rects[0].x > PLAY_WIDTH - CELL_SIZE:
            snake_rects[0].x = 0

        # check head collision with top and bottom screen sides
        if snake_rects[0].y < 0:
            snake_rects[0].y = PLAY_HEIGHT - CELL_SIZE
        elif snake_rects[0].y > PLAY_HEIGHT - CELL_SIZE:
            snake_rects[0].y = 0

        # shift body positions then move the head
        if move_timer >= MOVE_TIMER_MAX:
            for i in range(snake_len - 1 , 0, -1):
                snake_rects[i].x = snake_rects[i - 1].x
                snake_rects[i].y = snake_rects[i - 1].y
        
            snake_rects[0].x += head_direction[0]
            snake_rects[0].y += head_direction[1]
            move_timer = 0.0
        
        screen.fill((0, 0, 0))

        screen.blit(food_surf, food_xy)
        
        for i, snake_rect in enumerate(snake_rects):
            # body
            if i % 2 != 0 and i % 3 != 0:
                pygame.draw.rect(screen, (100, 120, 30), snake_rect, 0, 10)
            elif i % 2 == 0:
                pygame.draw.rect(screen, (100, 170, 30), snake_rect, 0, 10)
            elif i % 3 == 0: # every 4th
                pygame.draw.rect(screen, (100, 170, 80), snake_rect, 0, 10)
        
            # head
            pygame.draw.rect(screen, (150, 150, 150), snake_rect, 1, 6)
            
            # tail
            if i == snake_len and i != 0:
                pygame.draw.rect(screen, (150, 150, 150), snake_rect, 4, 34)
            if i == snake_len - 1 and i != 0:    
                pygame.draw.rect(screen, (150, 150, 150), snake_rect, 3, 10)
            if i == snake_len - 2 and i != 0:  
                pygame.draw.rect(screen, (150, 150, 150), snake_rect, 2, 6)

        # render dynamic text and draw ui
        pygame.draw.rect(screen, (5, 10, 5), UI_BG)
        pygame.draw.aaline(
            screen, (55, 155, 50),
            (0, WIN_HEIGHT - UI_HEIGHT),
            (WIN_WIDTH, WIN_HEIGHT - UI_HEIGHT)
        )

        UIT_SCORE_VAL = UI_FONT.render(f"{snake_len}", True, (100, 150, 100))
        screen.blit(UIT_SCORE, (5, PLAY_HEIGHT + 5))
        screen.blit(UIT_SCORE_VAL, (65, PLAY_HEIGHT + 5))
        
        scaled_speed = move_timer_offset - 19.0
        UIT_SPEED_VAL = UI_FONT.render(f"{scaled_speed:.2f}", True, (100, 150, 100))
        screen.blit(UIT_SPEED, (5, PLAY_HEIGHT + 25))
        screen.blit(UIT_SPEED_VAL, (65, PLAY_HEIGHT + 25))
        if move_timer_offset >= MOVE_TIMER_MAX:
            screen.blit(UIT_SPEED_MAX, (115, PLAY_HEIGHT + 25))
        
        UIT_SPACE_LEFT_VAL = UI_FONT.render(f"{len(food_coords)}", True, (100, 150, 100))
        screen.blit(UIT_SPACE_LEFT, (115, PLAY_HEIGHT + 5))
        screen.blit(UIT_SPACE_LEFT_VAL, (225, PLAY_HEIGHT + 5))
        
        pygame.display.flip()
        move_timer += move_timer_offset
        time.sleep(FPS / 1000.0)



if __name__ == '__main__':
    snake()
