import pygame
import random


pygame.init()

#game constants
white = (255, 255, 255)
black = (0, 0, 0)
gray = (128, 128, 128)
width = 600
height = 500
background = white
#screen
screen = pygame.display.set_mode([width, height])
pygame.display.set_caption('caliGO')
#more constants
player = pygame.transform.scale(pygame.image.load ('kitty.png'), (90, 70))
fps = 60
timer = pygame.time.Clock()
score = 0
game_over = False

#background
background_img = pygame.image.load("background.png").convert()
background_img = pygame.transform.scale(background_img, (width, height))
backgrounds = [
    pygame.transform.scale(pygame.image.load("background.png"), (width, height)),
    pygame.transform.scale(pygame.image.load("background1.png"), (width, height)),
    pygame.transform.scale(pygame.image.load("background2.png"), (width, height)),
    pygame.transform.scale(pygame.image.load("background3.png"), (width, height)),
    pygame.transform.scale(pygame.image.load("background4.png"), (width, height)),
    pygame.transform.scale(pygame.image.load("background5.png"), (width, height)),
    pygame.transform.scale(pygame.image.load("background6.png"), (width, height)),
    pygame.transform.scale(pygame.image.load("background7.png"), (width, height)),
    pygame.transform.scale(pygame.image.load("background8.png"), (width, height)),
    pygame.transform.scale(pygame.image.load("background9.png"), (width, height)),
    pygame.transform.scale(pygame.image.load("background10.png"), (width, height)),
    pygame.transform.scale(pygame.image.load("background11.png"), (width, height)),
    pygame.transform.scale(pygame.image.load("background12.png"), (width, height)),
    pygame.transform.scale(pygame.image.load("background13.png"), (width, height)),
    pygame.transform.scale(pygame.image.load("background14.png"), (width, height)),
    pygame.transform.scale(pygame.image.load("background15.png"), (width, height)),
    pygame.transform.scale(pygame.image.load("background16.png"), (width, height)),
    pygame.transform.scale(pygame.image.load("background17.png"), (width, height)),
    pygame.transform.scale(pygame.image.load("background18.png"), (width, height)),
] #woa so many 
current_background = 0
last_background_change = pygame.time.get_ticks()

#birb
bird_x = 100
bird_y = 100
bird_height = 72
bird_width = 112
bird_speed = 1
bird_rect = pygame.Rect(bird_x, bird_y, bird_width, bird_height)
bird_img1 = pygame.transform.scale(pygame.image.load("bird.png"), (bird_width, bird_height))
bird_img2 = pygame.transform.scale(pygame.image.load("bird2.png"), (bird_width, bird_height))
bird_img = bird_img1



#platforms
platform_img = pygame.image.load('platform_1.png').convert_alpha()
platform_width = 100  
platform_height = 50
platform_img = pygame.transform.scale(platform_img, (platform_width, platform_height))

#meow
jump_sound = pygame.mixer.Sound("kittymeow.mp3")

#game variables
player_x = 170
player_y = 400
platforms = [
    [175, 480, 90, 10], 
    [50, 330, 90, 10], 
    [125, 370, 90, 10], 
    [175, 260, 90, 10], 
    [185, 200, 90, 10], 
    [205, 150, 90, 10], 
    [175, 40, 90, 10]
    ] 

jump = False
y_change = 0
x_change = 0
player_speed = 3
high_score = 0

last_player_y = player_y

#animation variables
animation_tracker = 0.0
animation_increment = 0.1
is_grounded = False
facing_left = False

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

idle_sheet = pygame.image.load('idle.png').convert_alpha()
idle_frames = get_frames(idle_sheet, 3)

jump_sheet = pygame.image.load('jump.png').convert_alpha()
jump_frames = get_frames(jump_sheet, 4)


#restart
def restart():
    global player_x, player_y, y_change, x_change, score, game_over, platforms, jump
    player_x = 170
    player_y = 400
    y_change = 0
    x_change = 0
    score = 0
    game_over = False

    platforms = [
        [175, 480, 90, 10],
        [50, 330, 90, 10],
        [125, 370, 90, 10],
        [175, 260, 90, 10],
        [185, 150, 90, 10],
        [205, 150, 90, 10],
        [175, 40, 90, 10]
    ]

    jump = False


    waiting = True
    while waiting:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                quit()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
                waiting = False


    #show start screen again
    show_start_screen()

    waiting = True
    while waiting:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                quit()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
                waiting = False 



#font
font = pygame.font.SysFont(None, 30)

#update y coordinate of player 
def update_player(y_pos):
    global jump
    global y_change
    jump_height = 15
    gravity = 1
    if jump == True:
        y_change = -jump_height #negative y_change is positive jump
        jump = False
    y_pos += y_change
    y_change += gravity
    return y_pos

player_y = update_player(player_y)


#check for player collisions with blocks
def check_collisions(rect_list):
    global player_x, player_y, y_change, is_grounded
    is_grounded = False
    player_rect = pygame.Rect(player_x, player_y + 60, 90, 10)  #bottom of player

    for block in rect_list:
        if block.colliderect(player_rect) and y_change >= 0:
            player_y = block.top - 60
            y_change = 0
            is_grounded = True
            return True
    return False


