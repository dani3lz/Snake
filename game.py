import pygame
from random import randrange

def moveSnake(direct,x,y):
    if direct == "down":
        y+=size
    elif direct == "up":
        y-=size
    elif  direct == "left":
        x-=size
    elif direct == "right":
        x+=size
    elif direct == "none":
        pass
    return x,y

def collisionSnake(snake,lengthSnake):
    for x in range(2,lengthSnake):
        if snake[-1] == snake[-x]:
            return True
    return False

def checkApple(snake,lengthSnake):
    while True:
        check = True
        x = randrange(40,960,size)
        y = randrange(160,760,size)
        for i in range(1,lengthSnake):
            if (x,y) == snake[-i]:
                check = False
        if check:
            return x,y

def checkVolume(volume):
    if volume == 1:
        for i in range(785,906,30):
            displayOfGame.blit(volumeScale,(i,42))
    if volume < 1 and volume >= 0.8:
        for i in range(815,906,30):
            displayOfGame.blit(volumeScale,(i,42))
    if volume < 0.8 and volume >= 0.6:
        for i in range(845,906,30):
            displayOfGame.blit(volumeScale,(i,42))
    if volume < 0.6 and volume >= 0.4:
        for i in range(875,906,30):
            displayOfGame.blit(volumeScale,(i,42))
    if volume < 0.4 and volume > 0:
        for i in range(905,906,30):
            displayOfGame.blit(volumeScale,(i,42))

def settingsInit():
    check = 0
    with open("settings.txt", mode="r") as settingsFile:
        for row in settingsFile:
            for word in row.split():
                if word == "Volume":
                    for part in row.split():
                        check+=1
                        if check == 3:
                            return float(part)
    return 0

def settingsCheck():
    with open("settings.txt", mode="w+") as settingsFile:
        settingsFile.writelines("Volume = " + str(volume))

pygame.init()
Height = 800
Width = 1000
volume = settingsInit()
displayOfGame = pygame.display.set_mode((Width,Height))
nameOfDisplay = pygame.display.set_caption("Snake by dani3lz")
programIcon = pygame.image.load("img//icon.png")
volumeUp = pygame.image.load("img//vol+.png")
volumeDown = pygame.image.load("img//vol-.png")
volumeScale = pygame.image.load("img//volscale.png")
pygame.display.set_icon(programIcon)
font = pygame.font.Font("fonts//snakefont.otf", 80)
fontsmall = pygame.font.Font("fonts//snakefont.otf", 40)
fontsmall2 = pygame.font.Font("fonts//snakefont.otf", 20)
loseText = font.render("You Lose!", (0,0,0), (255,0,0))
tryAgain = fontsmall.render("Try Again?", (0,0,0), (255,255,255))
start = fontsmall2.render("START -> SPACE", (0,0,0), (192,192,192))
exit = fontsmall2.render("EXIT -> ESC", (0,0,0), (192,192,192))
run = True
FPS = 5
fpsClock = pygame.time.Clock()
pygame.mixer.music.load("sounds//background.wav")
pygame.mixer.music.set_volume(volume)
pygame.mixer.music.play(-1)

Upper = 120
size = 20

# Snake
x = randrange(40,960,size)
y = randrange(160,760,size)
lengthSnake = 1
snake = []

#Apple
x1 = randrange(40,960,size)
y1 = randrange(160,760,size)

direct = "none"
scorePlayer = 0

