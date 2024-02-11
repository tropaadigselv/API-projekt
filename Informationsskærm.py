import requests
import pygame
from pygame.locals import *
from io import BytesIO

pygame.init()

#globale variabler
width = 1200
height = 600
writing = False
status = "start"


clock=pygame.time.Clock()

#laver skærmen
screen = pygame.display.set_mode((width, height))
screen_rect = screen.get_rect()


pygame.display.set_caption('Fly afgange')

#font til tekst
font= pygame.font.SysFont("Arial",18)

#tekst
class text():
    def __init__(self,text):
        self.text=text
    #laver og viser tekst
    def show(self,x,y):
        surface=font.render(self.text,True,(0,0,0))
        screen.blit(surface,(x,y))

#ændre skærmene
def change(text):
    global planes, status
    loading_screen()
    planes = getPlanes(text)
    status= "main"

# Objekter der viser forskellige fly og henter logos til dem
class plane():
    def __init__(self,flight):
        self.flight=flight
        self.airline=self.flight['airline']
        self.departure=self.flight['departure']
        self.arrival=self.flight['arrival']
        self.nr=self.flight['flight']['iata']
        self.logo
    #for tide for flyet
    def get_time(self):
        a=str(self.departure['scheduled']).split("T")
        b=a[0].split("-")
        c=(b[2],b[1],b[0])
        year="-".join(c)
        time=a[1].split("+")
        return(year,time[0])

    #viser fly information 
    def show(self,y):
        t=f"Fly {self.nr} ({self.airline['name']}) fra {self.departure['airport']} til {self.arrival['airport']} flyver fra gate {self.departure['gate']} terminal {self.departure['terminal']} klokken {self.get_time()[1]} {self.get_time()[0]}"
        a=text(t)
        a.show(10,y)
    #henter logo med api ninjas
    def logo(self):
        name = self.airline['name']
        api_url = 'https://api.api-ninjas.com/v1/airlines?name={}'.format(name)
        result = requests.get(api_url, headers={'X-Api-Key': 'POvaQ7/3DwkLtXHxaMV9mA==d9RHRAfTSp2igfmP'}) # Indsæt din egen key her
        response = result.json()
    #laver det om til et billede
        try:
            a=response[0]['logo_url']
            b=requests.get(a)
            self.logo=pygame.image.load(BytesIO(b.content))
            self.logo=pygame.transform.rotozoom(self.logo,0,0.5)
        except:
            self.logo=pygame.image.load("API projekt\API-projekt\plane_icon.png")
            self.logo=pygame.transform.rotozoom(self.logo,0,0.1)
    #viser logo
    def show_logo(self,y):
        screen.blit(self.logo,(1100,y))

#knap
class button():
    def __init__(self):
        self.rect=Rect(700,30,70,30)
    #tegner knap
    def show(self):
        pygame.draw.rect(screen,(255,255,255),self.rect)
        t="Bekræft"
        a=text(t)
        a.show(710,30)

    #hvad der sker når den klikkes på
    def click(self):
        text= text_inp.text
        change(text)

# tekst input
class textInput():
    def __init__(self):
        self.text=""
        self.rect=Rect(100,30,500,30)
    # hvser tekst input boks 
    def show(self):
        pygame.draw.rect(screen,(255,255,255),self.rect)
        pygame.draw.rect(screen,(0,0,0),self.rect,1)
        text_surface=font.render(self.text,True,(0,0,0))
        screen.blit(text_surface,(110,30))
    # gør så man kan skrive i den
    def write(self,event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text+=event.unicode

# hvis der ikke er nogel fly kaldes den
def sorry():
    t="Undskyld men der kunne ikke findes nogle fly, prøv at genstarte programmet og ændre på 'limit' eller 'offset' i params i setup()"
    a=text(t)
    a.show(10,height//2)

#henter fly fra aviationstack api
def getPlanes(text):
    a=[]
    params = {
    'access_key': '5b9995494934e5feef1829d04ddbf000', # Indsæt din egen key her
    'limit':50,
    'offset':100,
    'airline_name':text
    }
    api_result = requests.get('http://api.aviationstack.com/v1/flights', params)

    api_response = api_result.json()
    for flight in api_response['data']:
        if flight['airline']['name'] == None or flight['departure']['gate'] == None or flight['departure']['terminal']== None:
            pass
        else:
            a.append(plane(flight))
    if len(a) >12:
        for i in range(len(a)-12):
            a.pop()
    for i in range(len(a)):
        a[i].logo()
    return a

#laver knap og text input
def setup():
    global planes, button, text_inp, writing
    writing = False
    button=button()
    text_inp=textInput()

#start skærm med knap og tekst input
def start_screen():
    global writing
    screen.fill((150,210,250))
    info = "Skriv flyselskab du vil se afgange for, du kan også bare klikke bekræft uden noget og se for alle flyselskaber"
    a=text(info)
    a.show(100,5)
    button.show()   
    text_inp.show()
    w0= "Knapperne og Tekst feltet er virker måske ikke altid, klik først på tekst feltet for at skrive"
    w1= "Hvis der ikke kommer nogle bogstaver frem efter et par klik på tasterne så klik på feltet igen"
    w2= "Hvis der så kommer tekst skal du være opmærksom på at den ikke altid læser dit indput så være"
    w3= "tåldmodig mens du skriver."
    w4= "Knappen kan du bare spam klikke for at få til at virke"
    y=100
    q=[]
    q.append(w0),q.append(w1),q.append(w2),q.append(w3),q.append(w4)
    e=[]
    for i in range(len(q)):
        e.append(text(q[i]))
    for i in range(len(e)):
        e[i].show(100,y)
        y+=20

    #tjekker om der klikkes på knap eller tekst input
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            #kalder knappen
            if button.rect.collidepoint(event.pos):
                button.click()
                writing = False
            elif text_inp.rect.collidepoint(event.pos):
                writing = True
            else:
                writing = False
        # kalder textInput hvis der er blevet klikket på den
        if writing:
            text_inp.write(event)

    
    pygame.display.flip()

#viser information for fly
def main_screen():

    screen.fill((150, 210, 250))
    y=0
    for i in range(int(height/50)):
        pygame.draw.line(screen,(0,0,0),(0,y),(width,y))
        y=y+50
    y=10
    for i in range(len(planes)):
        planes[i].show(y)
        planes[i].show_logo(y)
        y=y+50

    if len(planes)==0:
        sorry()
    pygame.display.flip()

#loading skærm når fly og logos hentes
def loading_screen():
    screen.fill((150,210,250))
    load = "Henter fly og logos til fly"
    a=text(load)
    a.show(width//2-100,height//2)
    pygame.display.flip()


setup()

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
    #bestmmer hviken skærm der vises
    if status == "start":
        start_screen()
    elif status == "main":
        main_screen()

pygame.quit()