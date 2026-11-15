# PROGRESSO DO COCAL (atualizado em 15/11/2026)

Entrega: 1 de dezembro de 2026.

## Estado atual

- Fase 0 concluída (janela, loop e personagem parado).
- Etapa 1.1 concluída: o caipira desliza com inércia (setas ou WASD).
- Etapas 1.2, 1.3 e 1.4 com código pronto (feitas de uma vez, a pedido): animação por direção, mapa em matriz e colisão.
- Marco da Fase 1 atingido: andar deslizando por um labirinto.
- Fase 2 com código pronto (feita de uma vez, a pedido): luz curta, pulso com recarga, barra, sons de ambiente e passos.
- Marco da Fase 2 atingido: a mata escura com luz e pulso.
- Fase 3 com código pronto (feita de uma vez, a pedido): caninana com estados, bote com corpo, luz que diminui, susto, game over e reinício (ENTER).
- Marco da Fase 3 atingido: dá para perder e recomeçar.
- Tela inicial pronta (feita a pedido): logo animada, som de abertura e menu JOGAR e SAIR (teclado ou mouse).
- Tela cheia ligada (TELA_CHEIA). No jogo, ESC volta ao menu. No menu, ESC fecha.
- Perguntas de verificação pendentes: Fases 1, 2 e 3 (estudar).
- Próxima: Fase 4, etapa 4.1 (armadilha com mini-missão).

## Fases e etapas

### Fase 0: Preparação (feita)
- [x] 0.1 Janela, loop principal e personagem parado na tela

### Fase 1: Base do jogo (15 a 18/nov)
- [x] 1.1 Movimento com inércia
- [x] 1.2 Sprite pela direção e animação
- [x] 1.3 Mapa em matriz desenhado
- [x] 1.4 Colisão com as paredes

### Fase 2: Luz e pulso (19 a 21/nov)
- [x] 2.1 Máscara de luz curta
- [x] 2.2 Pulso com recarga e revelação
- [x] 2.3 Barra de recarga, sons de ambiente e passos

### Fase 3: Perigo e susto (22 a 25/nov)
- [x] 3.1 Caninana parada, com estados
- [x] 3.2 Bote, recuo e corpo em segmentos
- [x] 3.3 Luz que diminui com a proximidade
- [x] 3.4 Susto, game over e reinício

### Fase 4: Jogo completo (26 a 28/nov)
- [ ] 4.1 Armadilha com mini-missão
- [ ] 4.2 Saída, vitória e estados do jogo
- [x] 4.3a Tela inicial: logo animada, som de abertura e menu JOGAR e SAIR
- [ ] 4.3b Galo à meia-noite e presságios básicos

### Fase 5: Polimento e defesa (29 e 30/nov)
- [ ] 5.1 Equilibrar constantes e testar com outra pessoa
- [ ] 5.2 Ensaio das perguntas dos monitores e tabela completa
- [ ] 5.3 Limpeza do código e README final

### Fase 6: Extras (opcional)
- [ ] Cascavel
- [ ] Terço
- [ ] Segundo monstro
- [ ] Enigmas de lógica
- [ ] Troca entre dois mundos
- [ ] Easter eggs

## Decisões

- Nome do jogo: Cocal.
- Perigo principal: caninana (cascavel como extra).
- Objetivo: atravessar a mata do Cocal escura, passando por todos os obstáculos e monstros, até a saída.
- Mapa: 20 colunas x 15 linhas, blocos de 40 px, cada linha é um texto (`mapa[linha][coluna]`). Início em linha 1, coluna 1. Saída no canto de baixo à direita.
- Colisão: testa os 4 cantos do jogador, eixo x e eixo y separados (assim ele desliza encostado na parede).
- Luz: superfície preta com um círculo de cor COR_BURACO, que vira transparente com set_colorkey.
- Pulso: ESPAÇO, recarga de 25 s, revela o mapa e escurece de volta em 1,5 s (alpha da sombra sobe de 0 até ESCURIDAO). Tempo medido em segundos com get_ticks() / 1000.
- Sons provisórios gerados por código (sons/passo.wav, sons/pulso.wav, sons/recarga.wav, musica/ambiente.wav). Trocar pelas gravações, com o mesmo nome.
- Caninana ataca o que faz barulho: só dá o bote se o jogador estiver rápido (acima de VELOCIDADE_SEGURA). SHIFT anda devagar. Sem isso o jogo era impossível (ela fica no único caminho para a saída).
- Caninana escondida no mato (linha 12, coluna 15), ao lado do último corredor. Só aparece com o pulso; no bote aparece por cima da escuridão.
- Recuo: a cabeça volta pelas posições guardadas em `corpo` (pop do início).
- Reinício: função `reiniciar()` com `global`, chamada no começo e no ENTER.
- Sons provisórios da caninana: sons/chiado.wav, sons/bote.wav, sons/susto.wav.
- Tela inicial: novo estado `MENU`. A logo são 24 quadros PNG em `sprites/logo/` (marrom e verde musgo), trocados pelo tempo: `indice = tempo * 1000 / MS_POR_QUADRO_LOGO`, com `% TOTAL_QUADROS_LOGO` para voltar ao início. Ela aparece aos poucos (`set_alpha`) e as opções surgem em `TEMPO_OPCOES`. Qualquer tecla pula a abertura.
- Função `abrir_menu()` (com `global`) para a abertura. `reiniciar()` é chamada ao escolher JOGAR. O mouse só aparece no menu.
- Sons provisórios do menu: sons/intro.wav (ronco, vento e sino), sons/navegar.wav, sons/confirmar.wav.
- Controles: setas ou WASD, SHIFT devagar, ESPAÇO pulso, ENTER recomeça, ESC volta ao menu (no menu, ESC sai). Velocidade negativa = esquerda ou cima.
- A decidir: nome definitivo da habilidade (pulso, eco das almas ou chamado das almas).
- A decidir: terço manual (tecla) ou automático.

