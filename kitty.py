import pygame
import random


pygame.init()

#game constants
white = (255, 255, 255)
black = (0, 0, 0)
gray = (128, 128, 128)
width = 400
height = 500
background = white
player = pygame.transform.scale(pygame.image.load ('kitty.png'), (90, 70))
fps = 60
timer = pygame.time.Clock()
score = 0
game_over = False


#game variables
player_x = 170
player_y = 400
platforms = [[0, 480, 700, 10], [50, 330, 70, 10], [165, 370, 70, 10], [175, 260, 70, 10], [185, 150, 70, 10], [205, 150, 70, 10], [175, 40, 70, 10]]
jump = False
y_change = 0
x_change = 0
player_speed = 3
animation_tracker = 0.0
animation_increment = 0.1 #every time the game ticks, animation_tracker goes up by ONE increment


#screen
screen = pygame.display.set_mode([width, height])
pygame.display.set_caption('caliGO')

#font
font = pygame.font.SysFont(None, 30)

#frames
def get_frames(sheet, count):
    frame_list = []
    coords = [
        (0, 0),
        (640, 0),
        (0, 640),
        (640, 640),
    ]
    for i in range(count):
        frame = pygame.Surface((640, 640), pygame.SRCALPHA)
        source_rect = (coords[i][0], coords[i][1], 640, 640)
        frame.blit(sheet, (0, 0), source_rect)
        frame_list.append(frame)
    return frame_list
idle = pygame.image.load('idle.png').convert_alpha()
idle_frames = get_frames(idle, 3)
jump = pygame.image.load('jump.png').convert_alpha()
jump_frames = get_frames(jump, 4)

#check for player collisions with blocks
def check_collisions(rect_list):
    global player_x
    global player_y
    global y_change
    for i in range(len(rect_list)):
        if rect_list[i].colliderect([player_x, player_y + 60, 90, 10]) and y_change > 0: #if it's colliding or already jumping, move player say it's colliding
            player_y = rect_list[i].top - 60
            y_change = 0
            return True            
    return False


#update y coordinate of player 
def update_player(y_pos):
    global jump
    global y_change
    jump_height = 17
    gravity = 1
    if jump == True:
        y_change = -jump_height # negative y_change is positive jump
        jump = False
    y_pos += y_change
    y_change += gravity
    return y_pos

#movement of platforms
def update_platforms(my_list, y_pos, change):
    global score
    if y_pos < 250 and change < 0:
        for i in range(len(my_list)):
            my_list[i][1] -= change
    else:
        pass
    for item in range(len(my_list)):
        if my_list[item][1] > 500:
            my_list[item] = [random.randint(10, 320), random.randint(-50, -10), 70, 10]
            score += 1
    return my_list


running = True
while running == True:
    timer.tick(fps)
    screen.fill(background)

    animation_tracker = animation_tracker + animation_increment 
    if animation_tracker >= len(idle_frames): #reset animation trackver every time it goes over 3
        animation_tracker = 0.0
    current_image = idle_frames[int(animation_tracker)] #the "int" rounds down. so if animation_tracker is at 1.1, it'll use frame 1. if animation_tracker is at 0.5, it'll use frame 0. et cetera

    blocks = []
    score_text = font.render('score: ' + str(score), True, black, background)
    screen.blit(score_text, (320, 20))

    for i in range(len(platforms)):
        block = pygame.draw.rect(screen, black, platforms[i], 0, 3)
        blocks.append(block)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN: #check when up arrow pressed
            if event.key == pygame.K_UP and y_change == 0:
                jump = True
            if event.key == pygame.K_RIGHT:
                x_change = player_speed
            if event.key == pygame.K_LEFT:
                x_change = -player_speed

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                x_change = 0
            if event.key == pygame.K_LEFT:
                x_change = 0

    player_y = update_player(player_y)
    player_x += x_change 
    platforms = update_platforms(platforms, player_y, y_change)
    check_collisions(blocks)

    if x_change > 0:
        player = pygame.transform.scale(current_image, (90, 70))
    if x_change < 0:
        current_image = pygame.transform.flip(current_image, True, False)
        player = pygame.transform.scale(current_image, (90, 70))
    screen.blit(player, (player_x, player_y))

    pygame.display.flip()
pygame.quit()