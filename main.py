import os
import math
import random
import pygame
from config import *
import telas
import mapas

os.chdir(os.path.dirname(os.path.abspath(__file__)))

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


def desenhar_mapa(superficie):
    for linha in range(len(mapa)):
        for coluna in range(len(mapa[linha])):
            bloco = mapa[linha][coluna]
            if bloco == "#":
                cor = COR_MATO
            elif bloco == "T":
                cor = COR_ARMADILHA
            elif bloco == "S":
                cor = COR_SAIDA
            elif bloco == "C":
                cor = COR_LAMA
            elif bloco == "W":
                cor = COR_AGUA
            elif bloco == "H":
                cor = COR_CONSTRUCAO
            else:
                cor = COR_TRILHA
            quadrado = (coluna * TAMANHO_BLOCO, linha * TAMANHO_BLOCO, TAMANHO_BLOCO, TAMANHO_BLOCO)
            pygame.draw.rect(superficie, cor, quadrado)
            centro_x = coluna * TAMANHO_BLOCO + TAMANHO_BLOCO // 2
            if bloco == "L":
                telas.desenhar_centro(superficie, img_lapide, centro_x, linha * TAMANHO_BLOCO + TAMANHO_BLOCO // 2)
            elif bloco == "+":
                base = (linha + 1) * TAMANHO_BLOCO
                superficie.blit(img_cruz, (centro_x - img_cruz.get_width() // 2, base - img_cruz.get_height()))
            elif bloco == "C":
                desenhar_curral(superficie, linha, coluna)
            elif bloco == "W":
                onda_y = linha * TAMANHO_BLOCO + (coluna * 7) % (TAMANHO_BLOCO - 8) + 4
                pygame.draw.line(superficie, COR_ONDA, (coluna * TAMANHO_BLOCO + 8, onda_y), (coluna * TAMANHO_BLOCO + 24, onda_y), 2)

    for linha in range(len(decoracao)):
        for coluna in range(len(decoracao[linha])):
            item = decoracao[linha][coluna]
            variacao = (linha + coluna) % 2
            centro_x, centro_y = centro_do_bloco([linha, coluna])
            if item == "P":
                telas.desenhar_centro(superficie, imgs_palmeira[variacao], centro_x, centro_y)
            elif item == "M":
                telas.desenhar_centro(superficie, imgs_mata[variacao], centro_x, centro_y)
            elif item == "B":
                telas.desenhar_centro(superficie, imgs_bananeira[variacao], centro_x, centro_y)
            elif item == "E":
                superficie.blit(img_estrada, (coluna * TAMANHO_BLOCO, linha * TAMANHO_BLOCO))

    for tipo, linha, coluna in construcoes:
        superficie.blit(imgs_construcoes[tipo], (coluna * TAMANHO_BLOCO, linha * TAMANHO_BLOCO))


def desenhar_arroz(agora):
    for linha in range(len(decoracao)):
        for coluna in range(len(decoracao[linha])):
            if decoracao[linha][coluna] == "R":
                centro_x, centro_y = centro_do_bloco([linha, coluna])
                balanco = math.sin(agora * VELOCIDADE_BALANCO + coluna) * BALANCO_ARROZ
                telas.desenhar_centro(tela, imgs_arroz[(linha + coluna) % 2], centro_x + balanco, centro_y)


def carregar_com_espelho(arquivo):
    imagem = pygame.image.load(arquivo).convert_alpha()
    return [imagem, pygame.transform.flip(imagem, True, False)]


def desenhar_curral(superficie, linha, coluna):
    esquerda = coluna * TAMANHO_BLOCO
    topo = linha * TAMANHO_BLOCO
    direita = esquerda + TAMANHO_BLOCO
    base = topo + TAMANHO_BLOCO
    poca_x = esquerda + (linha * 13 + coluna * 7) % (TAMANHO_BLOCO // 2)
    poca_y = topo + (linha * 7 + coluna * 11) % (TAMANHO_BLOCO // 2)
    pygame.draw.ellipse(superficie, COR_POCA, (poca_x, poca_y, TAMANHO_BLOCO // 2, TAMANHO_BLOCO // 4))
    lados = [
        [linha - 1, coluna, (esquerda, topo), (direita, topo)],
        [linha + 1, coluna, (esquerda, base), (direita, base)],
        [linha, coluna - 1, (esquerda, topo), (esquerda, base)],
        [linha, coluna + 1, (direita, topo), (direita, base)],
    ]
    for vizinho_linha, vizinho_coluna, inicio, fim in lados:
        if mapa[vizinho_linha][vizinho_coluna] in BLOCOS_SOLIDOS:
            pygame.draw.line(superficie, COR_CERCA, inicio, fim, GROSSURA_CERCA)
            pygame.draw.circle(superficie, COR_CERCA, inicio, GROSSURA_CERCA)


def eh_parede(px, py):
    coluna = int(px // TAMANHO_BLOCO)
    linha = int(py // TAMANHO_BLOCO)
    return mapa[linha][coluna] in BLOCOS_SOLIDOS


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
        if tempo_pulso < DURACAO_PULSO or terco_ativo:
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


def andar_ate(px, py, alvo_x, alvo_y, passo):
    falta = distancia(px, py, alvo_x, alvo_y)
    if falta <= passo:
        return alvo_x, alvo_y
    return px + (alvo_x - px) / falta * passo, py + (alvo_y - py) / falta * passo


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


def carregar_fase(numero):
    global fase, mapa, decoracao, construcoes, luzes, paredao, cenario
    global inicio, rota_caninana, rota_mulher, raio_base, recarga, velocidade_caninana, intervalo_min, intervalo_max
    global tem_cascavel, casa_x, casa_y, tem_bicicleta, origem_x, origem_y, tem_vaca, vaca_casa_x, vaca_casa_y
    global terco_usado
    fase = numero
    terco_usado = False
    mapa = mapas.MAPAS[fase]
    decoracao = mapas.DECORACOES[fase]
    construcoes = mapas.CONSTRUCOES[fase]
    luzes = mapas.LUZES[fase]
    paredao = mapas.PAREDOES[fase]
    inicio = mapas.INICIOS[fase]
    rota_caninana = mapas.ROTAS_CANINANA[fase]
    rota_mulher = mapas.ROTAS_MULHER[fase]
    raio_base = RAIOS_LUZ[fase]
    recarga = RECARGAS_PULSO[fase]
    velocidade_caninana = VELOCIDADES_CANINANA[fase]
    intervalo_min = INTERVALOS_MIN[fase]
    intervalo_max = INTERVALOS_MAX[fase]

    tem_cascavel = len(mapas.CASCAVEIS[fase]) > 0
    if tem_cascavel:
        casa_x, casa_y = centro_do_bloco(mapas.CASCAVEIS[fase])
    else:
        casa_x = -LONGE
        casa_y = -LONGE
    tem_bicicleta = len(mapas.BICICLETAS[fase]) > 0
    if tem_bicicleta:
        origem_x, origem_y = centro_do_bloco(mapas.BICICLETAS[fase])
    tem_vaca = len(mapas.VACAS[fase]) > 0
    if tem_vaca:
        vaca_casa_x, vaca_casa_y = centro_do_bloco(mapas.VACAS[fase])

    cenario = pygame.Surface((LARGURA, ALTURA))
    desenhar_mapa(cenario)


def novo_jogo():
    global inicio_jogo
    inicio_jogo = pygame.time.get_ticks() / 1000
    carregar_fase(0)
    reiniciar()


def passar_de_fase():
    carregar_fase(fase + 1)
    reiniciar()


def comecar_historia(agora):
    global estado_jogo, inicio_tela
    estado_jogo = HISTORIA
    inicio_tela = agora
    pygame.mixer.stop()
    som_tensao.play(loops=-1)


def avancar_introducao(agora):
    global estado_jogo, inicio_tela
    if estado_jogo == HISTORIA:
        tempo_total = telas.total_letras_historia() / LETRAS_POR_SEGUNDO
        if agora - inicio_tela < tempo_total:
            inicio_tela = agora - tempo_total
        else:
            estado_jogo = AVISO
            inicio_tela = agora
            som_navegar.play()
    else:
        novo_jogo()
        som_confirmar.play()


def usar_bicicleta(agora):
    global montado, bici_x, bici_y, homem_ativo, estado_jogo, inicio_susto_homem, vel_x, vel_y
    if not tem_bicicleta:
        return
    centro_x = x + TAMANHO_JOGADOR // 2
    centro_y = y + TAMANHO_JOGADOR // 2
    if montado:
        montado = False
        bici_x = centro_x
        bici_y = centro_y
        perto_de_casa = distancia(bici_x, bici_y, origem_x, origem_y) < DIST_DEVOLVER
        if perto_de_casa and peso_maximo >= PESO_FANTASMA and homem_ativo:
            homem_ativo = False
            estado_jogo = HOMEM
            inicio_susto_homem = agora
            vel_x = 0
            vel_y = 0
            som_rangido.set_volume(0)
            som_grito_homem.play()
    elif distancia(centro_x, centro_y, bici_x, bici_y) < DIST_PEGAR:
        montado = True


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
    global mulher_x, mulher_y, ponto_mulher, mulher_ativa
    global bici_x, bici_y, montado, peso, peso_maximo, homem_ativo
    global inicio_terco
    global vaca_x, vaca_y, estado_vaca, inicio_vaca, angulo_vaca, proximo_ei

    margem = (TAMANHO_BLOCO - TAMANHO_JOGADOR) // 2
    x = inicio[1] * TAMANHO_BLOCO + margem
    y = inicio[0] * TAMANHO_BLOCO + margem
    vel_x = 0
    vel_y = 0
    direcao = BAIXO
    quadro = 0
    contador = 0

    ultimo_pulso = pygame.time.get_ticks() / 1000 - recarga
    avisou_recarga = True
    raio_luz = raio_base
    estado_jogo = JOGANDO

    estado_cascavel = ESCONDIDA
    cascavel_x = casa_x
    cascavel_y = casa_y
    corpo_cascavel = []
    inicio_atenta = 0
    angulo_cascavel = 0
    fim_veneno = 0
    inicio_mordida = -DURACAO_FLASH_MORDIDA

    caninana_x, caninana_y = centro_do_bloco(rota_caninana[0])
    estado_caninana = PATRULHA
    ponto_rota = 1
    fim_perseguicao = 0
    rastro = []
    angulo_caninana = 0

    mulher_ativa = len(rota_mulher) > 0
    if mulher_ativa:
        mulher_x, mulher_y = centro_do_bloco(rota_mulher[0])
    ponto_mulher = 1

    if tem_bicicleta:
        bici_x = origem_x
        bici_y = origem_y
    montado = False
    peso = 0
    peso_maximo = 0
    homem_ativo = True

    if tem_vaca:
        vaca_x = vaca_casa_x
        vaca_y = vaca_casa_y
    estado_vaca = QUIETA
    inicio_vaca = 0
    angulo_vaca = 0
    proximo_ei = pygame.time.get_ticks() / 1000 + random.uniform(EI_MIN, EI_MAX)
    inicio_terco = -TEMPO_TERCO

    armadilhas_usadas = []
    mensagem_fim = ""
    inicio_partida = pygame.time.get_ticks() / 1000

    assombros_usados = []
    fila_assombros = []
    ultimo_assombro = NENHUM
    assombro_atual = NENHUM
    assombro_agendado = NENHUM
    proximo_assombro = inicio_partida + random.uniform(intervalo_min, intervalo_max)

    pygame.mixer.stop()
    som_ambiente.play(loops=-1)
    som_chocalho.set_volume(0)
    som_chocalho.play(loops=-1)
    som_chiado.set_volume(0)
    som_chiado.play(loops=-1)
    som_lamento.set_volume(0)
    som_lamento.play(loops=-1)
    som_rangido.set_volume(0)
    som_rangido.play(loops=-1)
    som_paredao.set_volume(0)
    if len(paredao) > 0:
        som_paredao.play(loops=-1)
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


sombra = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
gradiente = telas.criar_gradiente()

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
imgs_palmeira = carregar_com_espelho("sprites/palmeira.png")
imgs_mata = carregar_com_espelho("sprites/mata.png")
imgs_bananeira = carregar_com_espelho("sprites/bananeira.png")
imgs_arroz = carregar_com_espelho("sprites/arroz.png")
img_lapide = pygame.image.load("sprites/lapide.png").convert_alpha()
img_cruz = pygame.image.load("sprites/cruz.png").convert_alpha()
img_mulher = pygame.image.load("sprites/mulher.png").convert_alpha()
img_mulher.set_alpha(TRANSPARENCIA_MULHER)
img_mulher_rosto = pygame.image.load("sprites/mulher_rosto.png").convert_alpha()
img_mulher_mao = pygame.image.load("sprites/mulher_mao.png").convert_alpha()
som_lamento = carregar_som("sons/lamento.wav", VOLUME_LAMENTO)
som_grito_mulher = carregar_som("sons/grito_mulher.wav", VOLUME_GRITO_MULHER)
inicio_susto_mulher = 0
img_bicicleta = pygame.image.load("sprites/bicicleta.png").convert_alpha()
img_bicicleta_em_pe = pygame.transform.rotate(img_bicicleta, 90)
img_homem = pygame.image.load("sprites/homem.png").convert_alpha()
img_homem_rosto = pygame.image.load("sprites/homem_rosto.png").convert_alpha()
som_rangido = carregar_som("sons/rangido.wav", VOLUME_RANGIDO)
som_grito_homem = carregar_som("sons/grito_homem.wav", VOLUME_GRITO_HOMEM)
som_tensao = carregar_som("sons/tensao.wav", VOLUME_TENSAO)
som_terco = carregar_som("sons/terco.wav", VOLUME_TERCO)
som_mugido = carregar_som("sons/mugido.wav", VOLUME_MUGIDO)
som_ei = carregar_som("sons/ei.wav", VOLUME_EI)
img_vaca = pygame.image.load("sprites/vaca.png").convert_alpha()
img_vaca_rosto = pygame.image.load("sprites/vaca_rosto.png").convert_alpha()
brilho = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
botao_continuar = telas.criar_botao()
img_cabana = pygame.transform.scale(pygame.image.load("sprites/cabana.png").convert(), (LARGURA, ALTURA))
inicio_tela = 0
inicio_susto_homem = 0

img_estrada = pygame.image.load("sprites/estrada.png").convert()
imgs_construcoes = [
    pygame.image.load("sprites/bar.png").convert_alpha(),
    pygame.image.load("sprites/carro.png").convert_alpha(),
    pygame.image.load("sprites/casa.png").convert_alpha(),
]
som_paredao = carregar_som("sons/paredao.wav", VOLUME_PAREDAO)
som_passagem = carregar_som("sons/passagem.wav", VOLUME_TENSAO)
terco_usado = False
inicio_jogo = 0
carregar_fase(0)
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
        elif estado_jogo == HISTORIA or estado_jogo == AVISO:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    abrir_menu()
                elif evento.key == pygame.K_RETURN or evento.key == pygame.K_SPACE:
                    avancar_introducao(agora)
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if estado_jogo == HISTORIA or botao_continuar.collidepoint(evento.pos):
                    avancar_introducao(agora)
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                abrir_menu()
            elif evento.key == pygame.K_RETURN and estado_jogo == GAME_OVER:
                reiniciar()
            elif evento.key == pygame.K_RETURN and estado_jogo == VITORIA:
                novo_jogo()
            elif evento.key == pygame.K_RETURN and estado_jogo == PASSAGEM:
                passar_de_fase()
            elif evento.key == pygame.K_z and estado_jogo == JOGANDO and not terco_usado:
                terco_usado = True
                inicio_terco = agora
                som_terco.play()
            elif evento.key == pygame.K_e and estado_jogo == JOGANDO:
                usar_bicicleta(agora)
            elif evento.key == pygame.K_SPACE and estado_jogo == JOGANDO:
                if tempo_pulso >= recarga:
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
            comecar_historia(agora)
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
        elif estado_jogo == PASSAGEM:
            telas.desenhar_passagem(tela, agora - inicio_tela, fase + 2, mapas.NOMES_FASES[fase + 1])
            if agora - inicio_tela > TEMPO_PASSAGEM:
                passar_de_fase()
        elif estado_jogo == HISTORIA:
            telas.desenhar_historia(tela, agora - inicio_tela)
        elif estado_jogo == AVISO:
            mouse_em_cima = botao_continuar.collidepoint(pygame.mouse.get_pos())
            telas.desenhar_aviso(tela, agora - inicio_tela, botao_continuar, mouse_em_cima, img_cabana)
        elif estado_jogo == HOMEM:
            telas.desenhar_susto_homem(tela, agora - inicio_susto_homem, img_homem_rosto)
            if agora - inicio_susto_homem > DURACAO_SUSTO_HOMEM:
                estado_jogo = JOGANDO
        elif estado_jogo == MULHER:
            telas.desenhar_susto_mulher(tela, agora - inicio_susto_mulher, img_mulher_rosto, img_mulher_mao)
            if agora - inicio_susto_mulher > DURACAO_SUSTO_MULHER:
                estado_jogo = JOGANDO
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

    carga = min(tempo_pulso / recarga, 1)
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
    if montado:
        longe = distancia(x + TAMANHO_JOGADOR // 2, y + TAMANHO_JOGADOR // 2, origem_x, origem_y)
        peso = min(longe / DIST_PESO_MAX, 1)
        peso_maximo = max(peso_maximo, peso)
        limite = VELOCIDADE_BICICLETA + (VELOCIDADE_PESADA - VELOCIDADE_BICICLETA) * peso
    if teclas[pygame.K_LSHIFT] or teclas[pygame.K_RSHIFT]:
        limite = min(limite, VELOCIDADE_DEVAGAR)
    linha_pe = int((y + TAMANHO_JOGADOR // 2) // TAMANHO_BLOCO)
    coluna_pe = int((x + TAMANHO_JOGADOR // 2) // TAMANHO_BLOCO)
    if mapa[linha_pe][coluna_pe] == "C":
        limite = min(limite, VELOCIDADE_LAMA)
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
        if contador >= QUADROS_POR_PASSO and not montado:
            contador = 0
            quadro = 1 - quadro
            som_passo.play()
    if not andando or montado:
        quadro = 0

    jogador_cx = x + TAMANHO_JOGADOR // 2
    jogador_cy = y + TAMANHO_JOGADOR // 2
    if tem_cascavel:
        dist_cascavel = distancia(jogador_cx, jogador_cy, cascavel_x, cascavel_y)
    else:
        dist_cascavel = LONGE
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
    elif mapa[linha_jogador][coluna_jogador] == "S" and fase < len(mapas.MAPAS) - 1:
        estado_jogo = PASSAGEM
        inicio_tela = agora
        pygame.mixer.stop()
        som_passagem.play()
    elif mapa[linha_jogador][coluna_jogador] == "S":
        estado_jogo = VITORIA
        inicio_vitoria = agora
        tempo_travessia = int(agora - inicio_jogo)
        pygame.mixer.stop()
        som_vitoria.play()
    elif mapa[linha_jogador][coluna_jogador] == "A" and bloco_atual not in assombros_usados:
        if assombro_agendado == NENHUM and assombro_atual == NENHUM:
            assombros_usados.append(bloco_atual)
            agendar_assombro(agora)

    if agora >= proximo_assombro:
        agendar_assombro(agora)
        proximo_assombro = agora + random.uniform(intervalo_min, intervalo_max)

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
        alvo_x, alvo_y = centro_do_bloco(rota_caninana[ponto_rota])
        passo = velocidade_caninana
        if distancia(caninana_x, caninana_y, alvo_x, alvo_y) < passo:
            ponto_rota = (ponto_rota + 1) % len(rota_caninana)

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
    if len(paredao) > 0:
        som_x, som_y = centro_do_bloco(paredao)
        dist_paredao = distancia(jogador_cx, jogador_cy, som_x, som_y)
        som_paredao.set_volume(VOLUME_PAREDAO * max(0, 1 - dist_paredao / DIST_SOM_PAREDAO))
    if montado:
        som_rangido.set_volume(VOLUME_RANGIDO * peso)
    else:
        som_rangido.set_volume(0)

    perigo = min(dist_cascavel, dist_caninana)

    if tem_vaca:
        no_curral = mapa[linha_jogador][coluna_jogador] == "C"
        if no_curral and estado_vaca == QUIETA:
            estado_vaca = BRAVA
            inicio_vaca = agora
            som_mugido.play()
        elif not no_curral and estado_vaca == BRAVA:
            estado_vaca = QUIETA
        if estado_vaca == BRAVA and agora - inicio_vaca > TEMPO_BUFAR:
            alvo_x, alvo_y = jogador_cx, jogador_cy
            passo = VELOCIDADE_VACA
        else:
            alvo_x, alvo_y = vaca_casa_x, vaca_casa_y
            passo = VELOCIDADE_VACA_CALMA
        novo_x, novo_y = andar_ate(vaca_x, vaca_y, alvo_x, alvo_y, passo)
        if mapa[int(novo_y // TAMANHO_BLOCO)][int(novo_x // TAMANHO_BLOCO)] == "C":
            if novo_x != vaca_x or novo_y != vaca_y:
                angulo_vaca = math.degrees(math.atan2(novo_x - vaca_x, novo_y - vaca_y))
            vaca_x, vaca_y = novo_x, novo_y
        dist_vaca = distancia(jogador_cx, jogador_cy, vaca_x, vaca_y)
        if estado_vaca == BRAVA:
            perigo = min(perigo, dist_vaca)
            if dist_vaca < DIST_CHIFRE:
                estado_jogo = SUSTO
                inicio_susto = agora
                img_susto = img_vaca_rosto
                mensagem_fim = "A vaca parida te prensou na cerca."
                pygame.mixer.stop()
                som_susto.play()

    if agora >= proximo_ei:
        canal = som_ei.play()
        if canal is not None:
            if random.choice([True, False]):
                canal.set_volume(VOLUME_EI, 0)
            else:
                canal.set_volume(0, VOLUME_EI)
        proximo_ei = agora + random.uniform(EI_MIN, EI_MAX)
    if mulher_ativa:
        alvo_x, alvo_y = centro_do_bloco(rota_mulher[ponto_mulher])
        if distancia(mulher_x, mulher_y, alvo_x, alvo_y) < VELOCIDADE_MULHER:
            ponto_mulher = (ponto_mulher + 1) % len(rota_mulher)
        mulher_x, mulher_y = andar_ate(mulher_x, mulher_y, alvo_x, alvo_y, VELOCIDADE_MULHER)
        dist_mulher = distancia(jogador_cx, jogador_cy, mulher_x, mulher_y)
        perigo = min(perigo, dist_mulher)
        som_lamento.set_volume(VOLUME_LAMENTO * max(0, 1 - dist_mulher / DIST_SOM_MULHER))
        if dist_mulher < DIST_MULHER:
            mulher_ativa = False
            estado_jogo = MULHER
            inicio_susto_mulher = agora
            vel_x = 0
            vel_y = 0
            som_lamento.stop()
            som_grito_mulher.play()

    alvo = raio_base
    if perigo < DIST_MEDO:
        alvo = RAIO_MIN + (raio_base - RAIO_MIN) * perigo / DIST_MEDO
    if agora < fim_veneno:
        alvo = min(alvo, RAIO_VENENO)
    raio_luz += (alvo - raio_luz) * SUAVIZACAO

    atacando = estado_cascavel == BOTE or estado_cascavel == RECUA
    tempo_terco = agora - inicio_terco
    terco_ativo = tempo_terco < TEMPO_TERCO

    tela.blit(cenario, (0, 0))
    if tem_cascavel and not atacando:
        desenhar_cascavel()
    desenhar_caninana()
    if tem_vaca:
        telas.desenhar_centro(tela, pygame.transform.rotate(img_vaca, angulo_vaca), vaca_x, vaca_y)
    if montado:
        if direcao == CIMA or direcao == BAIXO:
            telas.desenhar_centro(tela, img_bicicleta_em_pe, jogador_cx, jogador_cy)
        else:
            telas.desenhar_centro(tela, img_bicicleta, jogador_cx, jogador_cy)
    elif tem_bicicleta:
        telas.desenhar_centro(tela, img_bicicleta, bici_x, bici_y)
    tela.blit(imagens_jogador[direcao][quadro], (int(x), int(y)))
    if montado and peso > PESO_FANTASMA:
        visivel = (peso - PESO_FANTASMA) / (1 - PESO_FANTASMA)
        img_homem.set_alpha(int(TRANSPARENCIA_FANTASMA * visivel))
        atras_x = [0, 0, DESVIO_FANTASMA, -DESVIO_FANTASMA][direcao]
        atras_y = [-DESVIO_FANTASMA, DESVIO_FANTASMA, 0, 0][direcao]
        telas.desenhar_centro(tela, img_homem, jogador_cx + atras_x, jogador_cy + atras_y)
    desenhar_arroz(agora)

    if assombro_atual == VULTO:
        progresso = tempo_assombro / DURACOES_ASSOMBRO[VULTO]
        vulto_x = jogador_cx + lado_assombro * (DIST_VULTO - 2 * DIST_VULTO * progresso)
        telas.desenhar_vulto(tela, vulto_x, jogador_cy + DESVIO_VULTO_Y)

    raio_desenho = raio_luz
    if assombro_atual == LAMPARINA:
        raio_desenho = raio_luz * random.uniform(FATOR_LUZ_MIN, FATOR_LUZ_MAX)

    if tempo_pulso < DURACAO_PULSO:
        escuro = int(ESCURIDAO * tempo_pulso / DURACAO_PULSO)
    else:
        escuro = ESCURIDAO
    if terco_ativo:
        voltando = max(0, tempo_terco - (TEMPO_TERCO - FADE_TERCO)) / FADE_TERCO
        escuro = min(escuro, int(ESCURIDAO * voltando))
    tamanho = max(int(raio_desenho * 2 * ALCANCE_LUZ), 1)
    luz = pygame.transform.smoothscale(gradiente, (tamanho, tamanho))
    sombra.fill((0, 0, 0, escuro))
    canto = (int(jogador_cx) - tamanho // 2, int(jogador_cy) - tamanho // 2)
    sombra.blit(luz, canto, special_flags=pygame.BLEND_RGBA_MIN)
    for luz_linha, luz_coluna, luz_raio in luzes:
        luz_x, luz_y = centro_do_bloco([luz_linha, luz_coluna])
        tamanho = int(luz_raio * 2 * ALCANCE_LUZ)
        mancha = pygame.transform.smoothscale(gradiente, (tamanho, tamanho))
        sombra.blit(mancha, (luz_x - tamanho // 2, luz_y - tamanho // 2), special_flags=pygame.BLEND_RGBA_MIN)
    tela.blit(sombra, (0, 0))
    if len(paredao) > 0:
        som_x, som_y = centro_do_bloco(paredao)
        cor = CORES_PAREDAO[int(agora * PISCADAS_POR_SEGUNDO) % len(CORES_PAREDAO)]
        telas.desenhar_luz_colorida(tela, som_x, som_y, cor)
    if terco_ativo:
        brilho.fill((COR_TERCO[0], COR_TERCO[1], COR_TERCO[2], int(BRILHO_TERCO * (1 - tempo_terco / TEMPO_TERCO))))
        tela.blit(brilho, (0, 0))

    if tem_vaca and estado_vaca == BRAVA:
        direcao_vaca = math.radians(angulo_vaca)
        cabeca_vaca_x = vaca_x + math.sin(direcao_vaca) * DIST_OLHOS_VACA
        cabeca_vaca_y = vaca_y + math.cos(direcao_vaca) * DIST_OLHOS_VACA
        for lado in (-1, 1):
            olho_x = cabeca_vaca_x + math.cos(direcao_vaca) * SEPARACAO_OLHOS * lado
            olho_y = cabeca_vaca_y - math.sin(direcao_vaca) * SEPARACAO_OLHOS * lado
            pygame.draw.circle(tela, COR_OLHO_VACA, (int(olho_x), int(olho_y)), 2)
    if mulher_ativa:
        flutuar = math.sin(agora * FLUTUAR_VELOCIDADE) * FLUTUAR_ALTURA
        telas.desenhar_centro(tela, img_mulher, mulher_x, mulher_y + flutuar)
    if tem_cascavel and atacando:
        desenhar_cascavel()
    if agora - inicio_mordida < DURACAO_FLASH_MORDIDA:
        tela.fill(COR_MORDIDA)
    telas.desenhar_barra(tela, carga)
    telas.desenhar_terco(tela, not terco_usado)
    if agora - inicio_partida < TEMPO_NOME_FASE:
        telas.desenhar_dica(tela, "Fase " + str(fase + 1) + ": " + mapas.NOMES_FASES[fase])
    elif montado:
        telas.desenhar_dica(tela, "E para largar a bicicleta")
    elif tem_bicicleta and distancia(jogador_cx, jogador_cy, bici_x, bici_y) < DIST_PEGAR:
        telas.desenhar_dica(tela, "E para pegar a bicicleta")
    pygame.display.flip()
    relogio.tick(FPS)

pygame.quit()
