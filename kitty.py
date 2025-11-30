import pygame
import random


pygame.init()

#music
pygame.mixer.music.load("music.mp3")
pygame.mixer.music.play(-1)

#game constants
white = (255, 255, 255)
black = (0, 0, 0)
gray = (128, 128, 128)
red = (255, 0, 0)
blue = (0, 0, 255)
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
celebrating = False
coins = 0



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
bird_y = 200
bird_height = 36
bird_width = 56
bird_speed = 1
bird_rect = pygame.Rect(bird_x, bird_y, bird_width, bird_height)
bird_img1 = pygame.transform.scale(pygame.image.load("bird.png"), (bird_width, bird_height))
bird_img2 = pygame.transform.scale(pygame.image.load("bird2.png"), (bird_width, bird_height))
flipped_bird1 = pygame.transform.flip(bird_img1, True, False)
bird_img = bird_img1
last_bird_swap = pygame.time.get_ticks()
bird_swap_interval = 1000

#coin
coin_width = 20
coin_height = 20
coin_img = pygame.transform.scale(pygame.image.load("coin.png"), (coin_width, coin_height))
coins_list = [
    pygame.Rect(random.randint(50, width-50), random.randint(50, height-100), coin_width, coin_height)
]
for coin in coins_list:
    screen.blit(coin_img, (coin.x, coin.y))


#platforms
platform_img = pygame.image.load('platform_1.png').convert_alpha()
platform_width = 90
platform_height = 10
platform_img = pygame.transform.scale(platform_img, (platform_width, platform_height))

#meow
jump_sound = pygame.mixer.Sound("kittymeow.mp3")

#game variables
player_x = 170
player_y = 400
platforms = [
    [175, 480, 90, 10],
    [60, 400, 90, 10],
    [220, 330, 90, 10],
    [100, 260, 90, 10],
    [190, 190, 90, 10],
    [40, 120, 90, 10],
    [230, 50, 90, 10]
]
jump = False
y_change = 0
x_change = 0
player_speed = 3
high_score = 0

last_player_y = player_y

celebrate_frames = [
    pygame.transform.scale(pygame.image.load("yay!.png").convert_alpha(), (width, height)),
    pygame.transform.scale(pygame.image.load("yay!!.png").convert_alpha(), (width, height)),
    pygame.transform.scale(pygame.image.load("yay!!!.png").convert_alpha(), (width, height)),]

