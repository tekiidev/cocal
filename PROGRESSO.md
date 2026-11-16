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
- Luz: começou com um círculo recortado (`set_colorkey`); hoje é suave (ver "Luz suave").
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
- Rosto: quando o vulto chega no meio da travessia (passa pelo caipira), aparece uma cara em tela cheia por `DURACAO_ROSTO` s, com flash, zoom, tremor e grito. Não mata: depois volta ao jogo (estado `ROSTO`). `CHANCE_ROSTO` (0 a 1) controla se toda passagem do vulto mostra a cara. A `desenhar_susto` do `telas.py` agora recebe imagem, duração, zoom e tremor, e serve para o susto das cobras e para o rosto.
- Pendente: aviso de sustos, luzes piscando e fones na tela inicial (previsto no CLAUDE.md).
- Sprite e som provisórios: sprites/cara.png, sons/grito.wav.
- Cemitério: área aberta de 4x4 blocos no canto de cima à esquerda (linhas 2 a 5, colunas 1 a 4), no caminho do jogador. Letras novas no mapa: `L` (lápide) e `+` (cruz de madeira grande, desenhada com a base no bloco e subindo um bloco acima). As duas são sólidas: `eh_parede` agora usa `in BLOCOS_SOLIDOS` ("#L+"). O ponto de assombro que ficava ali saiu.
- Mulher de branco: anda bem devagar pela `ROTA_MULHER` (um retângulo em volta da cruz que cruza o corredor da esquerda), meio transparente (`set_alpha`) e flutuando (`math.sin`). É desenhada depois da sombra, então aparece fraca até no escuro. O lamento aumenta com a proximidade e a luz diminui perto dela. Chegar a menos de `DIST_MULHER` dispara o susto (estado `MULHER`), que não mata; depois ela some até a próxima partida (`mulher_ativa`).
- Susto da mulher (`telas.desenhar_susto_mulher`): flash; a cara avança (zoom até `ZOOM_MULHER_MEIO` em `TEMPO_AVANCO`) e continua crescendo para fora da tela (`CRESCIMENTO_MULHER`); dois braços finos (linhas) saem de baixo do queixo, sobem até cotovelos no alto (`COTOVELO_X`, `COTOVELO_Y`) e descem até as mãos, que agarram as bordas (`MAO_ESQUERDA_Y`, `MAO_DIREITA_Y`). A mão direita é a esquerda espelhada (`pygame.transform.flip`).
- Nova função `andar_ate(px, py, alvo_x, alvo_y, passo)`: anda um passo em direção ao alvo sem passar dele. Usada pela mulher.
- Sprites e sons provisórios: sprites/mulher.png, mulher_rosto.png, mulher_mao.png, cruz.png, lapide.png; sons/lamento.wav, sons/grito_mulher.wav.
- Ambientação: segunda matriz `decoracao` (15 x 20, igual ao mapa), separada do `mapa`. Letras: `P` palmeira de babaçu, `M` mata, `B` bananeira (na parte das cobras, linhas 9 a 13), `R` arroz alto (nas trilhas em volta dos pontos do vulto), `.` nada. Palmeira, mata e bananeira ficam no mato; o arroz fica em cima da trilha e é desenhado depois do jogador (ele some na palha) e balança com `math.sin`. Cada planta tem a imagem normal e a espelhada (`carregar_com_espelho`), escolhida por `(linha + coluna) % 2`, para não parecerem todas iguais.
- Desempenho: o cenário (chão, mato, lápides, cruz e plantas) é desenhado uma vez só na imagem `cenario`, antes do loop, e a cada quadro só é colado com `tela.blit(cenario, (0, 0))`. Caiu de 18 ms para 4 ms por quadro. O arroz continua sendo desenhado a cada quadro porque balança.
- Sprites provisórios: sprites/palmeira.png, mata.png, bananeira.png, arroz.png.
- Bicicleta (história do João Rufino): fica na linha 7, coluna 3. Tecla E pega (a menos de `DIST_PEGAR`) e larga. Na bicicleta a velocidade máxima vai de `VELOCIDADE_BICICLETA` (8) até `VELOCIDADE_PESADA` (1) conforme o `peso`, que é a distância até onde ela foi pega dividida por `DIST_PESO_MAX` (0 a 1). Longe ela fica pesada; voltando, fica leve. Com peso acima de `PESO_FANTASMA` toca um rangido e aparece um homem transparente na garupa. Largar de volta no lugar de origem (a menos de `DIST_DEVOLVER`) depois de ela ter ficado pesada (`peso_maximo`) dispara o susto do homem (estado `HOMEM`, uma vez por partida, não mata). Largar em outro lugar não assusta. Na bicicleta o jogador é rápido e faz barulho (as cobras ouvem).
- Susto do homem (`telas.desenhar_susto_homem`): flash; a cara sobe por baixo da tela (`TEMPO_SUBIDA`) e fica torcendo a cabeça (`pygame.transform.rotate` com `math.sin`), diferente do zoom dos outros sustos.
- Dica na tela (`telas.desenhar_dica`): "E para pegar a bicicleta" só quando o E funciona, e "E para largar" enquanto está montado. Fica no topo (`DICA_Y`).
- Luz suave: a sombra tem transparência por pixel (`SRCALPHA`). Um degradê redondo (`telas.criar_gradiente`, feito uma vez) é redimensionado ao tamanho da luz e carimbado na sombra com `BLEND_RGBA_MIN`. Totalmente clara até `NUCLEO_LUZ` do raio e escurece até `ALCANCE_LUZ` vezes o raio. Saiu o círculo com `set_colorkey` (`COR_BURACO`).
- Sprites e sons provisórios: sprites/bicicleta.png, homem.png, homem_rosto.png; sons/rangido.wav, sons/grito_homem.wav.
- Introdução: JOGAR no menu leva para a HISTORIA (texto letra por letra, `LETRAS_POR_SEGUNDO`, tremendo como lamparina) e depois para o AVISO (jogar de noite e de fone; aviso de sustos, sons altos e luzes piscando; explicação da Reza do terço) com o botão CONTINUAR. ENTER ou clique completa o texto e avança. Som de tensão (zumbido, sapos, grilos, batimento) nas duas telas. Os textos ficam em `TEXTO_HISTORIA`, `TEXTO_AVISO` e `TEXTO_TERCO` no config.py. ENTER no game over e na vitória recomeça direto, sem a introdução.
- Tela de aviso com fundo de parede de taipa (barro com as varas aparecendo nos buracos) e beiral de palha (sprites/cabana.png, 200x150 esticado para 800x600). Texto com sombra (`telas.escrever`, `SOMBRA_TEXTO`) e botão de tábua (`COR_TABUA`).
- Texto da história reescrito com as histórias reais (ver CLAUDE.md): caninana no açude, mulher de branco na estrada do cemitério, alma na garupa da bicicleta, cascavel comum no mato, vaca parida que avança. Os vultos no arroz saíram do texto porque são invenção do jogo.
- Reza do terço: tecla Z, uma vez por partida (`terco_usado`). Clarão dourado que mostra a mata inteira por `TEMPO_TERCO` segundos (escuridão zero e volta aos poucos em `FADE_TERCO`), inclusive a cascavel escondida. Ícone do terço no canto: dourado disponível, cinza usado.
- Sons provisórios: sons/tensao.wav, sons/terco.wav (trocar pela minha voz: "Valei-me, Nossa Senhora!").
- Curral: área de lama (letra `C`) no canto de cima à direita, entre o corredor do topo e a coluna 18, que desce até a saída por fora da área das cobras. É uma rota alternativa arriscada. Na lama a velocidade máxima é `VELOCIDADE_LAMA` (2). A cerca é desenhada automaticamente nos lados do curral que encostam em blocos sólidos (`desenhar_curral`).
- Vaca parida: estados QUIETA e BRAVA. Entrou na lama, ela muge e fica BRAVA; depois de `TEMPO_BUFAR` corre atrás do jogador a `VELOCIDADE_VACA` (2.7, mais rápida que ele na lama). Não sai do curral (só anda se o próximo ponto for `C`). Saindo do curral ela desiste e volta devagar para o canto. Olhos vermelhos no escuro quando brava. Chifrada (`DIST_CHIFRE`) é game over ("A vaca parida te prensou na cerca."). A saída do curral fica do lado oposto à entrada e a vaca começa perto da entrada, para vir por trás. Teste: atravessando sem parar ela chega a 37 px (chifrada a 28); parado, ela pega.
- Sapo do "ei, ei, ei": voz sintetizada que parece gente chamando, tocada a cada `EI_MIN` a `EI_MAX` segundos (sorteado), num lado só do fone.
- Sprites e sons provisórios: sprites/vaca.png, vaca_rosto.png; sons/mugido.wav, sons/ei.wav.
- TRÊS FASES (mapas no arquivo `mapas.py`). Os perigos acumulam:
  - Fase 1, A mata e o açude: caninana, laço e vultos no arroz. Açude (`W`, sólido). Sem cascavel.
  - Fase 2, A estrada do cemitério e o Bar da Oneide: + mulher de branco no cemitério, bicicleta na estrada, cascavel ao lado da estrada. Bar de barro com telha de cerâmica e caminhonete com paredão (luz colorida piscando e som que diminui com a distância). Estrada com textura (`E` na decoração). Saída no portão do cemitério.
  - Fase 3, As fazendas do morro: + curral obrigatório com a vaca parida (ela começa no canto oposto e a saída do curral é para longe dela). Duas casas de taipa e palha. Caminho mais longo (48 blocos).
  - Dificuldade por fase (listas no config.py): `RAIOS_LUZ` 80/70/58, `RECARGAS_PULSO` 20/25/30, `VELOCIDADES_CANINANA` 1.0/1.2/1.5, assombros mais frequentes (`INTERVALOS_MIN`, `INTERVALOS_MAX`).
  - `mapas.py` tem uma lista por coisa que muda de fase: `MAPAS`, `DECORACOES`, `INICIOS`, `CASCAVEIS`, `BICICLETAS`, `VACAS`, `ROTAS_CANINANA`, `ROTAS_MULHER`, `CONSTRUCOES` (bar, carro, casa), `LUZES` (pontos que clareiam o escuro), `PAREDOES`, `NOMES_FASES`. A posição `[0]` é a fase 1. Lista vazia = a fase não tem.
  - `carregar_fase(numero)` pega tudo da fase, guarda em variáveis (`mapa`, `decoracao`, `raio_base`, `recarga`...) e desenha o `cenario`. `novo_jogo()` começa da fase 1 e zera o terço. `passar_de_fase()` carrega a próxima.
  - Chegar no `S` das fases 1 e 2 mostra a tela de passagem (estado `PASSAGEM`, 4 s ou ENTER). Na fase 3 é vitória, com o tempo total desde o começo do jogo.
  - Game over recomeça a fase atual.
  - Terço: uma reza por tentativa. Volta ao começar o jogo, ao passar de fase e ao recomeçar a fase depois de morrer (`terco_usado = False` dentro de `reiniciar`).
  - Nome da fase aparece no topo nos primeiros `TEMPO_NOME_FASE` segundos.
  - Nas fases sem cascavel, `dist_cascavel = LONGE`, então ela nunca acorda. Vaca e bicicleta só existem quando `tem_vaca` e `tem_bicicleta`.
  - Teste: as 3 fases foram vencidas por um jogador automático cuidadoso, e o jogo inteiro (fase 1 → 2 → 3 → vitória, com uma morte no meio) funcionou.
