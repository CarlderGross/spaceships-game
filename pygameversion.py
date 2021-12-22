import sys, pygame
pygame.init()

## DEFINE COLORS ##
black = [0, 0, 0]
purple = [128, 0, 128]
green = [0, 128, 0]
white = [255, 255, 255]

## INITIALIZE GLOBAL VARIABLES ##
screen = pygame.display.set_mode((400, 400))

class Ship(pygame.sprite.Sprite):
    
    def __init__(self, color, x, y):
        #call parent class constructor
        pygame.sprite.Sprite.__init__(self)
        width = 10
        height = 15
        
        self.image = pygame.Surface([width, height]) #the spaceship is 10 units wide and 15 units tall
        self.image.fill(white)
        self.body = pygame.draw.polygon(self.image, color, [[5, 0], [0, 15], [10, 15]]) #draws a polygon for the ship
        self.rect = pygame.Rect(x - width/2, y-height/2, width, height) #this is the reference rect for the image
        #self.delta = [0, 1]
        
#make a spaceship colored purple at (200, 200)
ship1 = Ship(purple, 200, 200)

## RENDER LOOP ##
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            sys.exit()
            #If pygame gets a quit command, this shuts the game down cleanly
    
    #move the ship
    #ship1.body = ship1.body.move(ship1.delta)
    
    screen.fill(white)
    screen.blit(ship1.image, ship1.rect)
    pygame.display.flip() #flip the buffer, to display the new drawings on the screen