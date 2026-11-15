# PROGRESSO DO COCAL (atualizado em 15/11/2026)

Entrega: 1 de dezembro de 2026.

## Estado atual

- Fase 0 concluída (janela, loop e personagem parado).
- Próxima etapa: Fase 1, etapa 1.1 (movimento com inércia).
- Perguntas de verificação pendentes: etapa 1.1 (código escrito, falta responder).

## Fases e etapas

### Fase 0: Preparação (feita)
- [x] 0.1 Janela, loop principal e personagem parado na tela

### Fase 1: Base do jogo (15 a 18/nov)
- [ ] 1.1 Movimento com inércia
- [ ] 1.2 Sprite pela direção e animação
- [ ] 1.3 Mapa em matriz desenhado
- [ ] 1.4 Colisão com as paredes

### Fase 2: Luz e pulso (19 a 21/nov)
- [ ] 2.1 Máscara de luz curta
- [ ] 2.2 Pulso com recarga e revelação
- [ ] 2.3 Barra de recarga, sons de ambiente e passos

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
- A decidir: nome definitivo da habilidade (pulso, eco das almas ou chamado das almas).
- A decidir: terço manual (tecla) ou automático.

## Onde mudar o quê (para a defesa)

| Quero mudar | Constante ou linha | Arquivo |
| --- | --- | --- |
| Tamanho da janela | `LARGURA` e `ALTURA` | main.py |
| Velocidade do jogo | `FPS` | main.py |
| Cor do fundo | `COR_FUNDO` | main.py |
| Posição inicial do personagem | `x` e `y` | main.py |

Esta tabela cresce a cada etapa.
