import sys, os
import pygame
from pygame.locals import *


# Inicialisa pygame
pygame.init()

# Variaveis publicas
black   = 0, 0, 0
size    = width, height = 600, 400 
screen  = pygame.display.set_mode(size) 

# Load
def load_image(name):
    '''carrega a imagem'''
    # carrega uma imagem na memoria, e retorna a imagem  
    # e o seu rect (retangulo)
    fullname = os.path.join('imagem', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print ('não posso ler a imagem:', fullname)
        raise SystemExit(message)

    return image, image.get_rect()


# Barra 
class Barra (pygame.sprite.Sprite):
    '''classe para barra'''
    def __init__(self, startpos): 
        pygame.sprite.Sprite.__init__(self)

        # direcao: 1=direita, -1=esquerda
        self.direction = 1

        # carrega a imagem e a posiciona na tela
        self.image, self.rect = load_image("barra1.gif")
        self.rect.centerx = startpos[0]
        self.rect.centery = startpos[1]

    def update(self):
        # multiplicamos x por 3 pro barra mover-se
        # um pouco mais rápido!
        self.rect.move_ip((self.direction*3,0))

        # se o barra atingir os limites da tela,
        # invertemos a sua direcao
        if self.rect.left < 0:
            self.direction = 1
        elif self.rect.right > width:
            self.direction = -1

# Bola
class Bola(pygame.sprite.Sprite):
    """classe para a bola"""
    def __init__(self, startpos):
        pygame.sprite.Sprite.__init__(self)
        self.speed = [2,2]

        # carrega a imagem e a posiciona na tela
        self.image, self.rect = load_image("bola1.gif")
        self.rect.centerx = startpos[0]
        self.rect.centery = startpos[1]

        # salva a posicao inicial para ser reutilizada
        # quando a bola sair da tela pelo fundo
        self.init_pos = startpos
                
    def update(self):
        self.rect.move_ip(self.speed)

        # se a bola atingir os lados da tela, inverte a
        # direcao horizontal (x)
        if self.rect.left < 0 or self.rect.right > width:
            self.speed[0] = -self.speed[0]

        # se a bola atingir o topo da tela, inverte a
        # posicao vertical (y)
        if self.rect.top < 0: 
            self.speed[1] = -self.speed[1]

        # se a bola atingir o fundo da tela, reseta
        # a sua posicao
        if self.rect.bottom > height:
            self.rect.centerx = self.init_pos[0]
            self.rect.centery = self.init_pos[1]


# Main
def main():
    # cria os nossos objetos (barra bola)
    bola = Bola([100,100])
    barra = Barra([20,395])
    clock = pygame.time.Clock()

    pygame.display.set_caption("Monkey Pong!")

    while 1:
        # garante que o programa nao vai rodar a mais que 120fps
        clock.tick(120)
        
        # checa eventos de teclado
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
               sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    barra.direction = -1
                if event.key == pygame.K_RIGHT:
                    barra.direction = 1

        # checa se a bola colidiu no barra, e caso sim inverte 
        # a direcao vertical da bola
        if barra.rect.colliderect(bola.rect):
            if bola.speed[1] > 0:
               bola.speed[1] = -bola.speed[1]
     
        # atualiza os objetos
        bola.update()
        barra.update()

        # redesenha a tela
        screen.fill(black)
        screen.blit(bola.image, bola.rect)
        screen.blit(barra.image, barra.rect)
        pygame.display.flip()


# Inicializa.        
if __name__ == "__main__":
    main()