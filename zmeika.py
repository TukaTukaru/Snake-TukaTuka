from pygame.locals import *
import random
import math
import pygame


GAME_SIZE = [800,600]
WHITE = [255,255,255]
BLACK = [0,0,0]
RED = [255,0,0]
GREEN = [0,255,0]
YELLOW = [255,255,0]
BLUE = [0,0,255]
BLOCK_SIZE = [20,20]
UP = 1
DOWN = 3
RIGHT = 2
LEFT = 4
MAX_X = 760
MIN_X = 20
MAX_Y = 560
MIN_Y = 80
SNAKESTEP = 20


def render_screen(screen,score,snake_list,apple_place,bomb_place): 

    screen.fill(BLACK) #Clear the screen

    '''Draw the screen borders'''
    pygame.draw.line(screen,BLUE,(0,9),(799,9),20)
    pygame.draw.line(screen,BLUE,(0,590),(799,590),20)
    pygame.draw.line(screen,BLUE,(0,69),(799,69),20)
    pygame.draw.line(screen,BLUE,(9,0),(9,599),20)
    pygame.draw.line(screen,BLUE,(789,0),(789,599),20)
    
    '''Print the score'''
    font = pygame.font.SysFont("arial", 38)
    text_surface = font.render(f"Zmeika TukaTuka          Счет: {score}", True, BLUE)
    screen.blit(text_surface, (50,18))

    '''Output the array elements to the screen as rectangles (the snake)'''
    for element in snake_list:
        pygame.draw.rect(screen,YELLOW,Rect(element,BLOCK_SIZE))

    '''Draw the apple and bomb'''
    pygame.draw.rect(screen,GREEN,Rect(apple_place,BLOCK_SIZE))

    pygame.draw.rect(screen,RED,Rect(bomb_place,BLOCK_SIZE))

    '''Flip the screen to display everything we just changed'''
    pygame.display.flip()


def show_initial_screen(screen,clock):
    
    global show_start_screen
    if show_start_screen == True:
        show_start_screen = False

        s = [[180,120],[180,100],[160,100],[140,100],[120,100],[100,100],[100,120],[100,140],[100,160],[120,160],[140,160],[160,160],[180,160],[180,180],[180,200],[180,220],[160,220],[140,220],[120,220],[100,220],[100,200]]
        apple = [100,200]
        
        pygame.draw.rect(screen,GREEN,Rect(apple,BLOCK_SIZE))
        pygame.display.flip()
        clock.tick(8)
        
        for e in s:
            pygame.draw.rect(screen,BLUE,Rect(e,BLOCK_SIZE))
            pygame.display.flip()
            clock.tick(8)
            
        font = pygame.font.SysFont("arial", 64)
        text_surface = font.render("NAKE TukaTuka", True, BLUE)
        screen.blit(text_surface, (220,180))
        font = pygame.font.SysFont("arial", 24)
        text_surface = font.render("Двигай змейкой клавишами и ешь яблочки", True, BLUE)
        screen.blit(text_surface, (50,300))
        text_surface = font.render("Избегай стен, столкновений с собой и опасными бомбами!", True, BLUE)
        screen.blit(text_surface, (50,350))
        text_surface = font.render("Нажми s для начала новой игры - Нажми q для выхода из игры", True, BLUE)
        screen.blit(text_surface, (50,400))
        text_surface = font.render("Нажми p для паузы в игреи и r чтобы возобновить игру", True, BLUE)
        screen.blit(text_surface, (50,450))

        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    exit()
            
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[K_q]: 
                exit()
            if pressed_keys[K_s]: 
                break

            clock.tick(15)


def show_end_screen(screen,clock,score):
    
    screen.fill(BLACK)
    font = pygame.font.SysFont("arial", 48)
    text_surface = font.render("GAME OVER", True, BLUE)
    screen.blit(text_surface, (250,200))
    text_surface = font.render(f"Твой счет: {score}", True, BLUE)
    screen.blit(text_surface, (250,300))
    font = pygame.font.SysFont("arial", 24)
    text_surface = font.render("Нажми q чтобы выйти", True, BLUE)
    screen.blit(text_surface, (250,400))
    text_surface = font.render("Нажми n чтобы начать игру снова", True, BLUE)
    screen.blit(text_surface, (217,450))

    pygame.display.flip()
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()

        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_q]: 
            exit()
        if pressed_keys[K_n]: 
            break

        clock.tick(10)