#movement of platforms
def update_platforms(my_list, y_pos, change):
    global score
    global player_x
    min_distance = 100  
    max_distance = 200  

    #move platforms down if player is high enough
    if y_pos < 250 and change < 0:
        for i in range(len(my_list)):
            my_list[i][1] -= change

    #respawn platforms that went off screen
    for item in range(len(my_list)):
        if my_list[item][1] > height:
            while True:
                new_x = random.randint(10, width - 80)
                if abs(new_x - player_x) >= min_distance and abs(new_x - player_x) <= max_distance:
                    break
            new_y = random.randint(-50, -10)
            my_list[item] = [new_x, new_y, 70, 10]
            score += 1

    return my_list




#start screen
def show_start_screen():
    screen.fill(white)
    title = font.render("caliGO", True, black)
    start_text = font.render("the kitty has probably forgiven you by now, press enter", True, black)
    
    screen.blit(title, (width//2 - title.get_width()//2, 150))
    screen.blit(start_text, (width//2 - start_text.get_width()//2, 250))

    pygame.display.flip()

#game over screen
def show_game_over_screen(score, high_score):
    screen.fill(white)
    over = font.render("game over, the kitty fell!!", True, black)
    score_text = font.render(f"Score: {score}", True, black)
    restart_text = font.render("press space to ask the kitty for forgiveness", True, black)

    screen.blit(over, (width//2 - over.get_width()//2, 150))
    screen.blit(score_text, (width//2 - score_text.get_width()//2, 200))
    screen.blit(restart_text, (width//2 - restart_text.get_width()//2, 260))


running = True
while running == True:
    timer.tick(fps)
    screen.blit(backgrounds[current_background], (0, 0))
    if score > 10 and score < 20:
        current_background = 1
    if score > 20 and score < 30:
        current_background = 2
    if score > 30 and score < 40:
        current_background = 3
    if score > 50 and score < 60:
        current_background = 4
    if score > 60 and score < 70:
        current_background = 5
    if score > 70 and score < 80:
        current_background = 6
    if score > 80 and score < 90:
        current_background = 7
    if score > 90 and score < 100:
        current_background = 8
    if score > 100 and score < 110:
        current_background = 9
    if score > 110 and score < 120:
        current_background = 10
    if score > 120 and score < 130:
        current_background = 11
    if score > 130 and score < 140:
        current_background = 12
    if score > 140 and score < 150:
        current_background = 13
    if score > 150 and score < 160:
        current_background = 14
    if score > 160 and score < 170:
        current_background = 15
    if score > 170 and score < 180:
        current_background = 16
    if score > 180 and score < 190:
        current_background = 17
    if score > 190 and score < 200:
        current_background = 18

    #animation system
    if is_grounded:
        animation_tracker += animation_increment
        if animation_tracker >= len(idle_frames):
            animation_tracker = 0.0
        player = idle_frames[int(animation_tracker)]
    else:
        if y_change < -6:
            player = jump_frames[0]
        elif -6 <= y_change < 0:
            player = jump_frames[1]
        elif 0 <= y_change < 6:
            player = jump_frames[2]
        else:
            player = jump_frames[3]

#scale + flip
    player = pygame.transform.scale(player, (90, 70))
    if facing_left:
        player = pygame.transform.flip(player, True, False)

    screen.blit(player, (player_x, player_y))
    blocks = []
    score_text = font.render('score: ' + str(score), True, black, background)
    screen.blit(score_text, (400, 50))
    high_score_text = font.render('high score: ' + str(score), True, black, background)
    screen.blit(high_score_text, (400, 20))
    
    bird_x += bird_speed
    bird_rect.x = bird_x
    if bird_x <= 0 or bird_x + bird_width >= width:
        bird_speed *= -1
    screen.blit(bird_img, (bird_x, bird_y))

    blocks = []
    for p in platforms:
        screen.blit(platform_img, (p[0], p[1]))
        blocks.append(pygame.Rect(p[0], p[1], platform_width, platform_height))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN: #check when up arrow pressed
            if event.key == pygame.K_UP and is_grounded:
                jump = True
                jump_sound.play()
            if event.key == pygame.K_RIGHT:
                x_change = player_speed
                facing_left = False
            if event.key == pygame.K_LEFT:
                x_change = -player_speed
                facing_left = True
            if event.key == pygame.K_SPACE:
               show_start_screen()

               waiting = True
               while waiting:
                  for e in pygame.event.get():
                     if e.type == pygame.QUIT:
                            pygame.quit()
                            quit()
                     if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                            waiting = False  
            if event.key == pygame.K_RETURN:
                restart()
                continue

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                x_change = 0
            if event.key == pygame.K_LEFT:
                x_change = 0

    player_rect = pygame.Rect(player_x, player_y, 90, 70)
    if player_rect.colliderect(bird_rect):
        game_over = True


    player_y = update_player(player_y)
    check_collisions(blocks)
    player_x += x_change 
    check_collisions(blocks)
    current_time = pygame.time.get_ticks()

    if player_y < 488:
        platforms = update_platforms(platforms, player_y, y_change)
    else:
        game_over = True
        y_change = 0
    if score > high_score:
        high_score = score

    if game_over == True:
        show_game_over_screen(score, high_score)
    pygame.display.flip()
pygame.quit()