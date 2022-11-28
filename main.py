import pygame
from OpenGL.GL import *
import copy
import random

#Variables iniciales
pygame.init()
scale = 10
width = 100
height = 100


#el grid donde sale la simulacion
screen = pygame.display.set_mode(
    (width*scale, height*scale),
    pygame.OPENGL | pygame.DOUBLEBUF
)

#Funcion para los pixeles de celulas
def pixel(x, y, color):
    
    glEnable(GL_SCISSOR_TEST)
    glScissor(x*scale, y*scale, 1*scale, 1*scale)
    glClearColor(color[0], color[1], color[2], 1.0)
    glClear(GL_COLOR_BUFFER_BIT)
    glDisable(GL_SCISSOR_TEST)
    
#El que almacena las celulas
celulas = []

#Esta funcion es para saber cuantas celulas tenemos
for x in range(1, width+1):
    temp = []
    for y in range(1, height+1):
        xy = 0
        temp.append(xy)
        y = +1
    celulas.append(temp)
    x = +1

    
#Funcion con logica del juego
def check(x, y, celulas):
    c = 0
    # Recorre el espacio alrededor de la celula
    if x > 0 and x < 99 and y > 0 and y < 99: #tiene que ser 1 menor que el tama;o del grid
        if celulas[x-1][y+1] == 1:
            c += 1
        if celulas[x][y+1] == 1:
            c += 1
        if celulas[x+1][y+1] == 1:
            c += 1
        if celulas[x-1][y] == 1:
            c += 1
        if celulas[x+1][y] == 1:
            c += 1
        if celulas[x-1][y-1] == 1:
            c += 1
        if celulas[x][y-1] == 1:
            c += 1
        if celulas[x+1][y-1] == 1:
            c += 1

    return c

#Funcion que dibuja las celulas
def draw ():
    for x in range(len(celulas)):
        for y in range(len(celulas)):
            if celulas[x][y] == 1:
                pixel(x, y, (0.2, 0.2, 1)) #color de celulas
            else:
                pixel(x, y, (0.12, 0, 0.12)) #color de fondo

#Funcion que mantiene la actualizacion de movimiento y acciones    
def update():
    temp = copy.deepcopy(celulas)
    for x in range(width):
        for y in range(height):
            # underpopulation
            if celulas[x][y] == 1:
                if check(x, y, temp) < 2:
                    celulas[x][y] = 0
                # survival
                if check(x, y, temp) > 3:
                    celulas[x][y] = 0
                # overpopulation
                if check(x, y, temp) == 2 or check(x, y, temp) == 3:
                    celulas[x][y] = 1

            else:
                if check(x, y, temp) == 3:
                    celulas[x][y] = 1
    draw()
    

#Tama;o de pantalla

size = (width * height)/3
x = width
y = height

#creacion de pixeles
while size > 0:
    tx = random.randint(5, x-5)
    ty = random.randint(5, y-5)
    celulas[tx][ty] = 1
    size -= 1
    
bandera = True

while bandera == True:
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)

    update()

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False