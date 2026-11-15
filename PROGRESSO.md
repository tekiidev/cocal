# PROGRESSO DO COCAL (atualizado em 15/11/2026)

Entrega: 1 de dezembro de 2026.

## Estado atual

- Fase 0 concluída (janela, loop e personagem parado).
- Etapa 1.1 concluída: o caipira desliza com inércia (setas ou WASD).
- Etapas 1.2, 1.3 e 1.4 com código pronto (feitas de uma vez, a pedido): animação por direção, mapa em matriz e colisão.
- Marco da Fase 1 atingido: andar deslizando por um labirinto.
- Fase 2 com código pronto (feita de uma vez, a pedido): luz curta, pulso com recarga, barra, sons de ambiente e passos.
- Marco da Fase 2 atingido: a mata escura com luz e pulso.
- Perguntas de verificação pendentes: etapas 1.2, 1.3, 1.4, 2.1, 2.2 e 2.3 (estudar).
- Próxima: Fase 3, etapa 3.1 (caninana parada, com estados).

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
- [ ] 3.1 Caninana parada, com estados
- [ ] 3.2 Bote, recuo e corpo em segmentos
- [ ] 3.3 Luz que diminui com a proximidade
- [ ] 3.4 Susto, game over e reinício

### Fase 4: Jogo completo (26 a 28/nov)
- [ ] 4.1 Armadilha com mini-missão
- [ ] 4.2 Saída, vitória e estados do jogo
- [ ] 4.3 Tela inicial, galo à meia-noite e presságios básicos

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
- Controles: setas ou WASD. Velocidade negativa = esquerda ou cima.
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
| Volumes | `VOLUME_AMBIENTE`, `VOLUME_PASSO`, `VOLUME_PULSO`, `VOLUME_RECARGA` (0 a 1) | main.py |

Esta tabela cresce a cada etapa.
