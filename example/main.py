import pygame, os, sqlite3, random
from datetime import *

HEIGHT = 750
WIDTH = 1000
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

BG = pygame.image.load(os.path.join("assets", "BG.png"))
BOX1 = pygame.image.load(os.path.join("assets", "box1.png"))
APPLE = pygame.image.load(os.path.join("assets", "apple.png"))


class Player():
    def __init__(self, xpos, ypos, image):
        self.xpos = xpos
        self.ypos = ypos
        self.img = image
        self.mask = pygame.mask.from_surface(self.img)
        self.scrambleColour()

    def scrambleColour(self):
        self.colour = randomColour()

    def draw(self, window):
        window.blit(self.img, (self.xpos, self.ypos))

    def collision(self, obj):
        return collide(self, obj)

    def get_height(self):
        return self.img.get_height()
    def get_width(self):
        return self.img.get_width()


class plants(Player):
    def __init__(self, xpos, ypos):
        self.xpos = xpos
        self.ypos = ypos
        self.img = APPLE
        self.mask = pygame.mask.from_surface(self.img)



def collide(obj1, obj2):
    offset_x = obj2.xpos - obj1.xpos
    offset_y = obj2.ypos - obj1.ypos
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None


def randomColour():
    return(random.randint(0,255),random.randint(0,255),random.randint(0,255))




def main():
    run = True
    FPS = 60

    player = Player(0, 0, BOX1)
    rectangle1 = pygame.Rect(0,0,player.img.get_width(),player.img.get_height())

    plantList = []
    for x in range(20):
        plantList.append(plants(random.randint(0,WIDTH), random.randint(0,HEIGHT)))

    clock = pygame.time.Clock()

    player_vel = 10

    def redraw_window():
        WIN.blit(BG, (0,0))

        pygame.draw.rect(WIN, randomColour(), pygame.Rect(0,0,WIDTH,HEIGHT))

        #player.draw(WIN)

        for plant in plantList:
            plant.draw(WIN)

        pygame.draw.rect(WIN, player.colour, rectangle1)
        pygame.display.update()

    while run == True:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.xpos - player_vel >= 0: # left
            player.xpos -= player_vel
        if keys[pygame.K_d] and player.xpos + player_vel + player.get_width() <= WIDTH: # right
            player.xpos += player_vel
        if keys[pygame.K_w] and player.ypos - player_vel >= 0: # up
            player.ypos -= player_vel
        if keys[pygame.K_s] and player.ypos + player_vel + player.get_height() <= HEIGHT: # down
            player.ypos += player_vel

        #move rectangle around
        rectangle1.left = player.xpos
        rectangle1.top = player.ypos

        for plant in plantList:
            if player.collision(plant):
                plantList.remove(plant)
                del plant
                player_vel+=1
        if plantList == []:
            run = False

        player.scrambleColour()

        redraw_window()



main()

pygame.quit()
