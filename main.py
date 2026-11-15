import os
import math
import random
import pygame
from config import *
import telas

os.chdir(os.path.dirname(os.path.abspath(__file__)))

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




def distancia(ax, ay, bx, by):
    return ((ax - bx) ** 2 + (ay - by) ** 2) ** 0.5




def desenhar_caninana():
    if estado_caninana == ESCONDIDA:
        if tempo_pulso < DURACAO_PULSO:
            telas.desenhar_centro(tela, img_enrolada, casa_x, casa_y)
    elif estado_caninana == ATENTA:
        tremor_x = random.randint(-TREMOR_ATENTA, TREMOR_ATENTA)
        tremor_y = random.randint(-TREMOR_ATENTA, TREMOR_ATENTA)
        telas.desenhar_centro(tela, img_enrolada, casa_x + tremor_x, casa_y + tremor_y)
    else:
        for i in range(len(corpo) - 1, -1, -1):
            if i % 2 == 0:
                segmento = img_corpo_amarelo
            else:
                segmento = img_corpo_preto
            telas.desenhar_centro(tela, segmento, corpo[i][0], corpo[i][1])
        cabeca = pygame.transform.rotate(img_cabeca, angulo)
        telas.desenhar_centro(tela, cabeca, cabeca_x, cabeca_y)
















def abrir_menu():
    global estado_jogo, inicio_menu, opcao
    estado_jogo = MENU
    inicio_menu = pygame.time.get_ticks() / 1000
    opcao = OPCAO_JOGAR
    pygame.mixer.stop()
    som_ambiente.play(loops=-1)
    som_intro.play()
    pygame.mouse.set_visible(True)


def reiniciar():
    global x, y, vel_x, vel_y, direcao, quadro, contador
    global ultimo_pulso, avisou_recarga, raio_luz, estado_jogo
    global estado_caninana, cabeca_x, cabeca_y, corpo, inicio_atenta, angulo
    global armadilhas_usadas, mensagem_fim, inicio_partida

    margem = (TAMANHO_BLOCO - TAMANHO_JOGADOR) // 2
    x = COLUNA_INICIAL * TAMANHO_BLOCO + margem
    y = LINHA_INICIAL * TAMANHO_BLOCO + margem
    vel_x = 0
    vel_y = 0
    direcao = BAIXO
    quadro = 0
    contador = 0

    ultimo_pulso = pygame.time.get_ticks() / 1000 - RECARGA_PULSO
    avisou_recarga = True
    raio_luz = RAIO_LUZ
    estado_jogo = JOGANDO

    estado_caninana = ESCONDIDA
    cabeca_x = casa_x
    cabeca_y = casa_y
    corpo = []
    inicio_atenta = 0
    angulo = 0

    armadilhas_usadas = []
    mensagem_fim = ""
    inicio_partida = pygame.time.get_ticks() / 1000

    pygame.mixer.stop()
    som_ambiente.play(loops=-1)
    som_chiado.set_volume(0)
    som_chiado.play(loops=-1)
    pygame.mouse.set_visible(False)


pygame.init()
if TELA_CHEIA:
    tela = pygame.display.set_mode((LARGURA, ALTURA), pygame.FULLSCREEN | pygame.SCALED)
else:
    tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Cocal")
relogio = pygame.time.Clock()
telas.carregar_fontes()

imagens_jogador = [
    carregar_jogador("baixo"),
    carregar_jogador("cima"),
    carregar_jogador("esquerda"),
    carregar_jogador("direita"),
]
img_cabeca = pygame.image.load("sprites/caninana_cabeca.png").convert_alpha()
img_corpo_amarelo = pygame.image.load("sprites/caninana_corpo_amarelo.png").convert_alpha()
img_corpo_preto = pygame.image.load("sprites/caninana_corpo_preto.png").convert_alpha()
img_enrolada = pygame.image.load("sprites/caninana_enrolada.png").convert_alpha()

quadros_logo = []
for i in range(TOTAL_QUADROS_LOGO):
    quadros_logo.append(pygame.image.load("sprites/logo/logo_" + str(i).zfill(2) + ".png").convert_alpha())

retangulos_opcoes = telas.criar_retangulos_opcoes()

casa_x = CANINANA_COLUNA * TAMANHO_BLOCO + TAMANHO_BLOCO // 2
casa_y = CANINANA_LINHA * TAMANHO_BLOCO + TAMANHO_BLOCO // 2

sombra = pygame.Surface((LARGURA, ALTURA))
sombra.set_colorkey(COR_BURACO)

