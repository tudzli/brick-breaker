# Brick Breaker

Um jogo de Brick Breaker (quebra-blocos) feito em Python com a biblioteca pygame.

A bola quica pelas paredes e pelo topo da tela. Voce controla a raquete azul
na parte de baixo e precisa rebater a bola para destruir todos os blocos
vermelhos. Se a bola passar pela raquete e tocar o fundo da tela, o jogo acaba.

## Como jogar

| Tecla | Acao |
|---|---|
| `A` ou seta esquerda | move a raquete para a esquerda |
| `D` ou seta direita | move a raquete para a direita |
| `P` ou `Esc` | pausa / continua o jogo |

O jogo comeca pausado: aperte `P` para iniciar.

## Regras

- 8 blocos por linha, 4 linhas: 32 blocos no total.
- Cada bloco destruido vale 1 ponto, mostrado no canto inferior da tela.
- Destruir todos os 32 blocos: tela de **VOCE VENCEU**.
- Deixar a bola cair no fundo da tela: tela de **FIM DE JOGO** com a pontuacao final.

## Como rodar

Precisa de Python 3 e do pygame:

```bash
pip install pygame
python jogo.py
```

No Python 3.14 ainda nao existe wheel do pygame original. Nesse caso use o
fork da comunidade, que tem a mesma API e o mesmo `import pygame`:

```bash
pip install pygame-ce
```

## Estrutura

Tudo fica em `jogo.py`: a criacao dos blocos, o movimento da bola e da
raquete, a deteccao de colisoes, a pontuacao e o loop principal do jogo.
