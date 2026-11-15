import math
import random
import pygame
from config import *

fonte = None
fonte_pequena = None


def carregar_fontes():
    global fonte, fonte_pequena
    fonte = pygame.font.Font(None, TAMANHO_TEXTO)
    fonte_pequena = pygame.font.Font(None, TAMANHO_TEXTO_PEQUENO)


def desenhar_centro(tela, imagem, cx, cy):
    tela.blit(imagem, (int(cx) - imagem.get_width() // 2, int(cy) - imagem.get_height() // 2))


def criar_gradiente():
    gradiente = pygame.Surface((TAMANHO_GRADIENTE * 2, TAMANHO_GRADIENTE * 2), pygame.SRCALPHA)
    gradiente.fill((0, 0, 0, 255))
    for raio in range(TAMANHO_GRADIENTE, 0, -1):
        parte = raio / TAMANHO_GRADIENTE
        if parte <= NUCLEO_LUZ:
            escuro = 0
        else:
            subida = (parte - NUCLEO_LUZ) / (1 - NUCLEO_LUZ)
            escuro = int(255 * subida * subida * (3 - 2 * subida))
        pygame.draw.circle(gradiente, (0, 0, 0, escuro), (TAMANHO_GRADIENTE, TAMANHO_GRADIENTE), raio)
    return gradiente


def desenhar_barra(tela, carga):
    pygame.draw.rect(tela, COR_BARRA_FUNDO, (BARRA_X, BARRA_Y, BARRA_LARGURA, BARRA_ALTURA))
    if carga >= 1:
        cor = COR_BARRA_PRONTA
    else:
        cor = COR_BARRA
    pygame.draw.rect(tela, cor, (BARRA_X, BARRA_Y, int(BARRA_LARGURA * carga), BARRA_ALTURA))


def desenhar_susto(tela, tempo, img, duracao, zoom_inicial, zoom_final, tremor):
    if tempo < DURACAO_FLASH:
        tela.fill(COR_FLASH)
        return
    tela.fill(COR_FUNDO)
    zoom = zoom_inicial + (zoom_final - zoom_inicial) * min(tempo / duracao, 1)
    imagem = pygame.transform.scale_by(img, zoom)
    tremor_x = random.randint(-tremor, tremor)
    tremor_y = random.randint(-tremor, tremor)
    desenhar_centro(tela, imagem, LARGURA // 2 + tremor_x, ALTURA // 2 + tremor_y)


def desenhar_game_over(tela, mensagem):
    tela.fill(COR_FUNDO)
    texto = fonte.render(mensagem, True, COR_TEXTO)
    dica = fonte_pequena.render("ENTER para tentar de novo, ESC para o menu", True, COR_TEXTO)
    desenhar_centro(tela, texto, LARGURA // 2, ALTURA // 2)
    desenhar_centro(tela, dica, LARGURA // 2, ALTURA // 2 + ESPACO_LINHAS)


def desenhar_vitoria(tela, tempo, tempo_travessia):
    claridade = min(tempo / TEMPO_AMANHECER, 1)
    cor = (int(COR_AMANHECER[0] * claridade), int(COR_AMANHECER[1] * claridade), int(COR_AMANHECER[2] * claridade))
    tela.fill(cor)
    texto = fonte.render("Você atravessou o Cocal.", True, COR_TEXTO)
    marca = fonte_pequena.render("Tempo: " + str(tempo_travessia) + " segundos", True, COR_TEXTO)
    dica = fonte_pequena.render("ENTER para jogar de novo, ESC para o menu", True, COR_TEXTO)
    desenhar_centro(tela, texto, LARGURA // 2, ALTURA // 2 - ESPACO_LINHAS)
    desenhar_centro(tela, marca, LARGURA // 2, ALTURA // 2)
    desenhar_centro(tela, dica, LARGURA // 2, ALTURA // 2 + ESPACO_LINHAS)


def desenhar_barra_missao(tela, barra_y, proporcao, cor):
    barra_x = LARGURA // 2 - MISSAO_LARGURA // 2
    pygame.draw.rect(tela, COR_BARRA_FUNDO, (barra_x, barra_y, MISSAO_LARGURA, MISSAO_ALTURA))
    pygame.draw.rect(tela, cor, (barra_x, barra_y, int(MISSAO_LARGURA * proporcao), MISSAO_ALTURA))


def desenhar_preso(tela, tempo, forca):
    tela.fill(COR_FUNDO)
    titulo = fonte.render("Você pisou num laço!", True, COR_TEXTO)
    dica = fonte_pequena.render("Alterne ESQUERDA e DIREITA para soltar o pé", True, COR_TEXTO)
    desenhar_centro(tela, titulo, LARGURA // 2, ALTURA // 2 - ESPACO_LINHAS)
    desenhar_centro(tela, dica, LARGURA // 2, ALTURA // 2)
    desenhar_barra_missao(tela, MISSAO_Y, min(forca / FORCA_PARA_SOLTAR, 1), COR_FORCA)
    desenhar_barra_missao(tela, MISSAO_Y + ESPACO_BARRAS, max(1 - tempo / TEMPO_ARMADILHA, 0), COR_TEMPO)


def criar_retangulos_opcoes():
    retangulos = []
    for i in range(len(OPCOES_MENU)):
        retangulos.append(pygame.Rect(LARGURA // 2 - LARGURA_OPCAO // 2, OPCAO_Y + i * ESPACO_OPCOES, LARGURA_OPCAO, ALTURA_OPCAO))
    return retangulos


def opcao_sob_mouse(posicao, retangulos):
    for i in range(len(retangulos)):
        if retangulos[i].collidepoint(posicao):
            return i
    return -1


def desenhar_menu(tela, tempo, quadros_logo, opcao, retangulos):
    tela.fill(COR_FUNDO)
    indice = int(tempo * 1000 / MS_POR_QUADRO_LOGO) % TOTAL_QUADROS_LOGO
    logo = quadros_logo[indice]
    logo.set_alpha(min(255, int(255 * tempo / TEMPO_FADE_LOGO)))
    tela.blit(logo, (0, LOGO_Y))
    if tempo >= TEMPO_OPCOES:
        for i in range(len(OPCOES_MENU)):
            texto = OPCOES_MENU[i]
            cor = COR_OPCAO
            if i == opcao:
                texto = "> " + texto + " <"
                cor = COR_OPCAO_SELECIONADA
            imagem = fonte.render(texto, True, cor)
            desenhar_centro(tela, imagem, retangulos[i].centerx, retangulos[i].centery)


def desenhar_vulto(tela, vx, vy):
    corpo = (int(vx) - TAMANHO_VULTO, int(vy) - TAMANHO_VULTO, TAMANHO_VULTO * 2, TAMANHO_VULTO * 3)
    pygame.draw.ellipse(tela, COR_VULTO, corpo)
    pygame.draw.circle(tela, COR_VULTO, (int(vx), int(vy) - TAMANHO_VULTO), TAMANHO_VULTO)


def desenhar_susto_mulher(tela, tempo, img_rosto, img_mao):
    if tempo < DURACAO_FLASH:
        tela.fill(COR_FLASH)
        return
    tela.fill(COR_FUNDO)

    avanco = min(tempo / TEMPO_AVANCO, 1)
    zoom = ZOOM_MULHER_INICIAL + (ZOOM_MULHER_MEIO - ZOOM_MULHER_INICIAL) * avanco
    if tempo > TEMPO_AVANCO:
        zoom += (tempo - TEMPO_AVANCO) * CRESCIMENTO_MULHER
    rosto = pygame.transform.scale_by(img_rosto, zoom)
    cx = LARGURA // 2 + random.randint(-TREMOR_MULHER, TREMOR_MULHER)
    cy = ALTURA // 2 + random.randint(-TREMOR_MULHER, TREMOR_MULHER)

    esticar = min(tempo / TEMPO_BRACOS, 1)
    ombro_y = cy + rosto.get_height() // 3
    maos = []
    for lado in (-1, 1):
        ombro_x = cx + lado * rosto.get_width() // 4
        if lado == -1:
            borda_x = 0
            borda_y = MAO_ESQUERDA_Y
        else:
            borda_x = LARGURA
            borda_y = MAO_DIREITA_Y
        cotovelo_x = ombro_x + (cx + lado * COTOVELO_X - ombro_x) * esticar
        cotovelo_y = ombro_y + (COTOVELO_Y - ombro_y) * esticar
        mao_x = cotovelo_x + (borda_x - cotovelo_x) * esticar
        mao_y = cotovelo_y + (borda_y - cotovelo_y) * esticar
        ombro = (ombro_x, ombro_y)
        cotovelo = (cotovelo_x, cotovelo_y)
        mao = (mao_x, mao_y)
        pygame.draw.line(tela, COR_BRACO_SOMBRA, ombro, cotovelo, GROSSURA_BRACO + 4)
        pygame.draw.line(tela, COR_BRACO_SOMBRA, cotovelo, mao, GROSSURA_BRACO + 4)
        pygame.draw.line(tela, COR_BRACO, ombro, cotovelo, GROSSURA_BRACO)
        pygame.draw.line(tela, COR_BRACO, cotovelo, mao, GROSSURA_BRACO)
        pygame.draw.circle(tela, COR_BRACO_SOMBRA, (int(cotovelo_x), int(cotovelo_y)), GROSSURA_BRACO)
        maos.append([lado, mao_x, mao_y])

    desenhar_centro(tela, rosto, cx, cy)

    mao = pygame.transform.scale_by(img_mao, ESCALA_MAO)
    for lado, mao_x, mao_y in maos:
        if lado == -1:
            desenhar_centro(tela, mao, mao_x + mao.get_width() * 0.35, mao_y)
        else:
            espelhada = pygame.transform.flip(mao, True, False)
            desenhar_centro(tela, espelhada, mao_x - mao.get_width() * 0.35, mao_y)


def desenhar_dica(tela, texto):
    imagem = fonte_pequena.render(texto, True, COR_TEXTO)
    desenhar_centro(tela, imagem, LARGURA // 2, DICA_Y)


def desenhar_susto_homem(tela, tempo, img_rosto):
    if tempo < DURACAO_FLASH:
        tela.fill(COR_FLASH)
        return
    tela.fill(COR_FUNDO)
    angulo = math.sin(tempo * VELOCIDADE_TORCAO) * ANGULO_TORCAO + random.randint(-3, 3)
    rosto = pygame.transform.rotate(pygame.transform.scale_by(img_rosto, ZOOM_HOMEM), angulo)
    subida = min(tempo / TEMPO_SUBIDA, 1)
    inicio_y = ALTURA + rosto.get_height() // 2
    cy = inicio_y + (ALTURA // 2 - inicio_y) * subida
    cx = LARGURA // 2 + random.randint(-TREMOR_HOMEM, TREMOR_HOMEM)
    desenhar_centro(tela, rosto, cx, cy + random.randint(-TREMOR_HOMEM, TREMOR_HOMEM))


def cor_de_lamparina(claridade):
    if random.random() < CHANCE_FALHA_TEXTO:
        claridade = claridade * FALHA_TEXTO
    return (int(COR_TEXTO[0] * claridade), int(COR_TEXTO[1] * claridade), int(COR_TEXTO[2] * claridade))


def total_letras_historia():
    total = 0
    for linha in TEXTO_HISTORIA:
        total += len(linha)
    return total


def desenhar_historia(tela, tempo):
    tela.fill(COR_FUNDO)
    letras = int(tempo * LETRAS_POR_SEGUNDO)
    cor = cor_de_lamparina(1)
    y = HISTORIA_Y
    for linha in TEXTO_HISTORIA:
        parte = linha[:max(letras, 0)]
        letras -= len(linha)
        if parte != "":
            imagem = fonte_pequena.render(parte, True, cor)
            tela.blit(imagem, (MARGEM_TEXTO, y - imagem.get_height() // 2))
        y += ESPACO_HISTORIA
    if tempo * LETRAS_POR_SEGUNDO >= total_letras_historia() and int(tempo / PISCAR) % 2 == 0:
        dica = fonte_pequena.render("ENTER ou clique para avançar", True, COR_OPCAO)
        desenhar_centro(tela, dica, LARGURA // 2, DICA_FIM_Y)


def criar_botao():
    return pygame.Rect(LARGURA // 2 - BOTAO_LARGURA // 2, BOTAO_Y, BOTAO_LARGURA, BOTAO_ALTURA)


def escrever(tela, texto, fonte_usada, cor, cx, cy):
    sombra = fonte_usada.render(texto, True, COR_FUNDO)
    desenhar_centro(tela, sombra, cx + SOMBRA_TEXTO, cy + SOMBRA_TEXTO)
    desenhar_centro(tela, fonte_usada.render(texto, True, cor), cx, cy)


def desenhar_aviso(tela, tempo, botao, mouse_em_cima, fundo):
    tela.fill(COR_FUNDO)
    claridade = min(tempo / TEMPO_FADE_AVISO, 1)
    fundo.set_alpha(int(255 * claridade))
    tela.blit(fundo, (0, 0))
    cor = cor_de_lamparina(claridade)
    escrever(tela, TITULO_AVISO, fonte, cor, LARGURA // 2, AVISO_Y)
    y = AVISO_Y + ESPACO_LINHAS
    for linha in TEXTO_AVISO:
        escrever(tela, linha, fonte_pequena, cor, LARGURA // 2, y)
        y += ESPACO_HISTORIA
    cor_terco = (int(COR_TERCO[0] * claridade), int(COR_TERCO[1] * claridade), int(COR_TERCO[2] * claridade))
    y = TERCO_TEXTO_Y
    for linha in TEXTO_TERCO:
        escrever(tela, linha, fonte_pequena, cor_terco, LARGURA // 2, y)
        y += ESPACO_HISTORIA
    if claridade >= 1:
        cor_botao = COR_TEXTO
        if mouse_em_cima:
            cor_botao = COR_OPCAO_SELECIONADA
        pygame.draw.rect(tela, COR_TABUA, botao)
        pygame.draw.rect(tela, COR_TABUA_ESCURA, botao, 3)
        escrever(tela, TEXTO_BOTAO, fonte, cor_botao, botao.centerx, botao.centery)


def desenhar_terco(tela, disponivel):
    cor = COR_TERCO_USADO
    if disponivel:
        cor = COR_TERCO
    for i in range(CONTAS_TERCO):
        angulo = 2 * math.pi * i / CONTAS_TERCO
        conta_x = TERCO_X + math.cos(angulo) * RAIO_TERCO
        conta_y = TERCO_Y - RAIO_TERCO + math.sin(angulo) * RAIO_TERCO
        pygame.draw.circle(tela, cor, (int(conta_x), int(conta_y)), 2)
    pygame.draw.line(tela, cor, (TERCO_X, TERCO_Y), (TERCO_X, TERCO_Y + 14), 2)
    pygame.draw.line(tela, cor, (TERCO_X - 4, TERCO_Y + 5), (TERCO_X + 4, TERCO_Y + 5), 2)
    letra = fonte_pequena.render("Z", True, cor)
    desenhar_centro(tela, letra, TERCO_X - RAIO_TERCO * 2 - 6, TERCO_Y - RAIO_TERCO)


def desenhar_luz_colorida(tela, cx, cy, cor):
    luz = pygame.Surface((RAIO_COR_PAREDAO * 2, RAIO_COR_PAREDAO * 2), pygame.SRCALPHA)
    pygame.draw.circle(luz, (cor[0], cor[1], cor[2], FORCA_COR_PAREDAO), (RAIO_COR_PAREDAO, RAIO_COR_PAREDAO), RAIO_COR_PAREDAO)
    pygame.draw.circle(luz, (cor[0], cor[1], cor[2], FORCA_COR_PAREDAO), (RAIO_COR_PAREDAO, RAIO_COR_PAREDAO), RAIO_COR_PAREDAO // 2)
    tela.blit(luz, (int(cx) - RAIO_COR_PAREDAO, int(cy) - RAIO_COR_PAREDAO))


def desenhar_passagem(tela, tempo, numero, nome):
    tela.fill(COR_FUNDO)
    claridade = min(tempo / TEMPO_FADE_AVISO, 1)
    cor = cor_de_lamparina(claridade)
    escrever(tela, "Fase " + str(numero), fonte, cor, LARGURA // 2, ALTURA // 2 - ESPACO_LINHAS // 2)
    escrever(tela, nome, fonte_pequena, cor, LARGURA // 2, ALTURA // 2 + ESPACO_LINHAS // 2)
