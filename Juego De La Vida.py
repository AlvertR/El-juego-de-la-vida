import pygame #libreria para crea interfaz y graficos
import numpy as np #libreria para vectores, matrices y funciones matematicas
import time #libreria para obtener el tiempo
import math #libreria para calculos matematicos

pygame.init() #inicia pygame

#contadores
contarGen = 0
contarPob = 0
#tamaño de la cuadricula o tablero
ancho = 300
alto = 300
#numero de renglones y columnas
renglones = 10
columnas = 10
#tamaño de las celdas
anchoCelda = (ancho - 1) / renglones
altoCelda = (alto - 1) / columnas
#color de fondo
fondo = 25, 25, 25
#crea la ventana
screen = pygame.display.set_mode((ancho, 400))
pygame.display.set_caption('El juego de la vida')
#genera la matriz de estado con 0
estado = np.zeros((renglones, columnas))
#carga las images de los botones
start_img = pygame.image.load('play.png').convert_alpha()
stop_img = pygame.image.load('pausa.png').convert_alpha()
#define la fuente de texto
Fuente = pygame.font.SysFont("Consolas", 20)

TexNoGen = Fuente.render("No. Generaciones:", 0,(255, 255, 255))
noGen = '0' #Numero de genraciones a calcular
#rectangulos para el cuadro de texto
entrada_rect = pygame.Rect(200, 303, 40, 24)
color_rect = 185, 185, 185
borde_rect = pygame.Rect(200, 303, 40, 24)
color_borde_pasivo = 255, 255, 255
color_borde_activo = 70, 176, 255
color_borde = color_borde_pasivo
star_rect = pygame.Rect(8, 336, 28, 28)

entrada_activo = False #control de animcaion cuadro de texto
pausa = True #control de iteraciones
is_running = True #control de ejecucion de interfaz

#clase Button para crear botones
class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        #escaldo de imagen
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface): #dibuja el boton y comprueba si se a clikeado
        action = False
		#posicion del mouse
        pos = pygame.mouse.get_pos()

		#revisa si el boton se clikeo
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

		#dibuja el button
        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action
#fin de la clase Button

#instanciacion de la clase Button y creacion de boton
start_button = Button(5, 335, start_img, 0.5)

