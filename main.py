import pygame
from sprites import Dragon, Laser, Plane
pygame.init()

screen = pygame.display.set_mode((2000, 1000))
pygame.display.set_caption("Day 3")
game_active = False
released = False


frame_rate = pygame.time.Clock()
score = 0
font = pygame.font.Font(None, 50)

background = pygame.image.load("images/sky.png").convert_alpha()
background_rect = background.get_rect()

dragon_timer = pygame.USEREVENT + 1
pygame.time.set_timer(dragon_timer, 500)
count = 0



player = pygame.sprite.GroupSingle()
player.add(Plane())
laser_group = pygame.sprite.Group()
dragon_group = pygame.sprite.Group()

def title_screen():
    global font

    title_text = font.render('Welcome To Day 4!', False, 'white')
    title_rect = title_text.get_rect(midtop=(1000, 200))
    screen.blit(title_text, title_rect)

    if score > 0:
        score_label = font.render(f"Your Score: {score}", False, 'white')
        score_rect = score_label.get_rect(center=(1000, 360))
        screen.blit(score_label, score_rect)

    instructions_label = font.render('Press the space bar to Start', False, 'gray')
    instructions_rect = instructions_label.get_rect(center=(1000, 500))
    screen.blit(instructions_label, instructions_rect)


def display_score():

    global score, dragon_group, game_active
    for dragon in dragon_group:
        if dragon.rect.x < 0:
            game_active = False
        score += dragon.return_score()


    score_font = pygame.font.Font(None, 50)
    score_surface = score_font.render('Score: ' + str(score), False, 'white')
    score_rectangle = score_surface.get_rect(topleft=(940, 50))
    screen.blit(score_surface, score_rectangle)


def shoot():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        global player, laser_group, released, game_active
        if released:
            laser_group.add(Laser(player.sprite.rect.x, player.sprite.rect.y))
            laser_group.add(Laser(player.sprite.rect.x, player.sprite.rect.y + 85))
            released = False
    else:
        released = True


def reset():
    global score,released
    score = 0
    dragon_group.empty()
    player.sprite.reset()
    released = False



while True:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not game_active:
                    reset()
                    game_active = True
        if game_active:
            if event.type == dragon_timer:
                if count == 0:
                    dragon_group.add(Dragon())
                    count = 10
                count -=1

    if game_active:
        screen.blit(background, background_rect)

        dragon_group.draw(screen)
        dragon_group.update(laser_group)

        player.draw(screen)
        player.update()
        game_active = player.sprite.player_colided(dragon_group)

        shoot()
        laser_group.draw(screen)
        laser_group.update()

        display_score()



    else:
        screen.fill((0, 0, 0))
        title_screen()



    pygame.display.update()

    frame_rate.tick(60)


