import pygame
import coordenadas_circulo


pygame.init

screen = pygame.display.set_mode((500, 500))

rojo = 255, 0, 0

posicion = [1, 1]
tamaño = [1, 1]
pygame.draw.rect(screen, rojo, (posicion, tamaño), width=5)

# coordenadas = [[400, -300], [-200, 100]]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.update()

    # def dibujar_circulo():
    #    posicion = []
    #    tamaño = [10, 10]
    #    for i in coordenadas:
    #        posicion = coordenadas.index(1)
    #        pygame.draw.rect(screen, rojo, (posicion, tamaño), witdh=5)
pygame.quit