som_passo = carregar_som("sons/passo.wav", VOLUME_PASSO)
som_pulso = carregar_som("sons/pulso.wav", VOLUME_PULSO)
som_recarga = carregar_som("sons/recarga.wav", VOLUME_RECARGA)
som_ambiente = carregar_som("musica/ambiente.wav", VOLUME_AMBIENTE)
som_chiado = carregar_som("sons/chiado.wav", VOLUME_CHIADO)
som_bote = carregar_som("sons/bote.wav", VOLUME_BOTE)
som_susto = carregar_som("sons/susto.wav", VOLUME_SUSTO)
som_intro = carregar_som("sons/intro.wav", VOLUME_INTRO)
som_navegar = carregar_som("sons/navegar.wav", VOLUME_NAVEGAR)
som_confirmar = carregar_som("sons/confirmar.wav", VOLUME_CONFIRMAR)
som_armadilha = carregar_som("sons/armadilha.wav", VOLUME_ARMADILHA)
som_vitoria = carregar_som("sons/vitoria.wav", VOLUME_VITORIA)

reiniciar()
inicio_susto = 0
dir_x = 0
dir_y = 0
inicio_preso = 0
forca = 0
ultima_puxada = -1
inicio_vitoria = 0
tempo_travessia = 0
abrir_menu()

