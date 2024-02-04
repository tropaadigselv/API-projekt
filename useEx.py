import requests
import pygame
from pygame.locals import *



width = 800
height = 400

clock=pygame.time.Clock()

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Fly kort')



def setup():
    global api_response
    A=[[]]
    i=0
    params = {
    'access_key': '5b9995494934e5feef1829d04ddbf000',
    'limit':100,
    'offset':0,
    'flight_status':'active'
    }
    api_result = requests.get('http://api.aviationstack.com/v1/flights', params)

    api_response = api_result.json()
    print(api_response)
    for flight in api_response['data']:
            print(u'%s flight %s from %s (%s) to %s (%s) is in the air. coordinates are: lati = %s and long = %s' % (
                A[i][0],
                A[i][1],
                flight['departure']['airport'],
                flight['departure']['iata'],
                flight['arrival']['airport'],
                flight['arrival']['iata'],
                A[i][2],
                A[i][3]))
            i=i+1
    print(A)


def draw():
    clock.tick(60)

#print(api_response)



setup()

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    draw()  

pygame.quit()