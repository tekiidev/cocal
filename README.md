# Cocal

Jogo de terror 2D em Pygame. Atravesse a Mata dos Cocais no escuro, com uma luz que mal alcança os pés e um grito que revela o caminho por um instante.

Projeto da P3 de Algoritmos 1 (UFMA). Autor: Felipe.

Todos os direitos reservados.

## Como rodar

1. Instale o Python 3.
2. Instale o Pygame: `pip install pygame`
3. Dentro da pasta do projeto: `python main.py`

## Estrutura

- `main.py`: o loop do jogo, o jogador, a caninana e o mapa
- `config.py`: as constantes (velocidades, cores, tempos, volumes)
- `telas.py`: o desenho das telas (menu, laço, susto, game over e vitória)
- `sprites/`: imagens dos personagens
- `sons/`: efeitos sonoros
- `musica/`: trilha e sons de ambiente

## Controles

Menu:
- Setas ou W e S (ou o mouse): escolher
- ENTER, ESPAÇO ou clique: confirmar
- ESC: sair

Jogo:
- Setas ou WASD: andar
- SHIFT: andar devagar
- ESPAÇO: pulso
- ESQUERDA e DIREITA alternadas: soltar o pé do laço
- ENTER: jogar de novo (no game over e na vitória)
- ESC: voltar ao menu