rodando = True
while rodando:
    agora = pygame.time.get_ticks() / 1000
    tempo_pulso = agora - ultimo_pulso

    escolheu = False
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        elif estado_jogo == MENU:
            tempo_menu = agora - inicio_menu
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    rodando = False
                elif tempo_menu < TEMPO_OPCOES:
                    inicio_menu = agora - TEMPO_OPCOES
                elif evento.key == pygame.K_UP or evento.key == pygame.K_w:
                    opcao = (opcao - 1) % len(OPCOES_MENU)
                    som_navegar.play()
                elif evento.key == pygame.K_DOWN or evento.key == pygame.K_s:
                    opcao = (opcao + 1) % len(OPCOES_MENU)
                    som_navegar.play()
                elif evento.key == pygame.K_RETURN or evento.key == pygame.K_SPACE:
                    escolheu = True
            elif evento.type == pygame.MOUSEMOTION and tempo_menu >= TEMPO_OPCOES:
                sob_mouse = telas.opcao_sob_mouse(evento.pos, retangulos_opcoes)
                if sob_mouse != -1 and sob_mouse != opcao:
                    opcao = sob_mouse
                    som_navegar.play()
            elif evento.type == pygame.MOUSEBUTTONDOWN and tempo_menu >= TEMPO_OPCOES:
                sob_mouse = telas.opcao_sob_mouse(evento.pos, retangulos_opcoes)
                if sob_mouse != -1:
                    opcao = sob_mouse
                    escolheu = True
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                abrir_menu()
            elif evento.key == pygame.K_RETURN and (estado_jogo == GAME_OVER or estado_jogo == VITORIA):
                reiniciar()
            elif evento.key == pygame.K_SPACE and estado_jogo == JOGANDO:
                if tempo_pulso >= RECARGA_PULSO:
                    ultimo_pulso = agora
                    tempo_pulso = 0
                    avisou_recarga = False
                    som_pulso.play()
            elif estado_jogo == PRESO:
                puxada = -1
                if evento.key == pygame.K_LEFT or evento.key == pygame.K_a:
                    puxada = ESQUERDA
                elif evento.key == pygame.K_RIGHT or evento.key == pygame.K_d:
                    puxada = DIREITA
                if puxada != -1 and puxada != ultima_puxada:
                    forca += 1
                    ultima_puxada = puxada
                    som_passo.play()

    if escolheu:
        if opcao == OPCAO_JOGAR:
            reiniciar()
            som_confirmar.play()
        else:
            rodando = False

    if estado_jogo != JOGANDO:
        if estado_jogo == MENU:
            telas.desenhar_menu(tela, agora - inicio_menu, quadros_logo, opcao, retangulos_opcoes)
        elif estado_jogo == SUSTO:
            telas.desenhar_susto(tela, agora - inicio_susto, img_cabeca)
            if agora - inicio_susto > DURACAO_SUSTO:
                estado_jogo = GAME_OVER
        elif estado_jogo == PRESO:
            telas.desenhar_preso(tela, agora - inicio_preso, forca)
            if forca >= FORCA_PARA_SOLTAR:
                estado_jogo = JOGANDO
            elif agora - inicio_preso > TEMPO_ARMADILHA:
                mensagem_fim = "Você não conseguiu se soltar do laço."
                estado_jogo = GAME_OVER
                pygame.mixer.stop()
        elif estado_jogo == VITORIA:
            telas.desenhar_vitoria(tela, agora - inicio_vitoria, tempo_travessia)
        else:
            telas.desenhar_game_over(tela, mensagem_fim)
        pygame.display.flip()
        relogio.tick(FPS)
        continue

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

    limite = VELOCIDADE_MAX
    if teclas[pygame.K_LSHIFT] or teclas[pygame.K_RSHIFT]:
        limite = VELOCIDADE_DEVAGAR
    vel_x = limitar(vel_x * ATRITO, limite)
    vel_y = limitar(vel_y * ATRITO, limite)

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

    jogador_cx = x + TAMANHO_JOGADOR // 2
    jogador_cy = y + TAMANHO_JOGADOR // 2
    dist = distancia(jogador_cx, jogador_cy, cabeca_x, cabeca_y)
    velocidade = distancia(vel_x, vel_y, 0, 0)

    linha_jogador = int(jogador_cy // TAMANHO_BLOCO)
    coluna_jogador = int(jogador_cx // TAMANHO_BLOCO)
    bloco_atual = [linha_jogador, coluna_jogador]
    if mapa[linha_jogador][coluna_jogador] == "T" and bloco_atual not in armadilhas_usadas:
        armadilhas_usadas.append(bloco_atual)
        estado_jogo = PRESO
        inicio_preso = agora
        forca = 0
        ultima_puxada = -1
        vel_x = 0
        vel_y = 0
        som_armadilha.play()
    elif mapa[linha_jogador][coluna_jogador] == "S":
        estado_jogo = VITORIA
        inicio_vitoria = agora
        tempo_travessia = int(agora - inicio_partida)
        pygame.mixer.stop()
        som_vitoria.play()

    if estado_caninana == ESCONDIDA:
        if dist < DIST_ATENTA:
            estado_caninana = ATENTA
            inicio_atenta = agora
    elif estado_caninana == ATENTA:
        if dist > DIST_ATENTA:
            estado_caninana = ESCONDIDA
        elif dist < DIST_BOTE and velocidade > VELOCIDADE_SEGURA and agora - inicio_atenta > TEMPO_AVISO:
            estado_caninana = BOTE
            dir_x = (jogador_cx - cabeca_x) / dist
            dir_y = (jogador_cy - cabeca_y) / dist
            angulo = math.degrees(math.atan2(dir_x, dir_y))
            som_bote.play()
    elif estado_caninana == BOTE:
        corpo.insert(0, (cabeca_x, cabeca_y))
        cabeca_x += dir_x * VELOCIDADE_BOTE
        cabeca_y += dir_y * VELOCIDADE_BOTE
        if distancia(jogador_cx, jogador_cy, cabeca_x, cabeca_y) < DIST_MORDIDA:
            estado_jogo = SUSTO
            inicio_susto = agora
            mensagem_fim = "A caninana te pegou."
            pygame.mixer.stop()
            som_susto.play()
        elif len(corpo) * VELOCIDADE_BOTE >= ALCANCE_BOTE:
            estado_caninana = RECUA
    elif estado_caninana == RECUA:
        if len(corpo) > 0:
            cabeca_x, cabeca_y = corpo.pop(0)
        else:
            estado_caninana = ESCONDIDA

    if estado_caninana == ATENTA:
        som_chiado.set_volume(VOLUME_CHIADO * (1 - dist / DIST_ATENTA))
    else:
        som_chiado.set_volume(0)

    alvo = RAIO_LUZ
    if dist < DIST_MEDO:
        alvo = RAIO_MIN + (RAIO_LUZ - RAIO_MIN) * dist / DIST_MEDO
    raio_luz += (alvo - raio_luz) * SUAVIZACAO

    atacando = estado_caninana == BOTE or estado_caninana == RECUA

    tela.fill(COR_FUNDO)
    desenhar_mapa()
    if not atacando:
        desenhar_caninana()
    tela.blit(imagens_jogador[direcao][quadro], (int(x), int(y)))

    if tempo_pulso < DURACAO_PULSO:
        sombra.set_alpha(int(ESCURIDAO * tempo_pulso / DURACAO_PULSO))
    else:
        sombra.set_alpha(ESCURIDAO)
    centro = (int(jogador_cx), int(jogador_cy))
    sombra.fill(COR_SOMBRA)
    pygame.draw.circle(sombra, COR_BURACO, centro, int(raio_luz))
    tela.blit(sombra, (0, 0))

    if atacando:
        desenhar_caninana()
    telas.desenhar_barra(tela, carga)
    pygame.display.flip()
    relogio.tick(FPS)

pygame.quit()
