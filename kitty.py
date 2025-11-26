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

#platforms
platform_img = pygame.image.load('platform_1.png').convert_alpha()
platform_width = 100  #match platform size
platform_height = 30
platform_img = pygame.transform.scale(platform_img, (platform_width, platform_height))


#game variables
player_x = 170
player_y = 400
platforms = [[175, 480, 90, 10], [50, 330, 90, 10], [125, 370, 90, 10], [175, 260, 90, 10], [185, 150, 90, 10], [205, 150, 90, 10], [175, 40, 90, 10]]

jump = False
y_change = 0
x_change = 0
player_speed = 3
high_score = 0

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
        y_change = -jump_height # negative y_change is positive jump
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
    min_distance = 100  #min distance from player
    max_distance = 200  #max distance from player

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
    screen.fill(background)
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
    

    blocks = []
    for p in platforms:
        screen.blit(platform_img, (p[0], p[1]))
        blocks.append(pygame.Rect(p[0], p[1], platform_width, platform_height))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN: #check when up arrow pressed
            if event.key == pygame.K_UP and y_change == 0:
                jump = True
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

    player_y = update_player(player_y)
    check_collisions(blocks)
    player_x += x_change 
    check_collisions(blocks)

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