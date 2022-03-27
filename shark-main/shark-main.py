
from errors import *
from done import *
import time
import random
import subprocess
import os
import tkinter as tk
import webbrowser


documentation = '''
===============================================================================


A copy of Make code arcade's shark tutorial, with some extra features

CONTROLS:
    right: right
    up: up
    down: down
    left: left
    f: toggle freeze
===============================================================================

'''



        


        


try:
    import pygame
    from pygame.locals import *
# homework Friday March 11 2022
# SAIL program
except ModuleNotFoundError:
    
    def install(module):
        subprocess.call([sys.executable, "-m", "pip", "install", module])
    print('It appears you do not have pygame. We can install this for you.')
    inpt = input('Proceed with default install? (y/n)')
    if inpt == 'y' or inpt == 'yes' or 'yes' in inpt:
        install('pygame')

    else:
        print('Ending program...')
        raise NOINSTALL_ERROR


def freeze_draw():
    freeze = pygame.image.load(os.path.join('images', 'snowflake.png'))
    freeze = pygame.transform.scale(freeze, (freeze.get_width() * 1 / 8, freeze.get_height() * 1 / 8)) 
    WIN.blit(freeze, (200, 0))
pygame.font.init()  

WIN = pygame.display.set_mode((800, 300))


FPS = 60
VEL = 5



time_f = pygame.font.Font('DS-DIGI.TTF', 40)
font = pygame.font.SysFont('sans', 40)





sharks = [pygame.image.load(os.path.join('images', f'Frame{i}.png')) for i in range(1, 6)]
msharks = [pygame.image.load(os.path.join(os.path.join('images', f'mFrame{i}.png'))) for i in range(1, 9)]
numstates = 5
fsh = pygame.image.load(os.path.join(os.path.join('images', 'fish.png')))
ocean = pygame.image.load(os.path.join('images', 'ocean.png'))
instructions = pygame.image.load(os.path.join('images', 'instructions.png'))
pygame.display.set_icon(sharks[0])
seaweed = pygame.image.load(os.path.join('images', 'seaweed.png'))
pygame.display.set_caption('sharks')
ocean = pygame.transform.scale(ocean, (160 * 2.5, 120 * 2.5))

sha = sharks[0].get_rect()
sha.y = 150
sha.x = 50
munching = False
frozen = False
complete_frozen = False

def get_shark(munching, state):
    if munching:
        return msharks[state]
    return sharks[state]
def is_future_collide(sha, fish):
    sx = sha.x
    sy = sha.y
    for i in fish:
        if (sx - i.x) + (sy - i.y) <= 500:
            munching = True
            state = 0
def handle_collide(sha, fish):
    global state
    global munching
    num = 0
    for i in fish.copy():
        if sha.colliderect(i):
            fish.remove(i)
            
            num += 1
            munching = True
    return num, fish 
def move_fish(fish):

    for i in fish:
        i.x -= 3
def handle_ship(sha, keys, state):
    global complete_frozen
    facing = ' '
    if munching:
        shark = msharks[state]

    else:
        shark = sharks[state]
    if (keys[pygame.K_UP] or keys[pygame.K_w]) and sha.y - VEL > 0:
        facing += ' up'
        sha.y -= VEL
    if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and sha.y + VEL + shark.get_height() < 300:
        facing += ' down'
        sha.y += VEL
    if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and sha.x - VEL > 0:
        facing += ' left'
        sha.x -= VEL
    if keys[pygame.K_RIGHT] and sha.x + VEL + shark.get_width() < 400:
        facing += ' right'
        sha.x += VEL

    
    
  
    
    
    return facing[1:]
def draw_weed(weed):
    WIN.blit(seaweed, (weed, 300 - seaweed.get_height()))

def draw_fish(i):
    WIN.blit(fsh, (i.x, i.y))
    