def main():
    
    global show_start_screen
    show_start_screen = True

    while True:

        direction = RIGHT # 1=up,2=right,3=down,4=left
        snake_place = [300,400]
        snake_list = [[300,400],[280,400],[260,400]]
        score = 0
        apple_on_screen = 0
        apple_place = [0,0]
        bomb_on_screen = 0
        bomb_place = [0,0]
        new_direction = RIGHT
        snake_dead = False
        game_regulator = 1
        game_paused = 0
        grow_snake = 0  
        snake_grow_unit = 2 
        counter = 0
        
        pygame.init()
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode(GAME_SIZE)
        pygame.display.set_caption('Zmeika TukaTuka')
        screen.fill(BLACK)


        show_initial_screen(screen=screen,clock=clock)

                


        while not snake_dead:
            for event in pygame.event.get():
                if event.type == QUIT:
                    exit()
                    
            pressed_keys = pygame.key.get_pressed()
            
            if pressed_keys[K_LEFT]: 
                new_direction = LEFT
            if pressed_keys[K_RIGHT]: 
                new_direction = RIGHT
            if pressed_keys[K_UP]: 
                new_direction = UP
            if pressed_keys[K_DOWN]: 
                new_direction = DOWN
            if pressed_keys[K_q]: 
                snake_dead = True
            if pressed_keys[K_p]: 
                game_paused = 1
            
            while game_paused == 1:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        exit()
                pressed_keys = pygame.key.get_pressed()
                if pressed_keys[K_r]:
                    game_paused = 0 
                clock.tick(10)

            
            if game_regulator == 6:

                '''can't go back the reverse direction'''

                if new_direction == LEFT and not direction == RIGHT:
                    direction = new_direction

                elif new_direction == RIGHT and not direction == LEFT:
                    direction = new_direction

                elif new_direction == UP and not direction == DOWN:
                    direction = new_direction

                elif new_direction == DOWN and not direction == UP:
                    direction = new_direction
                    
                
                '''hit the wall and our snake dies'''  

                if direction == RIGHT:
                    snake_place[0] = snake_place[0] + SNAKESTEP
                    if snake_place[0] > MAX_X:
                        snake_dead = True
                    
                elif direction == LEFT:
                    snake_place[0] = snake_place[0] - SNAKESTEP
                    if snake_place[0] < MIN_X:
                        snake_dead = True
                        
                elif direction == UP:
                    snake_place[1] = snake_place[1] - SNAKESTEP
                    if snake_place[1] < MIN_Y:
                        snake_dead = True
                        
                elif direction == DOWN:
                    snake_place[1] = snake_place[1] + SNAKESTEP
                    if snake_place[1] > MAX_Y:
                        snake_dead = True

                        
                if len(snake_list) > 3 and snake_list.count(snake_place) > 0: 
                    snake_dead = True
                        
                '''generate an apple and bomb at a random position'''
                    
                if apple_on_screen == 0:
                    good = False
                    while good == False:
                        x = random.randrange(1,39)
                        y = random.randrange(5,29)
                        apple_place = [int(x*SNAKESTEP),int(y*SNAKESTEP)]
                        counter+=1
                        if snake_list.count(apple_place) == 0:
                            good = True
                    apple_on_screen = 1
               

                if bomb_on_screen == 0:
                    good = False
                    while good == False:
                        x = random.randrange(1,39)
                        y = random.randrange(5,29)
                        bomb_place = [int(x*SNAKESTEP),int(y*SNAKESTEP)]
                        if snake_list.count(bomb_place) == 0:
                            good = True
                        elif bomb_place == apple_place:
                            continue
                    bomb_on_screen = 1
                elif counter%3 == 0:
                        bomb_on_screen = 0
                        counter+=1
                
                '''add  position of snake head and tail '''

                snake_list.insert(0,list(snake_place))
                if snake_place[0] == apple_place[0] and snake_place[1] == apple_place[1]:
                    apple_on_screen = 0
                    score = score + 1
                    grow_snake = grow_snake + 1
                elif grow_snake > 0:
                    grow_snake = grow_snake + 1
                    if grow_snake == snake_grow_unit:
                        grow_snake = 0
                else:
                    snake_list.pop()
                
                if snake_place[0] == bomb_place[0] and snake_place[1] == bomb_place[1]:
                    snake_dead = True
                

                game_regulator = 0
                
            render_screen(screen=screen,score=score,snake_list=snake_list,apple_place=apple_place,bomb_place=bomb_place)
            
            game_regulator = game_regulator + 1
    
            clock.tick(25)
            
            
        if snake_dead == True:
            show_end_screen(screen=screen,clock=clock,score=score)
            


if __name__ == '__main__':
    main()