## Onde mudar o quê (para a defesa)

| Quero mudar | Constante ou linha | Arquivo |
| --- | --- | --- |
| Tamanho da janela | `LARGURA` e `ALTURA` | main.py |
| Velocidade do jogo | `FPS` | main.py |
| Cor do fundo | `COR_FUNDO` | main.py |
| Velocidade máxima do personagem | `VELOCIDADE_MAX` (maior = mais rápido) | main.py |
| Arranque (quão rápido ganha velocidade) | `ACELERACAO` | main.py |
| Quanto desliza ao soltar | `ATRITO` (menor = para mais rápido, 1 = nunca para) | main.py |
| Ritmo da animação de passos | `QUADROS_POR_PASSO` (menor = passos mais rápidos) | main.py |
| Velocidade mínima para animar | `VEL_MIN_ANIMACAO` | main.py |
| Desenho do labirinto | a lista `mapa` (`#` mato, `.` trilha, `T` armadilha, `S` saída) | main.py |
| Tamanho dos blocos do mapa | `TAMANHO_BLOCO` | main.py |
| Onde o jogador começa | `LINHA_INICIAL` e `COLUNA_INICIAL` | main.py |
| Cores do mapa | `COR_MATO`, `COR_TRILHA`, `COR_ARMADILHA`, `COR_SAIDA` | main.py |
| Tamanho da caixa de colisão | `TAMANHO_JOGADOR` | main.py |
| Tamanho da luz | `RAIO_LUZ` | main.py |
| Quão escuro fica fora da luz | `ESCURIDAO` (255 = breu, 0 = sem escuro) | main.py |
| Tempo de recarga do pulso | `RECARGA_PULSO` (segundos) | main.py |
| Quanto tempo o pulso mostra o mapa | `DURACAO_PULSO` (segundos) | main.py |
| Tecla do pulso | `pygame.K_SPACE` no `if` do KEYDOWN | main.py |
| Posição e tamanho da barra | `BARRA_X`, `BARRA_Y`, `BARRA_LARGURA`, `BARRA_ALTURA` | main.py |
| Cores da barra | `COR_BARRA`, `COR_BARRA_PRONTA`, `COR_BARRA_FUNDO` | main.py |
| Volumes | `VOLUME_...` (0 a 1) | main.py |
| Tela cheia ou janela | `TELA_CHEIA` (True ou False) | main.py |
| Velocidade andando devagar (SHIFT) | `VELOCIDADE_DEVAGAR` | main.py |
| Onde a caninana fica | `CANINANA_LINHA` e `CANINANA_COLUNA` | main.py |
| Distância em que ela fica atenta (chiado) | `DIST_ATENTA` | main.py |
| Distância do bote | `DIST_BOTE` | main.py |
| Velocidade que não provoca bote | `VELOCIDADE_SEGURA` | main.py |
| Tempo de aviso antes do bote | `TEMPO_AVISO` | main.py |
| Velocidade e alcance do bote | `VELOCIDADE_BOTE`, `ALCANCE_BOTE` | main.py |
| Distância que conta como mordida | `DIST_MORDIDA` | main.py |
| Luz mínima perto do perigo | `RAIO_MIN` | main.py |
| Distância em que a luz começa a diminuir | `DIST_MEDO` | main.py |
| Suavidade da luz | `SUAVIZACAO` (maior = muda mais rápido) | main.py |
| Duração e zoom do susto | `DURACAO_SUSTO`, `ZOOM_INICIAL`, `ZOOM_FINAL`, `TREMOR_SUSTO` | main.py |
| Texto do game over | `desenhar_game_over()` | main.py |
| Velocidade da animação da logo | `MS_POR_QUADRO_LOGO` (menor = mais rápida) | main.py |
| Tempo da logo aparecendo | `TEMPO_FADE_LOGO` (segundos) | main.py |
| Quando as opções do menu aparecem | `TEMPO_OPCOES` (segundos) | main.py |
| Posição da logo e das opções | `LOGO_Y`, `OPCAO_Y`, `ESPACO_OPCOES` | main.py |
| Textos do menu | `OPCOES_MENU` | main.py |
| Cores do menu | `COR_OPCAO`, `COR_OPCAO_SELECIONADA` | main.py |
| Volume da abertura e dos cliques do menu | `VOLUME_INTRO`, `VOLUME_NAVEGAR`, `VOLUME_CONFIRMAR` | main.py |

Esta tabela cresce a cada etapa.