def draw_window(sha, fishies = [], facing = 'right', weed = [], state = 0):
            
    WIN.fill((0, 0, 150))
    WIN.blit(ocean, (0, 0))
    WIN.blit(pygame.transform.scale(instructions, (400, 300)), (400, 0))
    if facing == ' right' or facing == '':
        if not munching:
            WIN.blit(sharks[state], (sha.x, sha.y))

        else:
            WIN.blit(msharks[state], (sha.x, sha.y))
    elif facing == ' up':
        if not munching:
            image = pygame.transform.rotate(sharks[state], 90)
        else:
            image = pygame.transform.rotate(msharks[state], 90)
        WIN.blit(image, (sha.x, sha.y))

    elif facing == ' down':
        if not munching:
            image = pygame.transform.rotate(pygame.transform.flip(sharks[state], False, True), 270)
        else:
            image = pygame.transform.rotate(pygame.transform.flip(msharks[state], False, True), 270)
        WIN.blit(image, (sha.x, sha.y))
    elif facing == ' up right':
        if not munching:
            image = pygame.transform.rotate(sharks[state], 45)
        else:
            image = pygame.transform.rotate(msharks[state], 45)

        WIN.blit(image, (sha.x, sha.y))
    elif facing == ' down right':
        if not munching:
            image = pygame.transform.rotate(sharks[state], 315)
        else:
            image = pygame.transform.rotate(msharks[state], 315)

        WIN.blit(image, (sha.x, sha.y))


    
    elif facing == ' down left':
        if not munching:
            
            image = pygame.transform.rotate(pygame.transform.flip(sharks[state], True, False), 45)
        else:
                        image = pygame.transform.rotate(pygame.transform.flip(msharks[state], True, False), 45)
        WIN.blit(image, (sha.x, sha.y))

    elif facing == ' up left':
        if not munching:
            image = pygame.transform.rotate(pygame.transform.flip(sharks[state], True, False), 315)
        else:
            image = pygame.transform.rotate(pygame.transform.flip(msharks[state], True, False), 315)

            
        WIN.blit(image, (sha.x, sha.y))
    else:
        if not munching:
            shark2 = pygame.transform.flip(sharks[state], True, False)

        else:
            shark2 = pygame.transform.flip(msharks[state], True, False)
        WIN.blit(shark2, (sha.x, sha.y))
    
    for i in weed:

        draw_weed(i)



    for i in fishies:
        draw_fish(i)



def show_done_screen(score):
    WIN.fill((0, 6, 255))
    WIN.blit(pygame.transform.scale(pygame.image.load(os.path.join('images', 'icon.png')), (100, 100)), (0, 0))
    TEXT_FONT = pygame.font.SysFont('Times New Roman', 45)
    
    txt = TEXT_FONT.render(f'Time\'s up! Score: {score}', 15, (255, 255, 255))
    center = centerx, centery  = 400 - txt.get_width() / 2, 150 - text.get_height() / 2
    WIN.blit(txt, center)
    pygame.display.update()
    run = True
    
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise Done
        
clock = pygame.time.Clock()
running = True
currentFrame = 0

oldw = weed = [random.randint(0, 400) for i in range(10)]
f = []


state = -1

time = 0
test = False
score = 0
secs = 30
start = 3000
iconstate = 0 
while running:
    clock.tick(FPS)
    time += 1
    
    
    
    
    shax = sha.x
    shay = sha.y
    
    if not munching:
        sha = sharks[state].get_rect()

    else:
        sha = msharks[state].get_rect()
    if not test:
            sha.x = shax
            sha.y = shay
    if True:

    
        if time % 5 == 0:
            
                
                state += 1
                if not munching:
                    
                    state %= 5
                else:
                    if state == 8:
                        munching = False
                        state %= 8
        if time % 70 == 0 and not (frozen or complete_frozen):
            rand = random.randint(20, 280)
            f.append(fsh.get_rect())
            f[-1].x = 390
            f[-1].y = random.randint(20, 280)
        f.append(pygame.Rect(random.randint(10, 290), 400, 12000, 12000))
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False
                raise Done
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    complete_frozen = not complete_frozen

        

        keys = pygame.key.get_pressed()
        s, f = handle_collide(sha, f)
        score += s
        is_future_collide(sha, f)
        if not (frozen or complete_frozen):
            
            facing = handle_ship(sha, keys, state)
        draw_window(sha, f, facing, weed, state)



        if not (frozen or complete_frozen):
            move_fish(f)
        if frozen or complete_frozen:
            freeze_draw()
            
        
        text = font.render(f'{score}', 1, (255, 255, 255))
        WIN.blit(text, (0, 0))
        
        timer = str(start // 100)

                 

        
        
        
        text2 = time_f.render(timer, 23, (255, 255, 255))
        WIN.blit(text2, (400 - text2.get_width(), 0))
        if not (frozen or complete_frozen):
            start -= 1

        if start <= 0:
            show_done_screen(score)

            break
        
        pygame.display.set_icon(sharks[iconstate])
        if time % 5 == 0:
            iconstate += 1
            iconstate %= 5
        x = pygame.display.Info()
        
        pygame.display.update()
    
running = True   
    



