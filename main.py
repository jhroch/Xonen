import pygame
import random
import math
from pygame import mixer
import os
from datetime import datetime

# Initialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

fullscreen = False


# Images
pygame.display.set_caption("Rozla Smash")
icon = pygame.image.load("C:/Users/PC/PycharmProjects/SpaceInvader/data/ufo.png")
pygame.display.set_icon(icon)
rightarrowkey = pygame.image.load("C:/Users/PC/PycharmProjects/SpaceInvader/data/rightarrow1.png")
leftarrowkey = pygame.image.load("C:/Users/PC/PycharmProjects/SpaceInvader/data/leftarrow1.png")
akey = pygame.image.load("C:/Users/PC/PycharmProjects/SpaceInvader/data/akey.png")
dkey = pygame.image.load("C:/Users/PC/PycharmProjects/SpaceInvader/data/dkey.png")
pkey = pygame.image.load("C:/Users/PC/PycharmProjects/SpaceInvader/data/pkey.png")
spacebar = pygame.image.load("C:/Users/PC/PycharmProjects/SpaceInvader/data/spacebar.png")
unmutePhoto = pygame.image.load("C:/Users/PC/PycharmProjects/SpaceInvader/data/speaker.png")
mutePhoto = pygame.image.load("C:/Users/PC/PycharmProjects/SpaceInvader/data/mute.png")
unmutePhotow = pygame.image.load("C:/Users/PC/PycharmProjects/SpaceInvader/data/speakerw.png")
mutePhotow = pygame.image.load("C:/Users/PC/PycharmProjects/SpaceInvader/data/mutew.png")
playerImg = pygame.image.load("C:/Users/PC/PycharmProjects/SpaceInvader/data/player.png")
bulletImg = pygame.image.load("C:/Users/PC/PycharmProjects/SpaceInvader/data/bullet.png")
speakerless = pygame.image.load("C:/Users/PC/PycharmProjects/SpaceInvader/data/speakerless.png")
speakerlessw = pygame.image.load("C:/Users/PC/PycharmProjects/SpaceInvader/data/speakerlessw.png")
pauseimg = pygame.image.load("C:/Users/PC/PycharmProjects/SpaceInvader/data/pause.png")
fullscreenimg = pygame.image.load("C:/Users/PC/PycharmProjects/SpaceInvader/data/fullscreenimg.png")

# Background Image
background = pygame.image.load("C:/Users/PC/PycharmProjects/SpaceInvader/data/background1.jpg")

# Background sound

pygame.mixer.music.load("C:/Users/PC/PycharmProjects/SpaceInvader/data/theme1.wav")
pygame.mixer.music.play(-1)

# time
now = datetime.now()
rok = now.year
mesic = str(now.month)
den = str(now.day)
hodina = str(now.hour)
minuta = str(now.minute)
cas = (
    f"{hodina.zfill(2)}:{minuta.zfill(2)} {den.zfill(2)}.{mesic.zfill(2)}.{rok}\n")


volumechange = True
volumehalf = False

def volumemute():
    global volumechange
    global volumehalf
    volumechange = False
    pygame.mixer.music.pause()
    volumehalf = False


def volumeunmute():
    global volumechange
    global volumehalf
    volumechange = True
    pygame.mixer.music.unpause()
    pygame.mixer.music.set_volume(1)
    volumehalf = False



def volumeless():
    global volumehalf
    pygame.mixer.music.unpause()
    pygame.mixer.music.set_volume(0.3)
    volumehalf = True






# Player
playerImg = pygame.transform.scale(playerImg, (60, 60))
playerX = 370
playerY = 480
playerX_change = 0

# Game Over text
over_font = pygame.font.Font("freesansbold.ttf", 70)


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (180, 250))


# Enemies
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
basic_enemies = 6
chosen_enemies = 0


num_of_enemies = 6


for i in range(num_of_enemies + chosen_enemies):
    enemyImg.append(pygame.image.load("C:/Users/PC/PycharmProjects/SpaceInvader/data/enemy69.png"))
    enemyImg.append(pygame.image.load("C:/Users/PC/PycharmProjects/SpaceInvader/data/enemy31.png"))
    enemyX.append(random.randint(20, 730))
    enemyY.append(random.randint(50, 150))
    enemyY_change.append(80)
    enemyX_change.append(2)

# Bullet
# Ready - no bullet on the screen
# Fire - bullet is fired

bulletImg = pygame.transform.scale(bulletImg, (40, 40))
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 5
bullet_state = "ready"

# Other
score_value = 0

clock = pygame.time.Clock()

pause = False

# Font

font = pygame.font.SysFont("comicsansms", 35)


def player1(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 10, y + 10))


