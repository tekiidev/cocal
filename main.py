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

QUADROS_POR_PASSO = 10
VEL_MIN_ANIMACAO = 0.5

BAIXO = 0
CIMA = 1
ESQUERDA = 2
DIREITA = 3

TAMANHO_BLOCO = 40
TAMANHO_JOGADOR = 32
LINHA_INICIAL = 1
COLUNA_INICIAL = 1

COR_MATO = (12, 40, 18)
COR_TRILHA = (90, 70, 45)
COR_ARMADILHA = (120, 30, 30)
COR_SAIDA = (200, 180, 90)

RAIO_LUZ = 70
ESCURIDAO = 255
COR_SOMBRA = (0, 0, 0)
COR_BURACO = (255, 0, 255)

RECARGA_PULSO = 25
DURACAO_PULSO = 1.5

BARRA_X = 20
BARRA_Y = 570
BARRA_LARGURA = 150
BARRA_ALTURA = 10
COR_BARRA_FUNDO = (40, 40, 40)
COR_BARRA = (110, 110, 160)
COR_BARRA_PRONTA = (220, 210, 150)

VOLUME_AMBIENTE = 0.4
VOLUME_PASSO = 0.3
VOLUME_PULSO = 0.8
VOLUME_RECARGA = 0.5

mapa = [
    "####################",
    "#....#.......#.....#",
    "#.##.#.#####.#.###.#",
    "#.#..#.#...#...#...#",
    "#.#.##.#.#.#####.###",
    "#.#....#.#.....#...#",
    "#.######.#####.###.#",
    "#......#.....#.....#",
    "######.#####.###.#.#",
    "#....#.#...#...#.#.#",
    "#.##.#.#.#.###.#.#.#",
    "#.#..T...#...#...#.#",
    "#.#.######.#.#####.#",
    "#...#......#......S#",
    "####################",
]


def limitar(valor, limite):
    if valor > limite:
        return limite
    if valor < -limite:
        return -limite
    return valor


def carregar_jogador(direcao):
    quadro_0 = pygame.image.load("sprites/jogador_" + direcao + "_0.png").convert_alpha()
    quadro_1 = pygame.image.load("sprites/jogador_" + direcao + "_1.png").convert_alpha()
    return [quadro_0, quadro_1]


def desenhar_mapa():
    for linha in range(len(mapa)):
        for coluna in range(len(mapa[linha])):
            bloco = mapa[linha][coluna]
            if bloco == "#":
                cor = COR_MATO
            elif bloco == "T":
                cor = COR_ARMADILHA
            elif bloco == "S":
                cor = COR_SAIDA
            else:
                cor = COR_TRILHA
            quadrado = (coluna * TAMANHO_BLOCO, linha * TAMANHO_BLOCO, TAMANHO_BLOCO, TAMANHO_BLOCO)
            pygame.draw.rect(tela, cor, quadrado)


def eh_parede(px, py):
    coluna = int(px // TAMANHO_BLOCO)
    linha = int(py // TAMANHO_BLOCO)
    return mapa[linha][coluna] == "#"


def colide(px, py):
    fim_x = px + TAMANHO_JOGADOR - 1
    fim_y = py + TAMANHO_JOGADOR - 1
    return eh_parede(px, py) or eh_parede(fim_x, py) or eh_parede(px, fim_y) or eh_parede(fim_x, fim_y)


def carregar_som(arquivo, volume):
    som = pygame.mixer.Sound(arquivo)
    som.set_volume(volume)
    return som


def desenhar_barra(carga):
    pygame.draw.rect(tela, COR_BARRA_FUNDO, (BARRA_X, BARRA_Y, BARRA_LARGURA, BARRA_ALTURA))
    if carga >= 1:
        cor = COR_BARRA_PRONTA
    else:
        cor = COR_BARRA
    pygame.draw.rect(tela, cor, (BARRA_X, BARRA_Y, int(BARRA_LARGURA * carga), BARRA_ALTURA))


pygame.init()
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Cocal")
relogio = pygame.time.Clock()

imagens_jogador = [
    carregar_jogador("baixo"),
    carregar_jogador("cima"),
    carregar_jogador("esquerda"),
    carregar_jogador("direita"),
]
direcao = BAIXO
quadro = 0
contador = 0
margem = (TAMANHO_BLOCO - TAMANHO_JOGADOR) // 2
x = COLUNA_INICIAL * TAMANHO_BLOCO + margem
y = LINHA_INICIAL * TAMANHO_BLOCO + margem
vel_x = 0
vel_y = 0

sombra = pygame.Surface((LARGURA, ALTURA))
sombra.set_colorkey(COR_BURACO)

ultimo_pulso = -RECARGA_PULSO
avisou_recarga = True

som_passo = carregar_som("sons/passo.wav", VOLUME_PASSO)
som_pulso = carregar_som("sons/pulso.wav", VOLUME_PULSO)
som_recarga = carregar_som("sons/recarga.wav", VOLUME_RECARGA)
som_ambiente = carregar_som("musica/ambiente.wav", VOLUME_AMBIENTE)
som_ambiente.play(loops=-1)

rodando = True
while rodando:
    agora = pygame.time.get_ticks() / 1000
    tempo_pulso = agora - ultimo_pulso

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
            if tempo_pulso >= RECARGA_PULSO:
                ultimo_pulso = agora
                tempo_pulso = 0
                avisou_recarga = False
                som_pulso.play()

    carga = min(tempo_pulso / RECARGA_PULSO, 1)
    if carga >= 1 and not avisou_recarga:
        som_recarga.play()
        avisou_recarga = True

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
    if colide(x, y):
        x -= vel_x
        vel_x = 0

    y += vel_y
    if colide(x, y):
        y -= vel_y
        vel_y = 0

    andando = abs(vel_x) > VEL_MIN_ANIMACAO or abs(vel_y) > VEL_MIN_ANIMACAO
    if andando:
        if abs(vel_x) > abs(vel_y):
            if vel_x > 0:
                direcao = DIREITA
            else:
                direcao = ESQUERDA
        else:
            if vel_y > 0:
                direcao = BAIXO
            else:
                direcao = CIMA

        contador += 1
        if contador >= QUADROS_POR_PASSO:
            contador = 0
            quadro = 1 - quadro
            som_passo.play()
    else:
        quadro = 0

    tela.fill(COR_FUNDO)
    desenhar_mapa()
    tela.blit(imagens_jogador[direcao][quadro], (int(x), int(y)))

    if tempo_pulso < DURACAO_PULSO:
        sombra.set_alpha(int(ESCURIDAO * tempo_pulso / DURACAO_PULSO))
    else:
        sombra.set_alpha(ESCURIDAO)
    centro = (int(x) + TAMANHO_JOGADOR // 2, int(y) + TAMANHO_JOGADOR // 2)
    sombra.fill(COR_SOMBRA)
    pygame.draw.circle(sombra, COR_BURACO, centro, RAIO_LUZ)
    tela.blit(sombra, (0, 0))

    desenhar_barra(carga)
    pygame.display.flip()
    relogio.tick(FPS)

pygame.quit()
