import os
import pygame

os.chdir(os.path.dirname(os.path.abspath(__file__)))

LARGURA = 800
ALTURA = 600
FPS = 60
COR_FUNDO = (0, 0, 0)

ACELERACAO = 0.8
ATRITO = 0.92
VELOCIDADE_MAX = 5


def limitar(valor, limite):
    if valor > limite:
        return limite
    if valor < -limite:
        return -limite
    return valor


pygame.init()
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Cocal")
relogio = pygame.time.Clock()

imagem_jogador = pygame.image.load("sprites/jogador_baixo_0.png").convert_alpha()
x = LARGURA // 2
y = ALTURA // 2
vel_x = 0
vel_y = 0

rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
        vel_x -= ACELERACAO
    if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
        vel_x += ACELERACAO
    if teclas[pygame.K_UP] or teclas[pygame.K_w]:
        vel_y -= ACELERACAO
    if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
        vel_y += ACELERACAO

    vel_x = limitar(vel_x * ATRITO, VELOCIDADE_MAX)
    vel_y = limitar(vel_y * ATRITO, VELOCIDADE_MAX)
    x += vel_x
    y += vel_y

    tela.fill(COR_FUNDO)
    tela.blit(imagem_jogador, (int(x), int(y)))
    pygame.display.flip()
    relogio.tick(FPS)

pygame.quit()
