import pygame, sys
import math
import pygame.mixer as mixer
from pygame.locals import QUIT, KEYDOWN, KEYUP, K_LEFT, K_RIGHT, K_SPACE, K_ESCAPE, K_RETURN, K_UP, K_DOWN
import random
from collections import deque


def reset():
    global score,high_score, player_x, player_y, delta_x, delta_y, shots, shot_radius, shot_speed, player_speed, enemy_speed, player_radius, \
        enemy_radius, player_lives, number_of_enemies, enemies, powerup_radius, \
        powered_up, powershots, powershot_radius, powershot_speed, pw_heart_radius, pw_heart
    score = 0
    with open('high_score.dat', "r+") as file:
        for line in file:
            high_score = int(line.strip())

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
    pw_heart_radius = 20
    pw_heart = 0
    reset_pw_heart()

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


def reset_pw_heart():
    global pw_heart_speed, pw_heart
    pw_heart_speed = random.randint(50, 100) / FPS
    pw_heart = [random.randint(0, resolution[0]), - random.randint(4 * resolution[1], 11 * resolution[1])]


def distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    c = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
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
            explosions.append({"coord": enemy[:], "frame": 0})
            reset_enemy(enemy)
            shots_to_remove.append(shot)

            pygame.mixer.Channel(0).play(pygame.mixer.Sound('explosion_sound.mp3'), maxtime=600)


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


def scroll(layer, offset):
    target = pygame.Surface(layer.get_size(), pygame.SRCALPHA)
    target.blit(layer, (0, offset))
    target.blit(layer, (0, offset - layer.get_height()))
    return target


def draw_background():
    global background_layers, screen, player_x, player_y, delta_x, delta_y
    for number, layer in enumerate(background_layers):
        layer = scroll(layer, 0.5 * (len(background_layers) - number))
        background_layers[number] = layer
        x = player_x / (number + 1)
        y = player_y / (number + 1)

        screen.blit(layer, (
            (screen.get_width() - layer.get_width() - x) / 2, (screen.get_height() - layer.get_height() - y) / 2))


