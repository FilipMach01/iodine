import pygame, sys
import math
from pygame.locals import QUIT, KEYDOWN, KEYUP, K_LEFT, K_RIGHT, K_SPACE, K_ESCAPE, K_RETURN, K_UP, K_DOWN
import random


def reset():
    global score, player_x, player_y, delta_x, delta_y, shots, shot_radius, shot_speed, player_speed, enemy_speed, player_radius, enemy_radius, player_lives, number_of_enemies, enemies, powerup_radius, powered_up, powershots, powershot_radius, powershot_speed
    score = 0
    player_x, player_y = (200, 260)
    delta_x = 0
    delta_y = 0

    shots = list()
    shot_radius = 4
    shot_speed = 160 / FPS
    powershots = list()
    powershot_radius = 15
    powershot_speed = 170 / FPS
    reset_powerup()
    player_speed = 100 / FPS
    enemy_speed = 85 / FPS
    player_radius = 16
    enemy_radius = 16
    powerup_radius = 20
    powered_up = 0
    # enemies = [x
    #     [20, 0],
    #     [60, -100],
    #     [100, -200],

    # ]
    player_lives = 3
    number_of_enemies = 10
    enemies = list()  # []
    for index in range(0, number_of_enemies):
        x = random.randint(0, resolution[0])
        y = -index * resolution[1] / number_of_enemies
        enemies.append([x, y])


def reset_powerup():
    global powerup_speed, powerup
    powerup_speed = random.randint(50, 100) / FPS
                                                # powerup se objevi o 2 - 4 obrazovky vys
    powerup = [random.randint(0, resolution[0]), - random.randint(2 * resolution[1], 5 * resolution[1])]


def distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    c = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
    return c


def clip(min_value, number, max_value):
    return max(min_value, min(number, max_value))
    

def music():
    global music
    music = pygame.mixer.music.load('musicc.mp3')
    pygame.mixer.music.play(-1)


def shoot_enemy(shots, enemy, enemy_radius, shot_radius, shots_to_remove):
    global score
    for shot in shots:
        # doslo k zasazeni nepritele strelou
        if distance(shot, enemy) <= shot_radius + enemy_radius:
            score += 1
            reset_enemy(enemy)
            shots_to_remove.append(shot)


def reset_enemy(enemy):
    enemy[0] = random.randint(0, resolution[0])
    enemy[1] -= resolution[1]


def render_shots(shots_list, shots_to_remove_list, radius, speed, image):
    global screen
    for shot in shots_list:
        if shot[1] <= 0:
            shots_to_remove_list.append(shot)
        elif not paused:
            shot[1] -= speed
        # pygame.draw.circle(screen, (255, 255, 255), shot, radius)

        screen.blit(image, (shot[0] - image.get_size()[0] / 2,
                            shot[1] - image.get_size()[1] / 2))

    for shot in shots_to_remove_list:
        if shot in shots_list:
            shots_list.remove(shot)


def render_text(text, y_offset=0, color=(109, 68, 212), bg_color=(0, 0, 0)):
    global resolution
    rect = font.get_rect(text)

    font.render_to(screen, ((resolution[0] - rect.width) / 2,
                            (resolution[1] - rect.height) / 2 + y_offset),
                   text, color)
    return rect


def menu():
    global running, in_menu, menu_selection
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_RETURN:
                if menu_selection == 0:
                    reset()
                    in_menu = False
                elif menu_selection == 1:
                    running = False
            elif event.key == K_DOWN:
                if menu_selection == 0:
                    menu_selection = 1
            elif event.key == K_UP:
                if menu_selection == 1:
                    menu_selection = 0

    screen.fill((0, 0, 0))
    render_text('menu', -70, (64, 143, 85))

    default = (109, 68, 212)
    highlight = (224, 234, 255)

    render_text(text='start',
                color=highlight if menu_selection == 0 else default)
    render_text(text='quit',
                y_offset=70,
                color=highlight if menu_selection == 1 else default)