celebrate_platform = [width//2 - 45, 300, 90, 10]
celebrate_img = pygame.image.load("yay!.png").convert_alpha()
celebrate_img = pygame.transform.scale(celebrate_img, (width, height))

celebrate_index = 0
celebrate_timer = pygame.time.get_ticks()
celebrate_interval = 500
celebrate_flip_timer = pygame.time.get_ticks()
celebrate_flip_interval = 1000
celebrate_facing_left = False


celebrate_platform_img = pygame.transform.scale(pygame.image.load('celebrationplatform.png').convert_alpha(), (100, 20))
celebrate_platform_rect = pygame.Rect(width//2 - 50, 300, 100, 20)
font_large = pygame.font.SysFont(None, 40)
text_above = font_large.render("yippeeee!!", True, white)
text_below = font_large.render("you win!!", True, white)

def celebrate():
    global celebrate_index, celebrate_timer, current_time, player_x, player_y, is_grounded, y_change, player, animation_tracker, animation_index
    current_time = pygame.time.get_ticks()
    if current_time - celebrate_timer >= celebrate_interval:
        celebrate_index = (celebrate_index + 1) % len(celebrate_frames)
        celebrate_timer = current_time
    screen.blit(celebrate_frames[celebrate_index], (0, 0))
    screen.blit(celebrate_platform_img, (celebrate_platform_rect.x, celebrate_platform_rect.y))
    
    animation_tracker += animation_increment
    animation_index = int(animation_tracker) % len(idle_frames)
    player = idle_frames[animation_index]

    global celebrate_facing_left, celebrate_flip_timer
    now = pygame.time.get_ticks()
    if now - celebrate_flip_timer >= celebrate_flip_interval:
        celebrate_facing_left = not celebrate_facing_left
        celebrate_flip_timer = now

    if celebrate_facing_left:
        player = pygame.transform.flip(player, True, False)

    player = pygame.transform.scale(player, (90, 70))
    player_x = celebrate_platform_rect.x + (celebrate_platform_rect.width // 2) - 45
    player_y = celebrate_platform_rect.y - 70
    screen.blit(player, (player_x, player_y))
    screen.blit(text_above, (width//2 - text_above.get_width()//2, celebrate_platform_rect.y - 70 - 40))
    screen.blit(text_below, (width//2 - text_below.get_width()//2, celebrate_platform_rect.y + 20 + 10))

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
    global player_x, player_y, y_change, x_change, score, game_over, platforms, jump, celebrating, current_background

    player_x = 170
    player_y = 400
    y_change = 0
    x_change = 0
    score = 0
    game_over = False
    jump = False
    celebrating = False
    current_background = 0

    platforms = [
        [175, 480, 90, 10],
        [60, 400, 90, 10],
        [220, 330, 90, 10],
        [100, 260, 90, 10],
        [190, 190, 90, 10],
        [40, 120, 90, 10],
        [230, 50, 90, 10]
    ]

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
        y_change = -jump_height
        jump = False
    y_pos += y_change
    if is_grounded == False:
        y_change += gravity
    return y_pos

player_y = update_player(player_y)


#check for player collisions with blocks
def check_collisions(rect_list):
    global player_x, player_y, y_change, is_grounded
    is_grounded = False
    # formerly:     player_rect = pygame.Rect(player_x, player_y + 60, 90, 10)  #bottom of player
    player_rect = pygame.Rect(player_x + 20, player_y + 50, 50, 20)  #bottom of player
    # y-height: starts at 60th pixel and ends at  70th pixel (total cat height is 70)
    # pygame.draw.rect(screen, red, player_rect, 1)

    for block in rect_list:
        if block.colliderect(player_rect) and y_change >= 0:
            player_y = block.top - 50
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
                new_x = random.randint(10, width - platform_width)
                if abs(new_x - player_x) >= min_distance and abs(new_x - player_x) <= max_distance:
                    break
            new_y = random.randint(-50, -10)
            my_list[item] = [new_x, new_y, platform_width, platform_height]
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
    over = font.render("game over, the kitty fell!! (press enter)", True, black)
    score_text = font.render(f"Score: {score}", True, black)


    screen.blit(over, (width//2 - over.get_width()//2, 150))
    screen.blit(score_text, (width//2 - score_text.get_width()//2, 200))


running = True
while running == True:
    timer.tick(fps)
    if celebrating:
        x_change = 0
        y_change = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        celebrate()
        pygame.display.flip()
        continue

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
    high_score_text = font.render('high score: ' + str(high_score), True, black, background)
    screen.blit(high_score_text, (400, 20))
    coin_text = font.render('coins: ' + str(coins), True, black, background)
    screen.blit(coin_text, (400, 80))



    blocks = []
    for p in platforms:
        # pygame.draw.rect(screen, blue, (p[0], p[1], platform_width, platform_height))
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
            if event.key == pygame.K_RETURN and game_over:
                restart()

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                x_change = 0
            if event.key == pygame.K_LEFT:
                x_change = 0

    player_rect = pygame.Rect(player_x, player_y, 90, 70)
    if player_rect.colliderect(bird_rect):
        game_over = True
    for coin in coins_list[:]:
        if player_rect.colliderect(coin):
            coins += 1
            coins_list.remove(coin)

    for coin in coins_list:
        screen.blit(coin_img, (coin.x, coin.y))
        if player_y < 250 and y_change < 0:
            coin.y += -y_change
        if coin.y > height:
            coins_list.remove(coin)

    if len(coins_list) < 1:
        coins_list.append(pygame.Rect(random.randint(50, width-50), random.randint(0,height//4), coin_width, coin_height))

    bird_x += bird_speed
    bird_rect.x = bird_x
    if bird_x <= 0 or bird_x + bird_width >= width:
        bird_speed *= -1

    current_time = pygame.time.get_ticks()
    if current_time - last_bird_swap >= bird_swap_interval:
        if bird_img == bird_img1:
            bird_img = bird_img2
        else:
            bird_img = bird_img1
        last_bird_swap = current_time

    if bird_speed < 0:
        screen.blit(pygame.transform.flip(bird_img, True, False), (bird_x, bird_y))
    else:
        screen.blit(bird_img, (bird_x, bird_y))


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
    if score > 200 and not celebrating:
        celebrating = True
        player_y = celebrate_platform_rect.y - 70


    if is_grounded == True:
        animation_tracker = animation_tracker + animation_increment 
        if animation_tracker >= len(idle_frames):
            animation_tracker = 0.0
        player = idle_frames[int(animation_tracker)]
    elif is_grounded == False:
        if y_change < -6:
            player = jump_frames[0] 
        if y_change > -6 and y_change < 0:
            player = jump_frames[1]
        if y_change > 0 and y_change < 6: 
            player = jump_frames[2]
        if y_change > 6:
            player = jump_frames[3]

    player = pygame.transform.scale(player, (90, 70))
    if facing_left:
        player = pygame.transform.flip(player, True, False)

    screen.blit(player, (player_x, player_y))

    if game_over == True:
        show_game_over_screen(score, high_score)
    pygame.display.flip()
pygame.quit()