while run:
    fpsClock.tick(FPS)
    mx,my = pygame.mouse.get_pos()
    mouse = [mx,my]
    for event in pygame.event.get():
        if event.type == pygame.QUIT: run = False
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_DOWN or event.key == pygame.K_s) and directSaved != "up" and direct != "down":
                direct = "down"
            if (event.key == pygame.K_UP or event.key == pygame.K_w) and directSaved != "down" and direct != "up":
                direct = "up"
            if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and directSaved != "right" and direct != "left":
                direct = "left"
            if (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and directSaved != "left" and direct != "right":
                direct = "right"
            if event.key == pygame.K_ESCAPE:
                run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if (mouse[0] >= 751 and mouse[0] <= 781) and (mouse[1] >= 40 and mouse[1] <= 70):
                if event.button == 1:
                    if volume < 1:
                        volume+= 0.1
                        volume = round(volume,1)
                        settingsCheck()
                        pygame.mixer.music.set_volume(volume)
            elif (mouse[0] >= 935 and mouse[0] <= 965) and (mouse[1] >= 40 and mouse[1] <= 70):
                if event.button == 1:
                    if volume > 0:
                        volume-= 0.1
                        volume = round(volume,1)
                        settingsCheck()
                        pygame.mixer.music.set_volume(volume)

    directSaved = direct
    scoreStr = "Score: " + str(scorePlayer)
    scoreText = font.render(scoreStr, (0,0,0), (255,255,255))
    x,y = moveSnake(direct,x,y)
    snake.append((x,y))
    snake = snake[-lengthSnake:]
    displayOfGame.fill((0,0,0))
    #BorderUp
    pygame.draw.rect(displayOfGame, (0,0,255),(0,Upper,Width,size))
    #BorderLeft
    pygame.draw.rect(displayOfGame, (0,0,255),(0,Upper,size,Height-Upper))
    #BorderDown
    pygame.draw.rect(displayOfGame, (0,0,255),(0,Height-size,Width,size))
    #BorderRight
    pygame.draw.rect(displayOfGame, (0,0,255),(Width-size,Upper,size,Height-Upper))
    #Apple
    pygame.draw.rect(displayOfGame, (255,0,0), (x1,y1,size,size))
    #Snake
    [(pygame.draw.rect(displayOfGame, (0,255,0),(i,j,size,size))) for i, j in snake]
    pygame.draw.rect(displayOfGame, (0,115,0),(x,y,size,size))
    #BorderText
    bordertext = pygame.draw.rect(displayOfGame, (0,0,0),(0,0,Width,Upper))
    #Grid
    [pygame.draw.line(displayOfGame, pygame.Color('dimgray'), (x,140), (x,Height-20)) for x in range (20,Width,size)]
    [pygame.draw.line(displayOfGame, pygame.Color('dimgray'), (20,y), (Width-20,y)) for y in range (140,Height,size)]

    if snake[-1] == (x1,y1):
        scorePlayer+=1
        lengthSnake+=1
        x1,y1 = checkApple(snake,lengthSnake)
        FPS+=0.1

    if x < 20 or x > 960 or y < 140 or y > 760 or collisionSnake(snake,lengthSnake):
        pygame.mixer.music.stop()
        pygame.mixer.music.load("sounds//fail.wav")
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play()
        scoreStr = "Score: " + str(scorePlayer)
        scoreText = fontsmall.render(scoreStr, True, (255,255,255))
        direct = "none"
        displayOfGame.blit(loseText, (30,10))
        displayOfGame.blit(tryAgain, (470,15))
        displayOfGame.blit(scoreText, (470,55))
        displayOfGame.blit(start, (800, 40))
        displayOfGame.blit(exit, (800, 60))
        pygame.display.update()
        snake = snake.clear()
        lengthSnake = 1
        lose = True
        while lose:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    lose = False
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        lose = False
                        run = False
                    if event.key == pygame.K_SPACE:
                        pygame.mixer.music.load("sounds//background.wav")
                        pygame.mixer.music.set_volume(volume)
                        pygame.mixer.music.play(-1)
                        FPS = 5
                        lose = False
                        snake = []
                        x = randrange(40,960,size)
                        y = randrange(160,760,size)
                        x1 = randrange(40,960,size)
                        y1 = randrange(160,760,size)
                        scorePlayer = 0

    if run:
        displayOfGame.blit(scoreText, (30,10))
        #VolumeInfo
        infoscale = "Volume: " + str(round(volume*100))
        volumeInfo = fontsmall2.render(infoscale, (0,0,0), (192,192,192))
        displayOfGame.blit(volumeInfo,(805,70))
        #volumeOn
        displayOfGame.blit(volumeUp,(751,40))
        #volumeScale
        checkVolume(volume)
        #volumeOff
        displayOfGame.blit(volumeDown,(935,40))
    pygame.display.update()

pygame.quit()
