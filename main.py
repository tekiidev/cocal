import os
import math
import random
import pygame
from config import *
import telas

os.chdir(os.path.dirname(os.path.abspath(__file__)))

mapa = [
    "####################",
    "#....#...A...#.....#",
    "#.##.#.#####.#.###.#",
    "#.#..#.#...#...#...#",
    "#.#.##.#.#.#####.###",
    "#A#....#.#.....#...#",
    "#.######.#####.###.#",
    "#....A.#.....#.....#",
    "######.#####.###.#.#",
    "#....#.#.A.#...#.#.#",
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


def desenhar_cascavel():
    if estado_cascavel == ESCONDIDA:
        if tempo_pulso < DURACAO_PULSO:
            telas.desenhar_centro(tela, img_cascavel_enrolada, casa_x, casa_y)
    elif estado_cascavel == ATENTA:
        tremor_x = random.randint(-TREMOR_ATENTA, TREMOR_ATENTA)
        tremor_y = random.randint(-TREMOR_ATENTA, TREMOR_ATENTA)
        telas.desenhar_centro(tela, img_cascavel_enrolada, casa_x + tremor_x, casa_y + tremor_y)
    else:
        for i in range(len(corpo_cascavel) - 1, -1, -1):
            if i % 2 == 0:
                segmento = img_cascavel_claro
            else:
                segmento = img_cascavel_escuro
            telas.desenhar_centro(tela, segmento, corpo_cascavel[i][0], corpo_cascavel[i][1])
        cabeca = pygame.transform.rotate(img_cascavel_cabeca, angulo_cascavel)
        telas.desenhar_centro(tela, cabeca, cascavel_x, cascavel_y)


def desenhar_caninana():
    numero = 0
    for i in range(len(rastro) - 1, 0, -ESPACO_RASTRO):
        if numero % 2 == 0:
            segmento = img_caninana_amarelo
        else:
            segmento = img_caninana_preto
        telas.desenhar_centro(tela, segmento, rastro[i][0], rastro[i][1])
        numero += 1
    cabeca = pygame.transform.rotate(img_caninana_cabeca, angulo_caninana)
    telas.desenhar_centro(tela, cabeca, caninana_x, caninana_y)


def centro_do_bloco(ponto):
    return ponto[1] * TAMANHO_BLOCO + TAMANHO_BLOCO // 2, ponto[0] * TAMANHO_BLOCO + TAMANHO_BLOCO // 2


def abrir_menu():
    global estado_jogo, inicio_menu, opcao
    estado_jogo = MENU
    inicio_menu = pygame.time.get_ticks() / 1000
    opcao = OPCAO_JOGAR
    pygame.mixer.stop()
    som_ambiente.play(loops=-1)
    som_intro.play()
    pygame.mouse.set_visible(True)


def sortear_assombro():
    global fila_assombros, ultimo_assombro
    if len(fila_assombros) == 0:
        fila_assombros = TIPOS_ASSOMBRO[:]
        random.shuffle(fila_assombros)
        if fila_assombros[-1] == ultimo_assombro:
            fila_assombros[0], fila_assombros[-1] = fila_assombros[-1], fila_assombros[0]
    ultimo_assombro = fila_assombros.pop()
    return ultimo_assombro


def agendar_assombro(agora):
    global assombro_agendado
    if assombro_agendado == NENHUM and assombro_atual == NENHUM:
        assombro_agendado = agora + random.uniform(ATRASO_MIN, ATRASO_MAX)


def comecar_assombro(agora):
    global assombro_atual, inicio_assombro, lado_assombro, rosto_mostrado
    assombro_atual = sortear_assombro()
    rosto_mostrado = False
    inicio_assombro = agora
    lado_assombro = random.choice([-1, 1])
    if assombro_atual == VULTO:
        som_vulto.play()
    elif assombro_atual == LAMPARINA:
        som_lamparina.play()
    else:
        canal = som_sussurro.play()
        if canal is not None:
            if lado_assombro == -1:
                canal.set_volume(VOLUME_SUSSURRO, 0)
            else:
                canal.set_volume(0, VOLUME_SUSSURRO)


def reiniciar():
    global x, y, vel_x, vel_y, direcao, quadro, contador
    global ultimo_pulso, avisou_recarga, raio_luz, estado_jogo
    global estado_cascavel, cascavel_x, cascavel_y, corpo_cascavel, inicio_atenta, angulo_cascavel
    global armadilhas_usadas, mensagem_fim, inicio_partida
    global assombros_usados, fila_assombros, ultimo_assombro
    global assombro_atual, assombro_agendado, proximo_assombro
    global caninana_x, caninana_y, estado_caninana, ponto_rota, fim_perseguicao, rastro, angulo_caninana
    global fim_veneno, inicio_mordida

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

    estado_cascavel = ESCONDIDA
    cascavel_x = casa_x
    cascavel_y = casa_y
    corpo_cascavel = []
    inicio_atenta = 0
    angulo_cascavel = 0
    fim_veneno = 0
    inicio_mordida = -DURACAO_FLASH_MORDIDA

    caninana_x, caninana_y = centro_do_bloco(ROTA_CANINANA[0])
    estado_caninana = PATRULHA
    ponto_rota = 1
    fim_perseguicao = 0
    rastro = []
    angulo_caninana = 0

    armadilhas_usadas = []
    mensagem_fim = ""
    inicio_partida = pygame.time.get_ticks() / 1000

    assombros_usados = []
    fila_assombros = []
    ultimo_assombro = NENHUM
    assombro_atual = NENHUM
    assombro_agendado = NENHUM
    proximo_assombro = inicio_partida + random.uniform(INTERVALO_MIN, INTERVALO_MAX)

    pygame.mixer.stop()
    som_ambiente.play(loops=-1)
    som_chocalho.set_volume(0)
    som_chocalho.play(loops=-1)
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
img_cascavel_cabeca = pygame.image.load("sprites/cascavel_cabeca.png").convert_alpha()
img_cascavel_claro = pygame.image.load("sprites/cascavel_corpo_claro.png").convert_alpha()
img_cascavel_escuro = pygame.image.load("sprites/cascavel_corpo_escuro.png").convert_alpha()
img_cascavel_enrolada = pygame.image.load("sprites/cascavel_enrolada.png").convert_alpha()
img_caninana_cabeca = pygame.image.load("sprites/caninana_cabeca.png").convert_alpha()
img_caninana_amarelo = pygame.image.load("sprites/caninana_corpo_amarelo.png").convert_alpha()
img_caninana_preto = pygame.image.load("sprites/caninana_corpo_preto.png").convert_alpha()

quadros_logo = []
for i in range(TOTAL_QUADROS_LOGO):
    quadros_logo.append(pygame.image.load("sprites/logo/logo_" + str(i).zfill(2) + ".png").convert_alpha())

retangulos_opcoes = telas.criar_retangulos_opcoes()

casa_x = CASCAVEL_COLUNA * TAMANHO_BLOCO + TAMANHO_BLOCO // 2
casa_y = CASCAVEL_LINHA * TAMANHO_BLOCO + TAMANHO_BLOCO // 2

sombra = pygame.Surface((LARGURA, ALTURA))
sombra.set_colorkey(COR_BURACO)

som_passo = carregar_som("sons/passo.wav", VOLUME_PASSO)
som_pulso = carregar_som("sons/pulso.wav", VOLUME_PULSO)
som_recarga = carregar_som("sons/recarga.wav", VOLUME_RECARGA)
som_ambiente = carregar_som("musica/ambiente.wav", VOLUME_AMBIENTE)
som_chocalho = carregar_som("sons/chocalho.wav", VOLUME_CHOCALHO)
som_bote = carregar_som("sons/bote.wav", VOLUME_BOTE)
som_susto = carregar_som("sons/susto.wav", VOLUME_SUSTO)
som_intro = carregar_som("sons/intro.wav", VOLUME_INTRO)
som_navegar = carregar_som("sons/navegar.wav", VOLUME_NAVEGAR)
som_confirmar = carregar_som("sons/confirmar.wav", VOLUME_CONFIRMAR)
som_armadilha = carregar_som("sons/armadilha.wav", VOLUME_ARMADILHA)
som_vitoria = carregar_som("sons/vitoria.wav", VOLUME_VITORIA)
som_vulto = carregar_som("sons/vulto.wav", VOLUME_VULTO)
som_lamparina = carregar_som("sons/lamparina.wav", VOLUME_LAMPARINA)
som_sussurro = carregar_som("sons/sussurro.wav", VOLUME_SUSSURRO)
som_chiado = carregar_som("sons/chiado.wav", VOLUME_CHIADO)
som_mordida = carregar_som("sons/mordida.wav", VOLUME_MORDIDA)
som_grito = carregar_som("sons/grito.wav", VOLUME_GRITO)
img_rosto = pygame.image.load("sprites/cara.png").convert_alpha()
rosto_mostrado = False
inicio_rosto = 0

img_susto = img_caninana_cabeca
inicio_assombro = 0
lado_assombro = 1
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
            telas.desenhar_susto(tela, agora - inicio_susto, img_susto, DURACAO_SUSTO, ZOOM_INICIAL, ZOOM_FINAL, TREMOR_SUSTO)
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
        elif estado_jogo == ROSTO:
            telas.desenhar_susto(tela, agora - inicio_rosto, img_rosto, DURACAO_ROSTO, ZOOM_ROSTO_INICIAL, ZOOM_ROSTO_FINAL, TREMOR_ROSTO)
            if agora - inicio_rosto > DURACAO_ROSTO:
                estado_jogo = JOGANDO
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
    dist_cascavel = distancia(jogador_cx, jogador_cy, cascavel_x, cascavel_y)
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
    elif mapa[linha_jogador][coluna_jogador] == "A" and bloco_atual not in assombros_usados:
        if assombro_agendado == NENHUM and assombro_atual == NENHUM:
            assombros_usados.append(bloco_atual)
            agendar_assombro(agora)

    if agora >= proximo_assombro:
        agendar_assombro(agora)
        proximo_assombro = agora + random.uniform(INTERVALO_MIN, INTERVALO_MAX)

    if assombro_agendado != NENHUM and agora >= assombro_agendado:
        assombro_agendado = NENHUM
        comecar_assombro(agora)

    tempo_assombro = agora - inicio_assombro
    if assombro_atual != NENHUM and tempo_assombro > DURACOES_ASSOMBRO[assombro_atual]:
        assombro_atual = NENHUM

    if assombro_atual == VULTO and not rosto_mostrado and tempo_assombro >= DURACOES_ASSOMBRO[VULTO] / 2:
        rosto_mostrado = True
        if random.random() < CHANCE_ROSTO:
            estado_jogo = ROSTO
            inicio_rosto = agora
            assombro_atual = NENHUM
            vel_x = 0
            vel_y = 0
            som_grito.play()

    if estado_cascavel == ESCONDIDA:
        if dist_cascavel < DIST_ATENTA:
            estado_cascavel = ATENTA
            inicio_atenta = agora
    elif estado_cascavel == ATENTA:
        if dist_cascavel > DIST_ATENTA:
            estado_cascavel = ESCONDIDA
        elif dist_cascavel < DIST_BOTE and velocidade > VELOCIDADE_SEGURA and agora - inicio_atenta > TEMPO_AVISO:
            estado_cascavel = BOTE
            dir_x = (jogador_cx - cascavel_x) / dist_cascavel
            dir_y = (jogador_cy - cascavel_y) / dist_cascavel
            angulo_cascavel = math.degrees(math.atan2(dir_x, dir_y))
            som_bote.play()
    elif estado_cascavel == BOTE:
        corpo_cascavel.insert(0, (cascavel_x, cascavel_y))
        cascavel_x += dir_x * VELOCIDADE_BOTE
        cascavel_y += dir_y * VELOCIDADE_BOTE
        if distancia(jogador_cx, jogador_cy, cascavel_x, cascavel_y) < DIST_MORDIDA:
            if agora < fim_veneno:
                estado_jogo = SUSTO
                inicio_susto = agora
                img_susto = img_cascavel_cabeca
                mensagem_fim = "O veneno da cascavel te venceu."
                pygame.mixer.stop()
                som_susto.play()
            else:
                fim_veneno = agora + TEMPO_VENENO
                inicio_mordida = agora
                estado_cascavel = RECUA
                som_mordida.play()
        elif len(corpo_cascavel) * VELOCIDADE_BOTE >= ALCANCE_BOTE:
            estado_cascavel = RECUA
    elif estado_cascavel == RECUA:
        if len(corpo_cascavel) > 0:
            cascavel_x, cascavel_y = corpo_cascavel.pop(0)
        else:
            estado_cascavel = ESCONDIDA

    if estado_cascavel == ATENTA:
        som_chocalho.set_volume(VOLUME_CHOCALHO * (1 - dist_cascavel / DIST_ATENTA))
    else:
        som_chocalho.set_volume(0)

    dist_caninana = distancia(jogador_cx, jogador_cy, caninana_x, caninana_y)
    if velocidade > VELOCIDADE_SEGURA and dist_caninana < DIST_OUVIR:
        if estado_caninana == PATRULHA:
            som_bote.play()
        estado_caninana = PERSEGUINDO
        fim_perseguicao = agora + TEMPO_PERSEGUICAO
    elif estado_caninana == PERSEGUINDO and agora > fim_perseguicao:
        estado_caninana = PATRULHA

    if estado_caninana == PERSEGUINDO:
        alvo_x = jogador_cx
        alvo_y = jogador_cy
        passo = VELOCIDADE_PERSEGUICAO
    else:
        alvo_x, alvo_y = centro_do_bloco(ROTA_CANINANA[ponto_rota])
        passo = VELOCIDADE_CANINANA
        if distancia(caninana_x, caninana_y, alvo_x, alvo_y) < passo:
            ponto_rota = (ponto_rota + 1) % len(ROTA_CANINANA)

    falta = distancia(caninana_x, caninana_y, alvo_x, alvo_y)
    if falta > 0:
        mov_x = (alvo_x - caninana_x) / falta * passo
        mov_y = (alvo_y - caninana_y) / falta * passo
        caninana_x += mov_x
        caninana_y += mov_y
        angulo_caninana = math.degrees(math.atan2(mov_x, mov_y))
    rastro.insert(0, (caninana_x, caninana_y))
    if len(rastro) > TAMANHO_RASTRO * ESPACO_RASTRO:
        rastro.pop()

    if dist_caninana < DIST_TOQUE:
        estado_jogo = SUSTO
        inicio_susto = agora
        img_susto = img_caninana_cabeca
        mensagem_fim = "A caninana te pegou."
        pygame.mixer.stop()
        som_susto.play()

    som_chiado.set_volume(VOLUME_CHIADO * max(0, 1 - dist_caninana / DIST_SOM_CANINANA))

    perigo = min(dist_cascavel, dist_caninana)
    alvo = RAIO_LUZ
    if perigo < DIST_MEDO:
        alvo = RAIO_MIN + (RAIO_LUZ - RAIO_MIN) * perigo / DIST_MEDO
    if agora < fim_veneno:
        alvo = min(alvo, RAIO_VENENO)
    raio_luz += (alvo - raio_luz) * SUAVIZACAO

    atacando = estado_cascavel == BOTE or estado_cascavel == RECUA

    tela.fill(COR_FUNDO)
    desenhar_mapa()
    if not atacando:
        desenhar_cascavel()
    desenhar_caninana()
    tela.blit(imagens_jogador[direcao][quadro], (int(x), int(y)))

    if assombro_atual == VULTO:
        progresso = tempo_assombro / DURACOES_ASSOMBRO[VULTO]
        vulto_x = jogador_cx + lado_assombro * (DIST_VULTO - 2 * DIST_VULTO * progresso)
        telas.desenhar_vulto(tela, vulto_x, jogador_cy + DESVIO_VULTO_Y)

    raio_desenho = raio_luz
    if assombro_atual == LAMPARINA:
        raio_desenho = raio_luz * random.uniform(FATOR_LUZ_MIN, FATOR_LUZ_MAX)

    if tempo_pulso < DURACAO_PULSO:
        sombra.set_alpha(int(ESCURIDAO * tempo_pulso / DURACAO_PULSO))
    else:
        sombra.set_alpha(ESCURIDAO)
    centro = (int(jogador_cx), int(jogador_cy))
    sombra.fill(COR_SOMBRA)
    pygame.draw.circle(sombra, COR_BURACO, centro, int(raio_desenho))
    tela.blit(sombra, (0, 0))

    if atacando:
        desenhar_cascavel()
    if agora - inicio_mordida < DURACAO_FLASH_MORDIDA:
        tela.fill(COR_MORDIDA)
    telas.desenhar_barra(tela, carga)
    pygame.display.flip()
    relogio.tick(FPS)

pygame.quit()
