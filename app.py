import requests
import pygame
from pygame.locals import *
import math


pygame.init()
width = 1200
height = 600

clock=pygame.time.Clock()


screen = pygame.display.set_mode((width, height))
screen_rect = screen.get_rect()

surface = pygame.surface.Surface( (width, height) )

pygame.display.set_caption('Fly kort')

def move_all(a):
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
        if event.type == MOUSEBUTTONDOWN:
            if a.rect.collidepoint(event.pos):
                a.moving = True
        if event.type == MOUSEWHEEL:
            if event.y>0:
                a.scale_factor = a.scale_factor + 0.05
            elif event.y<0:
                if a.scale_factor==0 or a.scale_factor==1.3877787807814457e-17:
                    pass
                else:
                    a.scale_factor = a.scale_factor - 0.05
            a.img = pygame.transform.rotozoom(kort.kort,0,a.start_scale+a.scale_factor)
            print(a.start_scale+a.scale_factor)
            a.rect = a.img.get_rect()
            a.rect.center = width//2,height//2
        elif event.type == MOUSEBUTTONUP:
            a.moving=False
        if event.type == MOUSEMOTION and a.moving:
            a.rect.move_ip(event.rel)

class plane:
    def __init__(self,line,nr,fr,to,lat,lng,space):
        self.line=line
        self.nr=nr
        self.fr=fr
        self.to=to
        self.lat=lat
        self.long=lng
        self.space=space
        self.x=600
        self.y=300
        self.start_scale=0.1
        self.img = pygame.image.load("API projekt\API-projekt\plane_icon.png").convert()
        self.img = pygame.transform.rotozoom(self.img,0,self.start_scale)
        self.rect = self.img.get_rect()
        self.rect.center=width//2,height//2
        self.scale_factor = 0

    def show(self):
        screen.blit(self.img,kort.rect)

    def move(self):
        move_all(self)
        #pass

class Map:
    def __init__(self):
        self.kort=pygame.image.load("API projekt\API-projekt\map.png")
        self.kort.convert
        self.start_scale=0.28
        self.img= pygame.transform.rotozoom(self.kort,0,self.start_scale)
        self.moving = False
        self.rect=self.img.get_rect()
        self.rect.center=width//2,height//2
        self.scale_factor = 0
    
    def show(self):
        screen.blit(self.img,self.rect)

    def move(self):
        move_all(self)



    

def setup():
    global kort, planes
    kort =Map()
    planes=[]
    params = {
        'access_key': '5b9995494934e5feef1829d04ddbf000',
        'limit':100,
        'offset':10,
        'flight_status':'active'
    }
    #api_result = requests.get('http://api.aviationstack.com/v1/flights', params)

    #api_response = api_result.json()
    # for flight in api_response['data']:
    #     if flight['live']!=None:
    #         planes.append(plane(flight['airline']['name'],
    #                             flight['flight']['number'],
    #                             flight['departure']['airport'],
    #                             flight['arrival']['airport'],
    #                             flight['live']['latitude'],
    #                             flight['live']['longitude']))
    planes.append(plane(0,0,0,0,0,0,kort.img))
    print(planes)




def draw():
    global kort
    clock.tick(60)
    screen.fill((200, 200, 200))
    kort.show()
    kort.move()
    planes[0].show()   

    #print(pygame.mouse.get_pos())


    pygame.display.flip()



setup()

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    draw()  

pygame.quit()
