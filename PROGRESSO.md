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
- Etapa 4.1 pronta: laço de caçador no `T` com mini-missão (alternar ESQUERDA e DIREITA).
- Etapa 4.2 pronta: chegar no `S` dá vitória, com amanhecer, som de vitória e o tempo da travessia.
- Marco da Fase 4 quase atingido: já dá para jogar uma fase completa do menu até a vitória ou a derrota.
- Código dividido em 3 arquivos: `main.py` (loop, jogador, caninana, mapa), `config.py` (todas as constantes) e `telas.py` (desenho das telas e da barra).
- Etapa 4.3b pronta: assombros (sustos que não matam) em pontos `A` do mapa e por tempo, sorteados sem repetir.
- Duas cobras: a cascavel (verde) faz a tocaia e o bote com veneno; a caninana anda pelo mapa, persegue quando ouve e mata se encostar.
- Próxima: Fase 4, etapa 4.3c (mais assombros e presságios).

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
- [x] 4.1 Armadilha com mini-missão
- [x] 4.2 Saída, vitória e estados do jogo
- [x] 4.3a Tela inicial: logo animada, som de abertura e menu JOGAR e SAIR
- [x] 4.3b Assombros (parte 1): vulto, lamparina e sussurro
- [ ] 4.3c Assombros (parte 2): mais tipos, galo à meia-noite e presságios

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
- Perigos: cascavel (tocaia, bote e veneno) e caninana (anda pelo mapa e persegue quando ouve). A cascavel saiu dos extras da Fase 6.
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
- Armadilha: laço de caçador. Novo estado `PRESO`. Cada puxada alternada (ESQUERDA depois DIREITA) soma 1 em `forca`; repetir a mesma tecla não conta. Solta com `FORCA_PARA_SOLTAR` puxadas antes de `TEMPO_ARMADILHA` segundos, senão é game over. Cada laço só prende uma vez (lista `armadilhas_usadas`, zerada no `reiniciar()`).
- Vitória: novo estado `VITORIA`. Detectada como o laço, pelo bloco do centro do jogador (`elif ... == "S"`). A tela vai do preto até `COR_AMANHECER` em `TEMPO_AMANHECER` segundos, multiplicando cada parte da cor pela `claridade` (0 a 1). Mostra `tempo_travessia` (segundos desde o `inicio_partida`, que é guardado no `reiniciar()`). ENTER joga de novo.
- Estados do jogo: MENU, JOGANDO, PRESO, SUSTO, GAME_OVER e VITORIA.
- Som provisório: sons/vitoria.wav (passarinhos, galo e vento).
- Organização: constantes no `config.py`, importadas com `from config import *` (os nomes continuam iguais). Telas no `telas.py`, chamadas com `telas.nome_da_funcao(...)`. As funções do `telas.py` recebem por parâmetro o que precisam (`tela`, `forca`, `mensagem`...), porque o `global` só funciona dentro do próprio arquivo. As fontes são criadas em `telas.carregar_fontes()`, depois do `pygame.init()`.
- Assombros: sustos que não matam (o nome evita confusão com o estado `SUSTO` da caninana). Tipos numa lista (`TIPOS_ASSOMBRO`): VULTO (figura escura cruza a luz), LAMPARINA (a luz treme e quase apaga) e SUSSURRO (voz só no fone esquerdo ou direito, com `canal.set_volume(esq, dir)`). Disparam ao pisar num `A` (cada um uma vez) ou a cada 20 a 45 s sorteados. Atraso aleatório de 0,3 a 1,5 s antes de começar. Sorteio sem repetir: `random.shuffle` numa cópia da lista e `pop`; ao reabastecer, o primeiro nunca é igual ao último. Um assombro por vez (`NENHUM = -1` quando não há).
- Sons provisórios: sons/vulto.wav, sons/lamparina.wav, sons/sussurro.wav (trocar pela minha voz).
- Troca de papéis: a cobra de tocaia (estados ESCONDIDA, ATENTA, BOTE, RECUA) virou a cascavel, com sprites verdes e aviso de chocalho. Variáveis renomeadas: `estado_cascavel`, `cascavel_x`, `corpo_cascavel`, `dist_cascavel`, `CASCAVEL_LINHA`...
- Veneno: a 1ª mordida da cascavel não mata. Tela pisca vermelho, `fim_veneno = agora + TEMPO_VENENO` e a luz fica em `RAIO_VENENO`. Uma 2ª mordida antes do fim do veneno é game over.
- Caninana: estados PATRULHA e PERSEGUINDO. Na patrulha vai de ponto em ponto da lista `ROTA_CANINANA` (com `% len` volta ao primeiro). Se o jogador estiver rápido (acima de `VELOCIDADE_SEGURA`) e a menos de `DIST_OUVIR`, ela persegue por `TEMPO_PERSEGUICAO` segundos. Anda em linha reta, atravessando o mato. O corpo é a lista `rastro` com as posições antigas da cabeça, desenhando um segmento a cada `ESPACO_RASTRO`. Encostar (`DIST_TOQUE`) é game over. O chiado aumenta com a proximidade.
- A luz diminui pelo perigo mais perto: `perigo = min(dist_cascavel, dist_caninana)`.
- `VELOCIDADE_SEGURA` subiu para 2.2: andando devagar na diagonal a velocidade é √(1,5² + 1,5²) ≈ 2,12, e com 2 isso contava como barulho.
- Teste: com cuidado (esperar a caninana passar antes de cruzar a linha 10 e usar SHIFT perto das cobras) dá para vencer; correndo, ela pega.
- Sons e sprites provisórios: sons/chocalho.wav, sons/mordida.wav, sprites/cascavel_*.png (cores trocadas dos sprites da caninana).
- Game over com mensagem variável (`mensagem_fim`): caninana ou laço.
- Som provisório: sons/armadilha.wav (estalo de madeira e corda).
- A decidir: nome definitivo da habilidade (pulso, eco das almas ou chamado das almas).
- A decidir: terço manual (tecla) ou automático.