def generate_background():
    global background_layers, screen, player_x, player_y, delta_x, delta_y
    for number, layer in enumerate(background_layers):
        for star in range(200):
            x = random.randint(0, layer.get_width())
            y = random.randint(0, layer.get_height())

            pygame.draw.rect(layer, (250 - 40 * number, 250 - 40 * number, 250 - 40 * number), (x, y, 1, 1))


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
                    mixer.music.play(-1)
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
    global player_x, player_y, delta_x, delta_y, player_speed, player_lives, enemies, enemy_speed, shots, shot_speed, score, paused, running, in_menu, \
        resolution, screen, player_image, enemy_image, shot_image, background_image, powerup_image, powershot_image, heart_image, powerup_radius, \
        powered_up, powershots, powershot_radius, powershot_speed, music, frames_since_last_shot, fire_rate, pw_heart_radius, pw_heart
    # zpracovani eventu
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_LEFT:
                # klavesa stisknuta
                # print("<")
                delta_x -= player_speed
            elif event.key == K_RIGHT:
                # print(">")
                delta_x += player_speed
            elif event.key == K_UP:
                # klavesa stisknuta
                # print("<")
                delta_y -= player_speed
            elif event.key == K_DOWN:
                # print(">")
                delta_y += player_speed
            elif event.key == K_SPACE:
                if frames_since_last_shot > fire_rate:
                    frames_since_last_shot = 0
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound('shot_sound.mp3'), maxtime=600)
                    if powered_up > 0:
                        powershots.append([player_x, player_y])

                    else:
                        shots.append([player_x, player_y])
            elif event.key == K_ESCAPE:
                paused = not paused
        elif event.type == KEYUP:
            if event.key == K_LEFT:
                # klavesa uvolnena
                # print("< rel")
                delta_x += player_speed
            elif event.key == K_RIGHT:
                # print("> rel")
                delta_x -= player_speed
            elif event.key == K_UP:
                # klavesa uvolnena
                # print("< rel")
                if player_y > 0:
                    delta_y += player_speed
            elif event.key == K_DOWN:
                # print("> rel")
                if player_y < resolution[1]:
                    delta_y -= player_speed

    if not paused:
        frames_since_last_shot += 1

    delta_x = clip(-player_speed, delta_x, player_speed)
    delta_y = clip(-player_speed, delta_y, player_speed)
    if not paused:
        player_x = clip(1, player_x + delta_x, resolution[0] - 1)
        player_y = clip(1, player_y + delta_y, resolution[1] - 1)

    # renderovani
    screen.fill((0, 0, 0))
    # player

    draw_background()

    img = player_image
    if delta_x < 0:
        img = player_image_left
    if delta_x > 0:
        img = player_image_right
    screen.blit(img, (player_x - img.get_size()[0] / 2,
                      player_y - img.get_size()[1] / 2))

    if powered_up > 0:
        img = player_ani[0]
        player_ani.rotate(1)
        screen.blit(img, (player_x - img.get_size()[0] / 2,
                          player_y - img.get_size()[1] / 2))

    # for index in [0, 1, 2]:
    #     enemies[index] [1] += enemy_speed

    # for index, enemy in enumerate(enemies):
    #     enemies[index][1] += enemy_speed
    #     enemy[1] += enemy_speed
    c = distance([player_x, player_y], powerup)

    if c <= player_radius + powerup_radius:  # <-- doslo ke kolizi hrace s powerupem
        reset_powerup()
        print(powerup)
        powered_up = 5 * FPS

    if powerup[1] > resolution[1]:
        reset_powerup()
    powered_up -= 1
    c = distance([player_x, player_y], pw_heart)
    if c <= player_radius + pw_heart_radius:
        reset_pw_heart()
        player_lives += 1

    if pw_heart[1] > resolution[1]:
        reset_pw_heart()

    if not paused:
        powerup[1] += powerup_speed
    screen.blit(powerup_image, (powerup[0] - powerup_image.get_size()[0] / 2,
                                powerup[1] - powerup_image.get_size()[1] / 2))
    if not paused:
        pw_heart[1] += pw_heart_speed
    screen.blit(heart_image, (pw_heart[0] - heart_image.get_size()[0] / 2,
                              pw_heart[1] - heart_image.get_size()[1] / 2))

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
            if score > high_score:
                with open('high_score.dat',"w+")as file:
                    file.write(str (score))
        if enemy[1] >= resolution[1]:
            reset_enemy(enemy)

        screen.blit(enemy_image, (enemy[0] - enemy_image.get_size()[0] / 2,
                                  enemy[1] - enemy_image.get_size()[1] / 2))
    explosions_to_remove = list()
    for explosion in explosions:
        screen.blit(
            explosion_image,
            (explosion["coord"][0] - enemy_radius, explosion["coord"][1] - enemy_radius),
            (explosion["frame"] * (enemy_radius-1) * 2 , 0, (enemy_radius-1) * 2, enemy_radius * 2)
        )
        explosion["frame"] += 1

        if explosion["frame"] > 17:
            explosions_to_remove.append(explosion)
    for explosion in explosions_to_remove:
        explosions.remove(explosion)

    render_shots(shots, shots_to_remove, shot_radius, shot_speed, shot_image)
    render_shots(powershots, powershots_to_remove, powershot_radius,
                 powershot_speed, powershot_image)
    for life in range(player_lives):
        screen.blit(heart_image, (15 + life * 20, 15))

    font.render_to(screen, (240, 20), str(score).zfill(6), (224, 234, 255))
    font.render_to(screen, (240, 40), str(high_score).zfill(6), (124, 134, 155))


    if paused:
        render_text(text='paused', color=(224, 234, 255))
    else:
        enemy_speed *= 1.0003


# inicializace (pocatecni nastaveni, spusteni)
pygame.init()
mixer.init()
mixer.music.load('music.mp3')
mixer.music.set_volume(0.1)
resolution = (400, 300)
screen = pygame.display.set_mode(resolution, pygame.locals.RESIZABLE | pygame.locals.SCALED)
pygame.display.set_caption('iodine')
clock = pygame.time.Clock()
font = pygame.freetype.Font('font.ttf', 15)

enemy_image = pygame.image.load("enemy0.png").convert_alpha()
explosion_image = pygame.image.load("explosion_spritetheet.png").convert_alpha()
shot_image = pygame.image.load("shots0.png").convert_alpha()
background_image = pygame.image.load("sky.gif").convert_alpha()
background_layers = [pygame.Surface((resolution[0] * 2, resolution[1] * 2), pygame.SRCALPHA) for _ in range(5)]
generate_background()
powerup_image = pygame.image.load('powerup2.png').convert_alpha()
powershot_image = pygame.image.load('pwr_shot.png').convert_alpha()
heart_image = pygame.image.load('heart.png').convert_alpha()
player_ani = deque(
    [pygame.image.load('player_ani1.png').convert_alpha(), pygame.image.load('player_ani2.png').convert_alpha()])
player_image = pygame.image.load("player1.png").convert_alpha()
player_image_left = pygame.image.load("pixil-frame-0 (5).png").convert_alpha()
player_image_right = pygame.image.load("player_image_right3.png").convert_alpha()

FPS = 60
player_x, player_y = (200, 260)
delta_x = 0
delta_y = 0

shots = list()
shot_radius = 6
shot_speed = 80 / FPS
fire_rate = 0.8 * FPS  # cislo znaci, jak dlouha je prodleva mezi strelami ve vterinach
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
explosions = list()

player_lives = 3
number_of_enemies = 1
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
