import os
import pygame

os.chdir(os.path.dirname(os.path.abspath(__file__)))

LARGURA = 800
ALTURA = 600
FPS = 60
COR_FUNDO = (0, 0, 0)

pygame.init()
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Cocal")
relogio = pygame.time.Clock()

imagem_jogador = pygame.image.load("sprites/jogador_baixo_0.png").convert_alpha()
x = LARGURA // 2
y = ALTURA // 2

rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    tela.fill(COR_FUNDO)
    tela.blit(imagem_jogador, (x, y))
    pygame.display.flip()
    relogio.tick(FPS)

pygame.quit()
