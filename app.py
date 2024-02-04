import requests
import pygame
from pygame.locals import *

# todo

pygame.init()
width = 800
height = 400

clock=pygame.time.Clock()


screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Fly kort')


class planes:
    #def __init__(self,):
    print("hej")

def setup():
    params = {
        'access_key': 'ebb80138fa2c9bdc82579ee04ad114d8',
        #'limit':100,
        #'offset':0,
        #'flight_status':'active'
    }
    api_result = requests.get('http://api.aviationstack.com/v1/flights', params)

    api_response = api_result.json()
    print(api_response)


def draw():
    clock.tick(60)
    screen.fill((200, 200, 200))
    pygame.display.update()



setup()

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    draw()  

pygame.quit()