- Texto da história com jeito de interior (marminino, égua, visse). Clarão do terço mais rápido (`TEMPO_TERCO` 1.2 s).
- Sprites e sons provisórios: sprites/bar.png, carro.png, casa.png, estrada.png; sons/paredao.wav, sons/passagem.wav.
- Game over com mensagem variável (`mensagem_fim`): caninana ou laço.
- Som provisório: sons/armadilha.wav (estalo de madeira e corda).
- A decidir: nome definitivo da habilidade (pulso, eco das almas ou chamado das almas).
- Terço: decidido manual, tecla Z.

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
| Tamanho dos blocos do mapa | `TAMANHO_BLOCO` | config.py |
| Onde o jogador começa | `LINHA_INICIAL` e `COLUNA_INICIAL` | config.py |
| Cores do mapa | `COR_MATO`, `COR_TRILHA`, `COR_ARMADILHA`, `COR_SAIDA` | config.py |
| Tamanho da caixa de colisão | `TAMANHO_JOGADOR` | config.py |
| Tamanho da luz | `RAIOS_LUZ` (um por fase) | config.py |
| Quão escuro fica fora da luz | `ESCURIDAO` (255 = breu, 0 = sem escuro) | config.py |
| Tempo de recarga do pulso | `RECARGAS_PULSO` (um por fase) | config.py |
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
| Chance do vulto mostrar a cara | `CHANCE_ROSTO` (1.0 = sempre) | config.py |
| Duração, zoom e tremor da cara | `DURACAO_ROSTO`, `ZOOM_ROSTO_INICIAL`, `ZOOM_ROSTO_FINAL`, `TREMOR_ROSTO` | config.py |
| Volume do grito | `VOLUME_GRITO` | config.py |
| Cemitério (lápides e cruz) | letras `L` e `+` no `mapa` | main.py |
| Blocos que não dá para atravessar | `BLOCOS_SOLIDOS` | config.py |
| Caminho e velocidade da mulher | `ROTA_MULHER`, `VELOCIDADE_MULHER` | config.py |
| Distância que dispara o susto da mulher | `DIST_MULHER` | config.py |
| Quão visível ela é no escuro | `TRANSPARENCIA_MULHER` (0 a 255) | config.py |
| Flutuação | `FLUTUAR_ALTURA`, `FLUTUAR_VELOCIDADE` | config.py |
| Susto da mulher (tempo, zoom, tremor) | `DURACAO_SUSTO_MULHER`, `TEMPO_AVANCO`, `ZOOM_MULHER_INICIAL`, `ZOOM_MULHER_MEIO`, `CRESCIMENTO_MULHER`, `TREMOR_MULHER` | config.py |
| Braços e mãos do susto | `TEMPO_BRACOS`, `COTOVELO_X`, `COTOVELO_Y`, `MAO_ESQUERDA_Y`, `MAO_DIREITA_Y`, `ESCALA_MAO`, `GROSSURA_BRACO`, `COR_BRACO` | config.py |
| Volumes da mulher | `VOLUME_LAMENTO`, `VOLUME_GRITO_MULHER` | config.py |
| Quanto o arroz balança | `BALANCO_ARROZ`, `VELOCIDADE_BALANCO` | config.py |
| Onde fica a bicicleta | `BICICLETA_LINHA`, `BICICLETA_COLUNA` | config.py |
| Velocidade da bicicleta leve e pesada | `VELOCIDADE_BICICLETA`, `VELOCIDADE_PESADA` | config.py |
| Distância até ficar pesada de vez | `DIST_PESO_MAX` | config.py |
| Quando o homem aparece na garupa | `PESO_FANTASMA`, `TRANSPARENCIA_FANTASMA`, `DESVIO_FANTASMA` | config.py |
| Distância para pegar e para devolver | `DIST_PEGAR`, `DIST_DEVOLVER` | config.py |
| Tecla da bicicleta | `pygame.K_e` no `if` do KEYDOWN | main.py |
| Susto do homem | `DURACAO_SUSTO_HOMEM`, `TEMPO_SUBIDA`, `ZOOM_HOMEM`, `ANGULO_TORCAO`, `VELOCIDADE_TORCAO`, `TREMOR_HOMEM` | config.py |
| Suavidade da borda da luz | `NUCLEO_LUZ` (maior = borda mais dura), `ALCANCE_LUZ` (maior = some mais longe) | config.py |
| Posição da dica na tela | `DICA_Y` | config.py |
| Textos da história e do aviso | `TEXTO_HISTORIA`, `TITULO_AVISO`, `TEXTO_AVISO`, `TEXTO_TERCO` | config.py |
| Velocidade da digitação da história | `LETRAS_POR_SEGUNDO` | config.py |
| Volume da música de tensão | `VOLUME_TENSAO` | config.py |
| Tempo do clarão do terço | `TEMPO_TERCO`, `FADE_TERCO` | config.py |
| Cor e força do dourado | `COR_TERCO`, `BRILHO_TERCO` | config.py |
| Tecla do terço | `pygame.K_z` no `if` do KEYDOWN | main.py |
| Curral (lama) | letra `C` no `mapa` | main.py |
| Velocidade na lama | `VELOCIDADE_LAMA` | config.py |
| Vaca (lugar, velocidade, aviso, chifrada) | `VACA_LINHA`, `VACA_COLUNA`, `VELOCIDADE_VACA`, `VELOCIDADE_VACA_CALMA`, `TEMPO_BUFAR`, `DIST_CHIFRE` | config.py |
| Cores do curral | `COR_LAMA`, `COR_POCA`, `COR_CERCA` | config.py |
| Frequência do "ei, ei, ei" | `EI_MIN`, `EI_MAX`, `VOLUME_EI` | config.py |
| Os mapas das 3 fases | `MAPAS` e `DECORACOES` | mapas.py |
| Onde cada coisa fica em cada fase | `INICIOS`, `CASCAVEIS`, `BICICLETAS`, `VACAS`, `ROTAS_CANINANA`, `ROTAS_MULHER` | mapas.py |
| Bar, carro e casas | `CONSTRUCOES` | mapas.py |
| Luzes que clareiam o escuro (bar, janelas) | `LUZES` | mapas.py |
| Nome de cada fase | `NOMES_FASES` | mapas.py |
| Dificuldade de cada fase | `RAIOS_LUZ`, `RECARGAS_PULSO`, `VELOCIDADES_CANINANA`, `INTERVALOS_MIN`, `INTERVALOS_MAX` | config.py |
| Paredão (cores, piscadas, volume) | `CORES_PAREDAO`, `PISCADAS_POR_SEGUNDO`, `RAIO_COR_PAREDAO`, `DIST_SOM_PAREDAO`, `VOLUME_PAREDAO` | config.py |
| Tempo da tela de passagem | `TEMPO_PASSAGEM` | config.py |
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
