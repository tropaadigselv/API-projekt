import requests
import pygame
from pygame.locals import *



pygame.init()
width = 800
height = 400

clock=pygame.time.Clock()


screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Fly kort')


class planes:
    #def __init__(self,):
    print("hej")

class Map:
    def __init__(self, x,y):
        self.x=x
        self.y=y
        self.kort=pygame.image.load("map.png")
        self.kort.convert()
        self.moving = False
        self.rect=self.kort.get_rect()
        self.rect.center=width//2,height//2
    
    def show(self):
        screen.blit(self.kort,self.rect)

    def move(self):
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
            if event.type==MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.moving= True
            elif event.type == MOUSEBUTTONUP:
                self.moving=False
            
            if event.type== MOUSEMOTION and self.moving:
                self.rect.move_ip(event.rel)



    

def setup():
    global kort
    kort =Map(0,0)
    params = {
        'access_key': '5b9995494934e5feef1829d04ddbf000',
        'limit':100,
        'offset':0,
        'flight_status':'active'
    }
    #api_result = requests.get('http://api.aviationstack.com/v1/flights', params)

    #api_response = api_result.json()
    #print(api_response)


def draw():
    global kort
    clock.tick(60)
    screen.fill((200, 200, 200))
    kort.show()
    kort.move()

    pygame.display.update()



setup()

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    draw()  

pygame.quit()