#ciclo principal del programa
while is_running:
    nuevoEstado = np.copy(estado) #Se crea la matriz de apoyo
    eventt = pygame.event.get()
    for event in eventt: #cliclo para capturar eventos de teclado y mouse

        if event.type == pygame.MOUSEMOTION: #el mouse esta en movimiento
            if entrada_rect.collidepoint(event.pos): #esta en el cuadro de texto
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_IBEAM)
            elif star_rect.collidepoint(event.pos): #esta en el boton star
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        
        if event.type == pygame.QUIT: #se preciono el icono de cerrar
            is_running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN: #se presiono el mouse
            if entrada_rect.collidepoint(event.pos): #se presiono el cuadro de texto
                entrada_activo = True
            else:
                entrada_activo = False
            posicionX, posicionY = pygame.mouse.get_pos() #posicion del clikeo
            if posicionX > 0 and posicionX < (ancho - 1) and posicionY > 0 and posicionY <(alto - 1): #Se presiono dentro del tablero
                pausa = True
                start_button = Button(5, 335, start_img, 0.5)
                if nuevoEstado[math.floor(posicionX / anchoCelda), math.floor(posicionY / altoCelda)] == 1: #se presiono una casilla activa
                    nuevoEstado[math.floor(posicionX / anchoCelda),
                             math.floor(posicionY / altoCelda)] = 0
                else:
                    nuevoEstado[math.floor(posicionX / anchoCelda),
                             math.floor(posicionY / altoCelda)] = 1
        #fin mouse presionado
        
        if event.type == pygame.KEYDOWN: #se preciono el teclado
            if entrada_activo == True: #el cuadro de texto esta activo
                if event.key == pygame.K_BACKSPACE: #se preciono retroceso
                    noGen = noGen[:-1] #se borra la ultima entrada de teclado
                elif event.key in range(pygame.K_0, pygame.K_COLON): #se presiono una tecla del 0 al 9
                    noGen += event.unicode #captura de teclado
        
        if start_button.draw(screen): #se presiono el boton de star
            if noGen != '0' and noGen != '': #las generaciones a calcular son diferntes de 0 y vacio
                if pausa == True: #el proceso esta detenido
                    pausa = False
                    start_button = Button(5, 335, stop_img, 0.5)
                    if contarGen >= int(noGen): #el numero de ejecuciones es mayor a las requeridas
                        contarGen = 0
                else:
                    pausa = True
                    start_button = Button(5, 335, start_img, 0.5)
        #fin boton presionado
    #fin captura de teclado y mouse
    
    #texto actualizable
    TexGenObt = Fuente.render("Generación: " + str(contarGen), 0,(255, 255, 255))
    TexPob = Fuente.render("Población: " + str(contarPob), 0,(255, 255, 255))

    screen.fill(fondo)
    screen.blit(TexNoGen, (5, 305))

    if entrada_activo == True: #cuadro de texto activo
        color_borde = color_borde_activo #
        noGen += '|'
    else:
        color_borde = color_borde_pasivo
    #se dibuja el cuadro de texto
    pygame.draw.rect(screen, color_rect,entrada_rect)
    pygame.draw.rect(screen, color_borde,borde_rect, 2)
    pygame.draw.rect(screen, (25, 25, 25),star_rect)
    #se dibuja la captura de teclado
    entrada = Fuente.render(noGen, 0, (0, 0, 0))
    screen.blit(entrada, (entrada_rect.x + 10, entrada_rect.y + 3))
    #aumenta el tamaño del cuadro de texto segun lo ingresado
    entrada_rect.w = max(30, entrada.get_width() + 20)
    borde_rect.w = max(30, entrada.get_width() + 20)
    #se dinuja el texto actualizable
    screen.blit(TexGenObt, (60, 340))
    screen.blit(TexPob, (60, 360))
    #se dibuja el boton star
    start_button.draw(screen)
    contarPob = 0

    #recorre el tablero por columnas
    for y in range(0, columnas):
        #recorre el tablero por renglones
        for x in range(0, renglones):    
            if not pausa: #el proceso esta activo
                if contarGen >= int(noGen): #el numero de ejecuciones es mayor a las requeridas
                    pausa = True
                    start_button = Button(5, 335, start_img, 0.5)
                    noGen = '0'

                #calcula el numero de vecinos
                if y == 0 and x == 0:
                    vecinos = estado[(x + 1), (y)] + estado[(x), (y + 1)] + estado[(x + 1), (y + 1)]
                elif y ==0 and x == (renglones - 1):
                    vecinos = estado[(x - 1), (y)] + estado[(x - 1), (y + 1)] + estado[(x), (y + 1)]
                elif y == (columnas - 1) and x == 0:
                    vecinos = estado[(x), (y - 1)] + estado[(x + 1), (y - 1)] + estado[(x + 1), (y)]
                elif y == (columnas - 1) and x == (renglones - 1):
                    vecinos = estado[(x - 1), (y - 1)] + estado[(x), (y - 1)] + estado[(x - 1), (y)]
                    contarGen += 1 #termina una genracion
                elif y == 0:
                    vecinos = estado[(x - 1), (y)] + estado[(x + 1), (y)] + estado[(x - 1), (y + 1)] + \
                            estado[(x), (y + 1)] + estado[(x + 1), (y + 1)]
                elif x == 0:
                    vecinos = estado[(x), (y - 1)] + estado[(x + 1), (y - 1)] + estado[(x + 1), (y)] + \
                            estado[(x), (y + 1)] + estado[(x + 1), (y + 1)]
                elif y == (columnas-1):
                    vecinos = estado[(x - 1), (y - 1)] + estado[(x), (y - 1)] + estado[(x + 1), (y - 1)] + \
                            estado[(x - 1), (y)] + estado[(x + 1), (y)]
                elif x == (renglones-1):
                    vecinos = estado[(x - 1), (y - 1)] + estado[(x), (y - 1)] + estado[(x - 1), (y)] + \
                        estado[(x - 1), (y + 1)] + estado[(x), (y + 1)]
                else:
                    vecinos = estado[(x - 1), (y - 1)] + estado[(x), (y - 1)] + estado[(x + 1), (y - 1)] + \
                            estado[(x - 1), (y)] + estado[(x + 1), (y)] + estado[(x - 1), (y + 1)] + \
                            estado[(x), (y + 1)] + estado[(x + 1), (y + 1)]
                #fin de calculo de vecinos

                #R1: Una celula muerta con exactamente 3 celulas vecinas vivas NACE
                if estado[x, y] == 0 and vecinos == 3:
                    nuevoEstado[x, y] = 1
                #R2: Una celula viva con 2 o 3 celulas vecinas vivas sigue VIVA, en otro caso MUERE
                elif estado[x, y] == 1 and (vecinos < 2 or vecinos > 3):
                    nuevoEstado[x, y] = 0

            if estado[x, y] == 1: #la casilla esta activa
                contarPob += 1

            #se etsablecen las coordenadas del nuevo recuadro
            poly = [((x) * anchoCelda, (y) * altoCelda),
                    ((x + 1) * anchoCelda, (y) * altoCelda),
                    ((x + 1) * anchoCelda, (y + 1) * altoCelda),
                    ((x) * anchoCelda,  (y + 1) * altoCelda)]
            
            if nuevoEstado[x, y] == 0: #la celula murio
                pygame.draw.polygon(screen, (128, 128, 128), poly, 1) #recuadro vacio
            else:
                pygame.draw.polygon(screen, (255, 255, 255), poly, 0) #recuadro lleno
    #fin recorrido del tablero

    time.sleep(1 / 10) #retrazo de actualizacion

    if noGen and noGen[-1] == '|':
        noGen = noGen[:-1]

    estado = np.copy(nuevoEstado) #asigna el nuevo estado al actual
    pygame.display.flip() #actualiza la pantalla
#fin ciclo principal

pygame.quit() #termina pygame