## Onde mudar o quê (para a defesa)

| Quero mudar | Constante ou linha | Arquivo |
| --- | --- | --- |
| Tamanho da janela | `LARGURA` e `ALTURA` | config.py |
| Velocidade do jogo | `FPS` | config.py |
| Cor do fundo | `COR_FUNDO` | config.py |
| Velocidade máxima do personagem | `VELOCIDADE_MAX` (maior = mais rápido) | config.py |
| Arranque (quão rápido ganha velocidade) | `ACELERACAO` | config.py |
| Quanto desliza ao soltar | `ATRITO` (menor = para mais rápido, 1 = nunca para) | config.py |
| Ritmo da animação de passos | `QUADROS_POR_PASSO` (menor = passos mais rápidos) | config.py |
| Velocidade mínima para animar | `VEL_MIN_ANIMACAO` | config.py |
| Desenho do labirinto | a lista `mapa` (`#` mato, `.` trilha, `T` armadilha, `S` saída) | main.py |
| Tamanho dos blocos do mapa | `TAMANHO_BLOCO` | config.py |
| Onde o jogador começa | `LINHA_INICIAL` e `COLUNA_INICIAL` | config.py |
| Cores do mapa | `COR_MATO`, `COR_TRILHA`, `COR_ARMADILHA`, `COR_SAIDA` | config.py |
| Tamanho da caixa de colisão | `TAMANHO_JOGADOR` | config.py |
| Tamanho da luz | `RAIO_LUZ` | config.py |
| Quão escuro fica fora da luz | `ESCURIDAO` (255 = breu, 0 = sem escuro) | config.py |
| Tempo de recarga do pulso | `RECARGA_PULSO` (segundos) | config.py |
| Quanto tempo o pulso mostra o mapa | `DURACAO_PULSO` (segundos) | config.py |
| Tecla do pulso | `pygame.K_SPACE` no `if` do KEYDOWN | main.py |
| Posição e tamanho da barra | `BARRA_X`, `BARRA_Y`, `BARRA_LARGURA`, `BARRA_ALTURA` | config.py |
| Cores da barra | `COR_BARRA`, `COR_BARRA_PRONTA`, `COR_BARRA_FUNDO` | config.py |
| Volumes | `VOLUME_...` (0 a 1) | config.py |
| Tela cheia ou janela | `TELA_CHEIA` (True ou False) | config.py |
| Velocidade andando devagar (SHIFT) | `VELOCIDADE_DEVAGAR` | config.py |
| Onde a cascavel fica | `CASCAVEL_LINHA` e `CASCAVEL_COLUNA` | config.py |
| Distância em que a cascavel fica atenta (chocalho) | `DIST_ATENTA` | config.py |
| Distância do bote | `DIST_BOTE` | config.py |
| Velocidade que não provoca bote | `VELOCIDADE_SEGURA` | config.py |
| Tempo de aviso antes do bote | `TEMPO_AVISO` | config.py |
| Velocidade e alcance do bote | `VELOCIDADE_BOTE`, `ALCANCE_BOTE` | config.py |
| Distância que conta como mordida | `DIST_MORDIDA` | config.py |
| Luz mínima perto do perigo | `RAIO_MIN` | config.py |
| Distância em que a luz começa a diminuir | `DIST_MEDO` | config.py |
| Suavidade da luz | `SUAVIZACAO` (maior = muda mais rápido) | config.py |
| Duração e zoom do susto | `DURACAO_SUSTO`, `ZOOM_INICIAL`, `ZOOM_FINAL`, `TREMOR_SUSTO` | config.py |
| Texto do game over | `desenhar_game_over()` | telas.py |
| Velocidade da animação da logo | `MS_POR_QUADRO_LOGO` (menor = mais rápida) | config.py |
| Tempo da logo aparecendo | `TEMPO_FADE_LOGO` (segundos) | config.py |
| Quando as opções do menu aparecem | `TEMPO_OPCOES` (segundos) | config.py |
| Posição da logo e das opções | `LOGO_Y`, `OPCAO_Y`, `ESPACO_OPCOES` | config.py |
| Textos do menu | `OPCOES_MENU` | config.py |
| Cores do menu | `COR_OPCAO`, `COR_OPCAO_SELECIONADA` | config.py |
| Onde ficam os pontos de assombro | letra `A` no `mapa` | main.py |
| Tipos de assombro e duração | `TIPOS_ASSOMBRO`, `DURACOES_ASSOMBRO` | config.py |
| Atraso antes do assombro | `ATRASO_MIN`, `ATRASO_MAX` | config.py |
| Intervalo dos assombros por tempo | `INTERVALO_MIN`, `INTERVALO_MAX` | config.py |
| Vulto (distância, tamanho, cor) | `DIST_VULTO`, `DESVIO_VULTO_Y`, `TAMANHO_VULTO`, `COR_VULTO` | config.py |
| Quanto a lamparina apaga | `FATOR_LUZ_MIN`, `FATOR_LUZ_MAX` | config.py |
| Volumes dos assombros | `VOLUME_VULTO`, `VOLUME_LAMPARINA`, `VOLUME_SUSSURRO` | config.py |
| Rota da caninana | `ROTA_CANINANA` (lista de [linha, coluna]) | config.py |
| Velocidade da caninana (patrulha e perseguição) | `VELOCIDADE_CANINANA`, `VELOCIDADE_PERSEGUICAO` | config.py |
| Distância em que a caninana ouve | `DIST_OUVIR` | config.py |
| Tempo de perseguição | `TEMPO_PERSEGUICAO` | config.py |
| Distância que conta como encostar | `DIST_TOQUE` | config.py |
| Tamanho do corpo da caninana | `TAMANHO_RASTRO`, `ESPACO_RASTRO` | config.py |
| Veneno (luz e duração) | `RAIO_VENENO`, `TEMPO_VENENO` | config.py |
| Piscada vermelha da mordida | `DURACAO_FLASH_MORDIDA`, `COR_MORDIDA` | config.py |
| Onde fica a saída | letra `S` no `mapa` | main.py |
| Tempo do amanhecer na vitória | `TEMPO_AMANHECER` (segundos) | config.py |
| Cor do amanhecer | `COR_AMANHECER` | config.py |
| Texto da vitória | `desenhar_vitoria()` | telas.py |
| Volume da vitória | `VOLUME_VITORIA` | config.py |
| Puxadas para soltar do laço | `FORCA_PARA_SOLTAR` | config.py |
| Tempo para soltar do laço | `TEMPO_ARMADILHA` (segundos) | config.py |
| Onde ficam as armadilhas | letra `T` no `mapa` | main.py |
| Barras da mini-missão | `MISSAO_Y`, `MISSAO_LARGURA`, `MISSAO_ALTURA`, `ESPACO_BARRAS`, `COR_FORCA`, `COR_TEMPO` | config.py |
| Volume da abertura e dos cliques do menu | `VOLUME_INTRO`, `VOLUME_NAVEGAR`, `VOLUME_CONFIRMAR` | config.py |

Esta tabela cresce a cada etapa.
