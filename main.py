import math
import random as rnd

from cmu_graphics import *

## TODO ##
# make the ships able to shoot each other

## INITIALIZE SHIP 1 ##
ship1 = Polygon(200,190, 195,205, 205,205, fill='purple')

ship1.dx = 0
ship1.dy = 0
ship1.drotate = 0

## INITIALIZE SHIP 2 ##
ship2 = Polygon(200,190, 195,205, 205,205, fill ='green')

ship2.dx = 0
ship2.dy = 0
ship2.drotate = 0

## INITIALIZE GLOBAL VARIABLES ##
#app.stepsPerSecond = 60

ships = Group(ship1, ship2)
shipSpeed = .25
gravity = 10
bulletSpeed = shipSpeed*5

planet = Circle(200, 200, 5, fill='black') #it's a black hole, since the gravity is a point mass

explosions = Group()
bullets = Group()

rnd.seed()

## PLACE THE SHIPS ##
ship1.centerX = 50
ship1.centerY = 200
ship2.centerX = 350
ship2.centerY = 200

def applyGravity():
    global gravity
    #I will note that the gravity is actually a point mass centered on the 'planet' (which is a black hole)
    for ship in ships.children:
        #accelerate the ship 0.25 units/sec towards the planet
        #the angle is found by getting the arc tangent of deltaX and deltaY from ship to planet,
        #because those form a triangle with a being deltay and o being deltax (and h being distance)
        #(Arc tangent is the reverse of tangent, giving an angle based on a ratio)
        
        #I need to use atan2 so that it doesn't divide by 0 when planet and ship centerY are the same
        #instead of taking o/a, it takes o and a as separate arguments
        angle = math.atan2((planet.centerX - ship.centerX), (planet.centerY - ship.centerY))
        
        #sine = x and cosine = y
        #gravity follows an inverse square relationship, so the base gravity is divided by the square of the distance
        gravX = math.sin(angle) * (gravity / math.dist([planet.centerX, planet.centerY], [ship.centerX, ship.centerY])**2)
        gravY = math.cos(angle) * (gravity / math.dist([planet.centerX, planet.centerY], [ship.centerX, ship.centerY])**2)

        ship.dx += gravX
        ship.dy += gravY
    
    for bullet in bullets:
        angle = math.atan2((planet.centerX - bullet.centerX), (planet.centerY - bullet.centerY))
        
        gravX = math.sin(angle) * (gravity / math.dist([planet.centerX, planet.centerY], [bullet.centerX, bullet.centerY])**2)
        gravY = math.cos(angle) * (gravity / math.dist([planet.centerX, planet.centerY], [bullet.centerX, bullet.centerY])**2)

        bullet.dx += gravX
        bullet.dy += gravY

def wrapObjects():
    for ship in ships.children:
        if ship.centerX > 400:
            ship.centerX = 0
        elif ship.centerX < 0:
            ship.centerX = 400
        if ship.centerY > 400:
            ship.centerY = 0
        elif ship.centerY < 0:
            ship.centerY = 400
    
    for bullet in bullets:
        if bullet.centerX > 400:
            bullet.centerX = 0
        elif bullet.centerX < 0:
            bullet.centerX = 400
        if bullet.centerY > 400:
            bullet.centerY = 0
        elif bullet.centerY < 0:
            bullet.centerY = 400

def explosion(x, y, radius):
    boom = Star(x, y, radius, rnd.randint(8, 16), fill='yellow')
    boom.time = 10
    explosions.add(boom)

def destroyShip(ship):
    explosion(ship.centerX, ship.centerY, 10)
    ships.remove(ship)
    print(f"The {ship.fill} ship was destroyed!")

def fireBullet(ship):
    global bulletSpeed
    #7.5 is half the height of the ship, which is the distance from center to nose
    bullet = Circle(ship.centerX + math.sin(math.radians(ship.rotateAngle))*12, ship.centerY - math.cos(math.radians(ship.rotateAngle))*12, 2, fill='red')
    bullet.time = 200
    bullet.dx = ship.dx + math.sin(math.radians(ship.rotateAngle))*bulletSpeed
    bullet.dy = ship.dy - math.cos(math.radians(ship.rotateAngle))*bulletSpeed
    bullets.add(bullet)

def onKeyHold(keys):
    global shipSpeed
    #ship 1 uses wasd
    if 'a' in keys:
        ship1.drotate -= shipSpeed
    if 'd' in keys:
        ship1.drotate += shipSpeed
    if 'w' in keys:
        thrustX = math.sin(math.radians(ship1.rotateAngle)) * shipSpeed
        thrustY = math.cos(math.radians(ship1.rotateAngle)) * shipSpeed
        ship1.dx += thrustX
        ship1.dy -= thrustY
    if 's' in keys:
        thrustX = math.sin(math.radians(ship1.rotateAngle)) * (shipSpeed/2)
        thrustY = math.cos(math.radians(ship1.rotateAngle)) * (shipSpeed/2)
        ship1.dx -= thrustX
        ship1.dy += thrustY
    
    #ship 2 uses arrow keys
    if 'left' in keys:
        ship2.drotate -= shipSpeed
    if 'right' in keys:
        ship2.drotate += shipSpeed
    if 'up' in keys:
        thrustX = math.sin(math.radians(ship2.rotateAngle)) * shipSpeed
        thrustY = math.cos(math.radians(ship2.rotateAngle)) * shipSpeed
        ship2.dx += thrustX
        ship2.dy -= thrustY
    if 'down' in keys:
        thrustX = math.sin(math.radians(ship2.rotateAngle)) * (shipSpeed/2)
        thrustY = math.cos(math.radians(ship2.rotateAngle)) * (shipSpeed/2)
        ship2.dx -= thrustX
        ship2.dy += thrustY

def onKeyPress(key):
    if key == 'space':
        fireBullet(ship1)
    elif key == 'enter':
        fireBullet(ship2)

def onStep():
    ## Handle ships ##
    for ship in ships.children:
        ship.rotateAngle += ship.drotate
        ship.centerX += ship.dx
        ship.centerY += ship.dy
        
        if ship.hitsShape(planet):
            destroyShip(ship)
            
    ## Move bullets ##
    for bullet in bullets.children:
        bullet.centerX += bullet.dx
        bullet.centerY += bullet.dy
        
        if bullet.hitsShape(ship1) and ship1 in ships.children:
            destroyShip(ship1)
        elif bullet.hitsShape(ship2) and ship2 in ships.children:
            destroyShip(ship2)
        elif bullet.hitsShape(planet):
            explosion(bullet.centerX, bullet.centerY, 5)
            bullets.remove(bullet)
        for bullet2 in bullets.children:
            if (bullet != bullet2) and (bullet.hitsShape(bullet2)):
                explosion(bullet.centerX, bullet.centerY, 5)
                bullets.remove(bullet)
                bullets.remove(bullet2)

        bullet.time -= 1
        if bullet.time <= 0:
            bullets.remove(bullet)

    applyGravity()
    
    ## Decay explosions ##
    for boom in explosions.children:
        boom.time -= 1
        if boom.time <= 0:
            explosions.remove(boom)
            
    wrapObjects()

cmu_graphics.run()