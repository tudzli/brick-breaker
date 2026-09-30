import pygame


#Inicializar jogo
pygame.init()

tamanho_tela = (800, 600)
tela = pygame.display.set_mode(tamanho_tela)

#Nome do jogo
pygame.display.set_caption("Brick Breaker")

largura_bola = 15
altura_bola = 15
bola = pygame.Rect(400, 300, largura_bola, altura_bola)
largura_jogador = 100
altura_jogador = 20
jogador = pygame.Rect(400 - largura_jogador // 2, 560, largura_jogador, altura_jogador)

qtd_blocos_linha = 8
qtd_linhas_blocos = 4
qtd_total_blocos = qtd_blocos_linha * qtd_linhas_blocos


def criar_blocos(qtd_blocos_linhas, qtd_linhas_blocos):
    altura_tela = tamanho_tela[1]
    largura_tela = tamanho_tela[0]

    dist_blocos = 5
    largura_bloco = largura_tela / 8 - dist_blocos

    altura_bloco = 15
    dist_linhas = altura_bloco + 10

    blocos = []
    #criar os blocos
    for j in range(qtd_linhas_blocos):
        for i in range(qtd_blocos_linha):
            bloco = pygame.Rect(i * (largura_bloco + dist_blocos), j * dist_linhas, largura_bloco, altura_bloco)
            blocos.append(bloco)
    return blocos

#Segue sempre o padrão RGB (red, green, blue)
cores = {
    "branca": (255, 255, 255),
    "preto": (0, 0 ,0),
    "vermelho": (255, 0, 0),
    "amarelo": (255, 255, 0),
    "azul": (0, 0, 255),
    "verde": (0, 255, 0)
}
pontuacao = 0

#pq não tupla, e sim uma lista?
#pq tuplas são imutaveis, e o movimento a partir de uma colisão deve ser invertido.
veloc_bola = [1, -1]



# criar as funções do jogo_________________________________
def movimento_jogador(evento):
    if evento.type == pygame.KEYDOWN:
        if evento.key == pygame.K_d or evento.key == pygame.K_RIGHT:
            if (jogador.x + largura_jogador) < tamanho_tela[0]:
                jogador.x = jogador.x + 1
        if evento.key == pygame.K_a or evento.key == pygame.K_LEFT:
            if jogador.x > 0:
                jogador.x = jogador.x - 1


def movimentar_bola(bola):
    movimento = veloc_bola
    bola.x = bola.x + movimento[0]
    bola.y = bola.y + movimento[1]

    if bola.x <= 0:
        movimento[0] = movimento[0] * -1
    if bola.y <= 0:
        movimento[1] = movimento[1] * -1

    if bola.x + largura_bola >= tamanho_tela[0]:
        movimento[0] = movimento[0] * -1

    #inferior da tela, se bater lá, finaliza o jogo.
    if bola.y + altura_bola >= tamanho_tela[1]:
        movimento = None


    if jogador.collidepoint(bola.x, bola.y):
        movimento[1] = movimento[1] * -1
    for bloco in blocos:
        if bloco.collidepoint(bola.x, bola.y):
            blocos.remove(bloco)
            movimento[1] = movimento[1] * -1

    return movimento


def atualizar_pontuacao(pontuacao):
    fonte = pygame.font.Font(None, 30)
    texto = fonte.render(f"Pontuação: {pontuacao}", 1, cores["amarelo"])
    tela.blit(texto, (0, 580))
    if pontuacao >= qtd_total_blocos:
        return True
    else:
        return False



# criar as funções do jogo_________________________________

#desenhar as coisas na tela_______________________________________
def desenhar_inicio_jogo():
    tela.fill(cores["preto"])
    #onde, que cor, o que.
    pygame.draw.rect(tela, cores["azul"], jogador)
    pygame.draw.ellipse(tela, cores["amarelo"], bola)

def desenhar_blocos(blocos):
    for bloco in blocos:
        pygame.draw.rect(tela, cores["vermelho"], bloco)

desenhar_inicio_jogo()
blocos = criar_blocos(qtd_blocos_linha, qtd_linhas_blocos)
#desenhar as coisas na tela_______________________________________



#criar um loop infinito para o jogo________________________________________________
estado_jogo = "pausado"
fim_de_jogo = False


while fim_de_jogo == False:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            fim_de_jogo = True

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_p or evento.key == pygame.K_ESCAPE:
                if estado_jogo == "jogando":
                    estado_jogo = "pausado"
                elif estado_jogo == "pausado":
                    estado_jogo = "jogando"

        if estado_jogo == "jogando":
            movimento_jogador(evento)

    #movimento_jogador(evento)

    if estado_jogo == "jogando":
        desenhar_inicio_jogo()
        desenhar_blocos(blocos)
        venceu = atualizar_pontuacao(qtd_total_blocos - len(blocos))

        #movimento_jogador(evento)
        movimento_bola = movimentar_bola(bola)

        if movimento_bola == None:
            estado_jogo = "derrota"

        elif venceu:
            estado_jogo = "vitoria"

    elif estado_jogo == "pausado":
        fonte_pause = pygame.font.Font(None, 60)
        texto_pause = fonte_pause.render("JOGO PAUSADO", 1, cores["branca"])
        tela.blit(texto_pause, (tamanho_tela[0]//2 - 160, tamanho_tela[1]//2))

    elif estado_jogo == "derrota":
        tela.fill(cores["preto"])

        fonte_grande = pygame.font.Font(None, 80)
        fonte_media = pygame.font.Font(None, 50)

        texto_fim = fonte_grande.render("FIM DE JOGO", 1, cores["vermelho"])
        texto_pontos = fonte_media.render(f"Pontuação: {qtd_total_blocos - len(blocos)}", 1, cores["amarelo"])
        tela.blit(texto_fim, (tamanho_tela[0]//2 - 180, tamanho_tela[1]//2 - 60))
        tela.blit(texto_pontos, (tamanho_tela[0]//2 - 160, tamanho_tela[1]//2 + 20))

    elif estado_jogo == "vitoria":
        tela.fill(cores["verde"])
        fonte_grande = pygame.font.Font(None, 80)
        texto_vitoria = fonte_grande.render("VOCÊ VENCEU!", 1, cores["amarelo"])
        tela.blit(texto_vitoria, (tamanho_tela[0]//2 - 200, tamanho_tela[1]//2 - 40))


    #tempo para rodar a atualização do jogo, a cada 1 milisegundo
    pygame.time.wait(1)
    #flip atualiza a tela do jogo
    pygame.display.flip()

pygame.quit()

#criar um loop infinito para o jogo________________________________________________