def game_loop():
    global player_x, player_y, delta_x, delta_y, player_speed, player_lives, enemies, enemy_speed, shots, shot_speed, score, paused, running, in_menu, resolution, screen, player_image, enemy_image, shot_image, background_image, powerup_image, powershot_image, heart_image, powerup_radius, powered_up, powershots, powershot_radius, powershot_speed, music,frames_since_last_shot,fire_rate
    # zpracovani eventu
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_LEFT:
                #klavesa stisknuta
                # print("<")
                delta_x -= player_speed
            elif event.key == K_RIGHT:
                # print(">")
                delta_x += player_speed
            elif event.key == K_UP:
                #klavesa stisknuta
                # print("<")
                delta_y -= player_speed
            elif event.key == K_DOWN:
                # print(">")
                delta_y += player_speed
            elif event.key == K_SPACE:
                if frames_since_last_shot > fire_rate:
                    frames_since_last_shot = 0
                    if powered_up > 0:
                        powershots.append([player_x, player_y])
                    else:
                        shots.append([player_x, player_y])
            elif event.key == K_ESCAPE:
                paused = not paused
        elif event.type == KEYUP:
            if event.key == K_LEFT:
                #klavesa uvolnena
                # print("< rel")
                delta_x += player_speed
            elif event.key == K_RIGHT:
                # print("> rel")
                delta_x -= player_speed
            elif event.key == K_UP:
                #klavesa uvolnena
                # print("< rel")
                if player_y > 0:
                    delta_y += player_speed
            elif event.key == K_DOWN:
                # print("> rel")
                if player_y < resolution[1]:
                    delta_y -= player_speed

    if not paused:
        frames_since_last_shot += 1
    
    delta_x = clip(-player_speed, delta_x, player_speed )
    delta_y = clip(-player_speed, delta_y, player_speed )
    if not paused:
        player_x = clip(1, player_x + delta_x, resolution[0] - 1)
        player_y = clip(1, player_y + delta_y, resolution[1] - 1)
    
    # renderovani
    screen.fill((12, 64, 207))
    #player
    screen.blit(background_image,
                (resolution[0] - background_image.get_size()[0] / 2,
                 resolution[1] - background_image.get_size()[1] / 2))

    screen.blit(player_image, (player_x - player_image.get_size()[0] / 2,
                               player_y - player_image.get_size()[1] / 2))
    # for index in [0, 1, 2]:
    #     enemies[index] [1] += enemy_speed

    # for index, enemy in enumerate(enemies):
    #     enemies[index][1] += enemy_speed
    #     enemy[1] += enemy_speed
    c = distance([player_x, player_y], powerup)
    if c <= player_radius + powerup_radius:  # <-- doslo ke kolizi hrace s nepritelem
        reset_powerup()
        print(powerup)
        powered_up = 5 * FPS
    if powerup[1] > resolution[1]:
        reset_powerup()
    powered_up -= 1
    
    powerup[1] += powerup_speed
    screen.blit(powerup_image, (powerup[0] - powerup_image.get_size()[0] / 2,
                                powerup[1] - powerup_image.get_size()[1] / 2))

    shots_to_remove = list()
    powershots_to_remove = list()
    # render enemies
    for enemy in enemies:
        # enemy[0], enemy[1]  <- enemy: List              enemy = [20, 30]
        # enemy["x"], enemy["y"] <- enemy: Dictionary     enemy = {"x": 20, "y": 30}
        # enemy.x, enemy.y <- enemy: Class
        # print(enemy[1])

        # enemy[1] = enemy[1] + enemy_speed
        if not paused:
            enemy[1] += enemy_speed
        shoot_enemy(shots, enemy, enemy_radius, shot_radius, shots_to_remove)
        shoot_enemy(powershots, enemy, enemy_radius, powershot_radius,
                    powershots_to_remove)

        c = distance([player_x, player_y], enemy)
        # doslo ke kolizi hrace s nepritelem
        if c <= player_radius + enemy_radius:
            player_lives -= 1
            # score = score - 5 if score - 5 > 0 else 0
            score = max(score - 5, 0)
            reset_enemy(enemy)
        if player_lives == 0:
            in_menu = True
        if enemy[1] >= resolution[1]:
            reset_enemy(enemy)

        # vyplata = 20
        # kasicka = 13
        # obrazek kola = 100
        # while konec mesice:
        #     kasicka += vyplata

        #     if kasicka >= obrazek kola:
        #         kup kolo ()

        # leden: 13
        # unor: 33
        # brezen: 53
        # duben: 73
        # kveten: 93
        # cerven: 113

        screen.blit(enemy_image, (enemy[0] - enemy_image.get_size()[0] / 2,
                                  enemy[1] - enemy_image.get_size()[1] / 2))

    render_shots(shots, shots_to_remove, shot_radius, shot_speed, shot_image)
    render_shots(powershots, powershots_to_remove, powershot_radius,
                 powershot_speed, powershot_image)
    for life in range(player_lives):

        screen.blit(heart_image, (15 + life * 20, 15))

        font.render_to(screen, (240, 20), str(score).zfill(6), (224, 234, 255))

    if paused:
        render_text(text='paused', color=(224, 234, 255))


# inicializace (pocatecni nastaveni, spusteni)
pygame.init()
resolution = (400, 300)
screen = pygame.display.set_mode(resolution)
pygame.display.set_caption('Tyrian Simulator')
clock = pygame.time.Clock()
font = pygame.freetype.Font('font.ttf', 15)

# music/sounds

player_image = pygame.image.load("player1.png").convert_alpha()
enemy_image = pygame.image.load("enemy0.png").convert_alpha()
shot_image = pygame.image.load("shots0.png").convert_alpha()
background_image = pygame.image.load("sky.gif").convert_alpha()
powerup_image = pygame.image.load('powerup2.png').convert_alpha()
powershot_image = pygame.image.load('pwr_shot.png').convert_alpha()
heart_image = pygame.image.load('heart.png').convert_alpha()

FPS = 60
player_x, player_y = (200, 260)
delta_x = 0
delta_y = 0

shots = list()
shot_radius = 6
shot_speed = 80 / FPS
fire_rate = 0.8 * FPS   # cislo znaci, jak dlouha je prodleva mezi strelami ve vterinach
frames_since_last_shot = 0

player_speed = 50 / FPS
enemy_speed = 50 / FPS
player_radius = 15
enemy_radius = 15
# enemies = [x
#     [20, 0],
#     [60, -100],
#     [100, -200],

# ]
player_lives = 3
number_of_enemies = 10
enemies = list()  # []
for index in range(0, number_of_enemies):
    x = random.randint(0, resolution[0])
    y = -index * resolution[1] / number_of_enemies
    enemies.append([x, y])

# for enemy in enemies:
#     enemy = [20, 30]  # 1. beh cyklu   # enemies[0]
#     enemy = [40, 30]  # 2. beh cyklu   # enemies[1]

paused = False
in_menu = True
menu_selection = 0

# herni smycka
running = True
while running:
    if in_menu:
        menu()
    else:
        game_loop()

    pygame.display.update()
    clock.tick(FPS)