def is_collision(enemyX, enemyY, bulletX, bulletY):
    distance = math.hypot(enemyX - bulletX, enemyY - bulletY)
    if distance < 60:
        return True
    else:
        return False


def text_objects(text, font):
    textSurface = font.render(text, True, (0, 0, 0))
    return textSurface, textSurface.get_rect()


def text_objectsw(text, font):
    textSurface = font.render(text, True, (255, 255, 255))
    return textSurface, textSurface.get_rect()


def buttonxd(c, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if 750 + 32 > mouse[0] > 750 and 10 + 32 > mouse[1] > 10:
        pygame.draw.rect(screen, c, (749, 9, 34, 34), 1)
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(screen, c, (749, 9, 34, 34), 1)
    smallText = pygame.font.SysFont("comicsansms", 20)
    textSurf, textRect = text_objects("", smallText)
    textRect.center = ((700 + (32 / 2)), (20 + (32 / 2)))
    screen.blit(textSurf, textRect)


def button(msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, ac, (x, y, w, h))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(screen, ic, (x, y, w, h))
    smallText = pygame.font.SysFont("comicsansms", 20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    screen.blit(textSurf, textRect)


def fullscreenbutton():
    global screen
    global fullscreen
    fullscreen = not fullscreen
    if fullscreen:
        screen = pygame.display.set_mode((screen.get_width(), screen.get_height()), pygame.FULLSCREEN)
        pygame.display.update()
    else:
        screen = pygame.display.set_mode((screen.get_width(), screen.get_height()))
        pygame.display.update()


def quitgame():
    pygame.quit()
    quit()
    exit()


def game_intro():
    intro = True
    global screen
    pygame.mixer.music.set_volume(1)

    while intro:
        screen.fill((255, 255, 255))

        largeText = pygame.font.SysFont("comicsansms", 100)
        TextSurf, TextRect = text_objects("Rozla Smash", largeText)
        TextRect.center = ((800 / 2), 200)
        screen.blit(TextSurf, TextRect)

        button("Play", 150, 450, 100, 50, (0, 255, 0), (0, 150, 0), game_loop)
        button("Quit", 550, 450, 100, 50, (255, 0, 0), (150, 0, 0), quitgame)
        button("Controls", 350, 450, 100, 50, (0, 0, 255), (0, 0, 150), settings)
        button("", 10, 20, 66, 66, (255, 255, 255), (255, 255, 255), volumemute)
        button("", 160, 20, 66, 66, (255, 255, 255), (255, 255, 255), volumeunmute)
        button("", 90, 20, 66, 66, (255, 255, 255), (255, 255, 255), volumeless)

        screen.blit(mutePhoto, (10, 20))
        screen.blit(unmutePhoto, (160, 20))
        screen.blit(speakerless, (90, 20))
        screen.blit(fullscreenimg, (750, 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        buttonxd((255,255,255),fullscreenbutton)


        pygame.display.update()



def unpause():
    game_loop()


def paused():
    #screen.fill((255, 255, 255))
    largeText = pygame.font.SysFont("freesansbold", 115)
    TextSurf, TextRect = text_objectsw("PAUSED", largeText)
    TextRect.center = (400, 200)
    screen.blit(TextSurf, TextRect)

    pause = True

    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause = False

        button("Continue", 150, 450, 100, 50, (0, 255, 0), (0, 150, 0), unpause)
        button("Quit", 550, 450, 100, 50, (255, 0, 0), (150, 0, 0), quitgame)

        button("", 10, 20, 66, 66, (0, 0, 0), (0, 0, 0), volumemute)
        button("", 160, 20, 66, 66, (0, 0, 0), (0, 0, 0), volumeunmute)
        button("", 90, 20, 66, 66, (0, 0, 0), (0, 0, 0), volumeless)

        screen.blit(mutePhotow, (10, 20))
        screen.blit(unmutePhotow, (160, 20))
        screen.blit(speakerlessw, (90, 20))

        pygame.display.update()
        clock.tick(15)


def openscore():
    os.system("start C:/Users/PC/PycharmProjects/SpaceInvader/score.txt")


def resetscore():
    filo = open("score.txt", "w")
    filo.write(f"last reset in {cas}")
    filo.close()


def gameover():
    screen.fill((255, 255, 255))
    largeText = pygame.font.SysFont("freesansbold", 115)
    TextSurf, TextRect = text_objects("GAME OVER", largeText)
    TextRect.center = (400, 200)
    screen.blit(TextSurf, TextRect)
    file = open("score.txt", "a")
    file.write(f"{score_value} in {cas}")
    file.close()

    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        button("Quit", 350, 450, 100, 50, (255, 0, 0), (150, 0, 0), quitgame)
        button("Reset scores", 500, 450, 150, 50, (255, 255, 0), (150, 150, 0), resetscore)
        button("Open scores", 150, 450, 150, 50, (0, 0, 255), (0, 0, 150), openscore)
        score = font.render("Score: " + str(score_value), True, (0, 0, 0))
        screen.blit(score, (340, 350))
        pygame.display.update()
    pygame.display.update()


def textos(surf, rect):
    screen.blit(surf, rect)


def settings():
    pygame.mixer.music.set_volume(1)
    screen.fill((255, 255, 255))
    # Texts
    largeText = pygame.font.SysFont("freesansbold", 100)
    settingsText = pygame.font.SysFont("freesansbold", 40)
    TextSurf, TextRect = text_objects("Controls", largeText)
    TextMurf, TextMect = text_objects("Move:          / ", settingsText)
    TextNurf, TextNect = text_objects("Shoot: ", settingsText)
    TextPurf, TextPect = text_objects("Pause: ", settingsText)
    TextRect.center = ((800 / 2), 100)
    TextMect = (290, 300)
    TextNect = (290, 350)
    TextPect = (290, 400)
    textos(TextSurf, TextRect)
    textos(TextMurf, TextMect)
    textos(TextNurf, TextNect)
    textos(TextPurf, TextPect)
    screen.blit(rightarrowkey, (505, 298))
    screen.blit(leftarrowkey, (465, 298))
    screen.blit(akey, (373, 298))
    screen.blit(dkey, (410, 298))
    screen.blit(pkey, (385, 400))
    screen.blit(spacebar, (390, 350))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        button("Back", 600, 500, 100, 50, (255, 255, 0), (230, 230, 0), game_intro)

        pygame.display.update()


def game_loop():
    global playerX
    global playerX_change
    global bulletX
    global bulletY
    global bullet_state
    global score_value
    global pause
    clock = pygame.time.Clock()
    clock.tick(60)

    running = True
    while running:

        # Color
        screen.fill((0, 0, 0))
        # Background Image
        screen.blit(background, (0, 0))

        button("", 730, 20, 50, 50, (0, 0, 0), (0, 0, 0), paused)
        screen.blit(pauseimg, (728, 20))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitgame()
            # Player movement
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerX_change -= 2
                elif event.key == pygame.K_a:
                    playerX_change -= 2
                elif event.key == pygame.K_RIGHT:
                    playerX_change += 2
                elif event.key == pygame.K_d:
                    playerX_change += 2
                elif event.key == pygame.K_p:
                    paused()
                # Bullet
                elif event.key == pygame.K_SPACE:
                    if bullet_state is "ready":
                        if volumechange:
                            laser_Sound = mixer.Sound("C:/Users/PC/PycharmProjects/SpaceInvader/data/laser.wav")
                            laser_Sound.play()
                            if volumehalf:
                                laser_Sound.set_volume(0.3)

                        bulletX = playerX
                        fire_bullet(playerX, bulletY)
                elif event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0
                elif event.key == pygame.K_a or event.key == pygame.K_d:
                    playerX_change = 0

        playerX += playerX_change

        # Edge block
        if playerX <= playerX_change:
            playerX = 0.1
        elif playerX >= 740:
            playerX = 739.9

        # Line
        pygame.draw.line(screen, (255, 255, 255), [0, 460], [50, 460], 3)
        pygame.draw.line(screen, (255, 255, 255), [750, 460], [801, 460], 3)

        # Enemy movement
        for i in range(num_of_enemies):

            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= playerX_change:
                enemyX_change[i] = 2
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 740:
                enemyX_change[i] = -2
                enemyY[i] += enemyY_change[i]

            # Collision
            collision = is_collision(enemyX[i], enemyY[i], bulletX, bulletY)
            if collision:
                if volumechange:
                    explosion_Sound = mixer.Sound("C:/Users/PC/PycharmProjects/SpaceInvader/data/explosion.wav")
                    explosion_Sound.play()
                    if volumehalf:
                        explosion_Sound.set_volume(0.3)
                bulletY = 480
                bullet_state = "ready"
                score_value += 1
                enemyX[i] = random.randint(20, 730)
                enemyY[i] = random.randint(30, 120)

            # Game over
            if enemyY[i] > 365:
                for j in range(num_of_enemies):
                    enemyY[j] = 2000
                pause = True
                gameover()
                break

            enemy(enemyX[i], enemyY[i], i)

        # Bullet movement
        if bulletY <= 0:
            bulletY = 480
            bullet_state = "ready"
        if bullet_state is "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change

        player1(playerX, playerY)

        # Show score

        score = font.render("Score: " + str(score_value), True, (255, 255, 255))
        screen.blit(score, (10, 10))
        pygame.display.update()


game_intro()
game_loop()
