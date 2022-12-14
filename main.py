import pygame, sys
import math
from pygame.locals import QUIT, KEYDOWN, KEYUP, K_LEFT, K_RIGHT, K_SPACE
import random


def distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    c = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
    return c

def reset_enemy(enemy):
    enemy[0] = random.randint(0, resolution[0])
    enemy[1] -= resolution[1]
    
# inicializace (pocatecni nastaveni, spusteni)
pygame.init()
resolution = (400, 300)
screen = pygame.display.set_mode(resolution)
pygame.display.set_caption('Circle game')
clock = pygame.time.Clock()
font = pygame.freetype.Font('font.ttf', 15)
score = 0


# music/sounds
music = pygame.mixer.music.load('music.mp3')
pygame.mixer.music.play(-1)

FPS = 60
player_x, player_y = (200, 260)
delta_x = 0
delta_y = 0

shots = list()
shot_radius = 6
shot_speed = 80 / FPS

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

# herni smycka
running = True
while running:

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
            elif event.key == K_SPACE:
                shots.append([player_x, player_y])
                print(len(shots))
        elif event.type == KEYUP:
            if event.key == K_LEFT:
                #klavesa uvolnena
                # print("< rel")
                if player_x > 0:
                    delta_x += player_speed
            elif event.key == K_RIGHT:
                # print("> rel")
                if player_x < resolution[0]:
                    delta_x -= player_speed

    player_x += delta_x
    # y += delta_y

    #      pravy okraj          levy okraj
    if player_x > resolution[0] or player_x < 0:
        delta_x = 0

    #      spodni okraj         horni okraj
    if player_y > resolution[1] or player_y < 0:
        # delta_y = delta_y * -1
        delta_y *= -1

    # renderovani
    screen.fill((112, 64, 207))

    # draw.circle(kam, jakou barvou, souradnice stredu, polomer)
    pygame.draw.circle(screen, (random.randint(25, 35), random.randint(
        60, 68), random.randint(200, 210)), (player_x, player_y),
                       player_radius)

    # for index in [0, 1, 2]:
    #     enemies[index] [1] += enemy_speed

    # for index, enemy in enumerate(enemies):
    #     enemies[index][1] += enemy_speed
    #     enemy[1] += enemy_speed

    shots_to_remove = list()
    
    # render enemies
    for enemy in enemies:
        # enemy[0], enemy[1]  <- enemy: List              enemy = [20, 30]
        # enemy["x"], enemy["y"] <- enemy: Dictionary     enemy = {"x": 20, "y": 30}
        # enemy.x, enemy.y <- enemy: Class
        # print(enemy[1])

        # enemy[1] = enemy[1] + enemy_speed
        enemy[1] += enemy_speed

        for shot in shots:
            if distance(shot, enemy) <= shot_radius + enemy_radius:
                reset_enemy(enemy)
                shots_to_remove.append(shot)
        c = distance([player_x, player_y], enemy)
        if c <= player_radius + enemy_radius:  # <-- doslo ke kolizi
            player_lives -= 1
            print(player_lives)
            reset_enemy(enemy)
        if player_lives == 0:
            running = False
        if enemy[1] >= resolution[1]:
            reset_enemy(enemy)
            score += 1

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

        pygame.draw.circle(screen, (71, 179, 191), enemy, enemy_radius)

    for shot in shots:
        if shot[1] <= 0:
            shots_to_remove.append(shot)
        else:
            shot[1] -= shot_speed
        pygame.draw.circle(screen, (255, 255, 255), shot, shot_radius)
        
    for shot in shots_to_remove:
        shots.remove(shot)
    
    for life in range(player_lives):
        pygame.draw.circle(screen, (255, 0, 0), (30 + life * 20, 30), 8)

    font.render_to(screen, (240, 20), str(score).zfill(6), (224, 234, 255))
    pygame.display.update()
    clock.tick(FPS)
