import pygame

pygame.init()

#game constants
white = (255, 255, 255)
black = (0, 0, 0)
gray = (128, 128, 128)
width = 400
height = 500
background = white
player = pygame.transform.scale(pygame.image.load ('kittyplayer.jpg'), (90, 70))
fps = 60
timer = pygame.time.Clock()


#game variables
player_x = 170
player_y = 400
platforms = [[175, 480, 70, 10]]
jump = False
y_change = 0


#screen
screen = pygame.display.set_mode([width, height])
pygame.display.set_caption('caliGO')


#check for player collisions with blocks
def check_collisions(rect_list, j):
    global player_x
    global player_y
    global y_change
    for i in range(len(rect_list)):
        if rect_list[i].colliderect([player_x, player_y + 60, 90, 10]) and jump == False and y_change > 0:
            j = True
    return j


#update y coordinate of player 
def update_player(y_pos):
    global jump
    global y_change
    jump_height = 10
    gravity = 1
    if jump:
        y_change -= jump_height
        jump = False
    y_pos += y_change
    y_change += gravity
    return y_pos



running = True
while running == True:
    timer.tick(fps)
    screen.fill(background)
    screen.blit(player, (player_x, player_y))
    blocks = []


    for i in range(len(platforms)):
        block = pygame.draw.rect(screen, black, platforms[i], 0, 3)
        blocks.append(block)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    player_y = update_player(player_y)
    jump = check_collisions(blocks, jump)

    pygame.display.flip()
pygame.quit()