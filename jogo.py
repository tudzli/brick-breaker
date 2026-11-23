import pygame
import os
import json

#Inicializar jogo
pygame.init()

tamanho_tela = (800, 600)
tela = pygame.display.set_mode(tamanho_tela)

#Nome do jogo
pygame.display.set_caption("Brick Breaker")

#Save do jogo| manutenção do estado
PASTA = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_SAVE = os.path.join(PASTA, "save.json")
VELOCIDADE_BOLA = 1.5

#Bola
largura_bola = 15
altura_bola = 15
bola = pygame.Rect(400, 300, largura_bola, altura_bola)
pos_bola = pygame.Vector2(bola.topleft)
veloc_bola = pygame.Vector2()

#jogador
largura_jogador = 100
altura_jogador = 20
jogador = pygame.Rect(400 - largura_jogador // 2, 560, largura_jogador, altura_jogador)

qtd_blocos_linha = 50
qtd_linhas_blocos = 7
qtd_total_blocos = qtd_blocos_linha * qtd_linhas_blocos

#Segue sempre o padrão RGB (red, green, blue)
cores = {
    "branca": (255, 255, 255),
    "preto": (0, 0 ,0),
    "vermelho": (255, 0, 0),
    "amarelo": (255, 255, 0),
    "azul": (0, 0, 255),
    "verde": (0, 255, 0)
}

#Fontes
fonte_titulo = pygame.font.Font(None, 80)
fonte_media = pygame.font.Font(None, 50)
fonte_botao = pygame.font.Font(None, 40)
fonte_pequena = pygame.font.Font(None, 30)


#Blocos
def criar_blocos(qtd_blocos_linha, qtd_linhas_blocos):
    largura_tela = tamanho_tela[0]

    dist_blocos = 5
    largura_bloco = largura_tela / qtd_blocos_linha - dist_blocos

    altura_bloco = 15
    dist_linhas = altura_bloco + 10

    blocos = []
    #criar os blocos
    for j in range(qtd_linhas_blocos):
        for i in range(qtd_blocos_linha):
            bloco = pygame.Rect(i * (largura_bloco + dist_blocos), j * dist_linhas, largura_bloco, altura_bloco)
            blocos.append(bloco)
    return blocos


# criar as funções do jogo_________________________________
def apontar_bola(inclinacao):
    veloc_bola.update(inclinacao, -1)
    veloc_bola.scale_to_length(VELOCIDADE_BOLA)


def movimento_jogador():
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_d] or teclas[pygame.K_RIGHT]:
        if (jogador.x + largura_jogador) < tamanho_tela[0]:
            jogador.x = jogador.x + 1
    if teclas[pygame.K_a] or teclas[pygame.K_LEFT]:
        if jogador.x > 0:
            jogador.x = jogador.x - 1


def movimentar_bola(bola):
    pos_bola.x += veloc_bola.x
    pos_bola.y += veloc_bola.y
    bola.x = round(pos_bola.x)
    bola.y = round(pos_bola.y)


    if bola.x <= 0:
        veloc_bola.x = abs(veloc_bola.x)
    if bola.right >= tamanho_tela[0]:
        veloc_bola.x = -abs(veloc_bola.x)
    if bola.y <= 0:
        veloc_bola.y = abs(veloc_bola.y)

    #inferior da tela, se bater lá, finaliza o jogo.
    if bola.bottom >= tamanho_tela[1]:
        return False


    if jogador.colliderect(bola) and veloc_bola.y > 0:
        bola.bottom = jogador.top
        pos_bola.y = bola.y
        #angulo
        batida = (bola.centerx - jogador.centerx) / (largura_jogador / 2)
        apontar_bola(batida * 1.5)


    for bloco in blocos:
        if bloco.colliderect(bola):
            blocos.remove(bloco)
            dentro_x = min(bola.right, bloco.right) - max(bola.left, bloco.left)
            dentro_y = min(bola.bottom, bloco.bottom) - max(bola.top, bloco.top)
            if dentro_x < dentro_y:
                if veloc_bola.x > 0:
                    #indo pra direita
                    bola.right = bloco.left
                else:
                    #indo pra esquerda
                    bola.left = bloco.right
                veloc_bola.x *= -1
            else:
                if veloc_bola.y < 0:
                    #subindo
                    bola.top = bloco.bottom
                else:
                    #descendo
                    bola.bottom = bloco.top
                veloc_bola.y *= -1
            pos_bola.update(bola.x, bola.y) #Sincroniza a pos
            break

    return True


def atualizar_pontuacao(pontuacao):
    texto = fonte_pequena.render(f"Pontuação: {pontuacao}", 1, cores["amarelo"])
    tela.blit(texto, (0, 580))
    return pontuacao >= qtd_total_blocos

#save / load

def salvar_jogo():
    estado = {
        "bola": [pos_bola.x, pos_bola.y],
        "veloc_bola": [veloc_bola.x, veloc_bola.y],
        "jogador_x": jogador.x,
        "blocos": [[b.x, b.y, b.width, b.height] for b in blocos],
    }
    with open(ARQUIVO_SAVE, "w", encoding="utf-8") as f:
        json.dump(estado, f, indent=2)

def carregar_jogo():
    try:
        with open(ARQUIVO_SAVE, "r", encoding="utf-8") as f:
            e = json.load(f)
        bx, by = e["bola"]
        vx, vy = e["veloc_bola"]
        jx = e["jogador_x"]
        novos = [pygame.Rect(*b) for b in e["blocos"]]
    except (OSError, json.JSONDecodeError, KeyError, ValueError, TypeError):
        return False #sem save ou quebrado

    pos_bola.update(bx, by)
    bola.topleft = (round(bx), round(by))
    veloc_bola.update(vx, vy)
    jogador.x = jx
    blocos[:] = novos
    return True


#reinicio de jogo
def reiniciar_jogo():
    bola.x, bola.y = 400, 300
    pos_bola.update(bola.x, bola.y)
    jogador.x = 400 - largura_jogador // 2
    apontar_bola(1)
    blocos[:] = criar_blocos(qtd_blocos_linha, qtd_linhas_blocos)




#desenho_______________________________________
def desenhar_inicio_jogo():
    tela.fill(cores["preto"])
    #onde, que cor, o que.
    pygame.draw.rect(tela, cores["azul"], jogador)
    pygame.draw.ellipse(tela, cores["amarelo"], bola)

def desenhar_blocos(blocos):
    for bloco in blocos:
        pygame.draw.rect(tela, cores["vermelho"], bloco)

def desenhar_campo():
    desenhar_inicio_jogo()
    desenhar_blocos(blocos)
    return atualizar_pontuacao(qtd_total_blocos - len(blocos))

def desenhar_texto(texto, fonte, cor, centro):
    imagem = fonte.render(texto, 1, cor)
    tela.blit(imagem, imagem.get_rect(center=centro))

#menus
def criar_botoes(nomes, topo):
    return {nome: pygame.Rect(tamanho_tela[0]//2 - 130, topo + i * 60, 260, 50)
        for i, nome in enumerate(nomes)}

def desenhar_botoes(botoes):
    for nome, rect in botoes.items():
        pygame.draw.rect(tela, cores["azul"], rect)
        desenhar_texto(nome, fonte_botao, cores["branca"], rect.center)

def clicar_botao(botoes, pos):
    for nome, rect in botoes.items():
        if rect.collidepoint(pos):
            return nome
    return None

botoes_menu = criar_botoes(["Novo Jogo", "Carregar Jogo", "Sair"], 250)
botoes_pausa = criar_botoes(["Retomar", "Salvar","Reiniciar", "Sair"], 220)
botoes_fim = criar_botoes(["REINICIAR"], 400)
painel_pausa = pygame.Rect(tamanho_tela[0]//2 - 200, 130, 400, 380)

aviso = "" #Mensagem ao salvar/carregar


def desenhar_menu():
    tela.fill(cores["preto"])
    desenhar_texto("BRICK BREAKER", fonte_titulo, cores["amarelo"], (tamanho_tela[0]//2, 150))
    desenhar_botoes(botoes_menu)
    desenhar_texto(aviso, fonte_pequena, cores["vermelho"], (tamanho_tela[0]//2, 460))

def desenhar_pausa():
    desenhar_campo()
    pygame.draw.rect(tela, cores["preto"], painel_pausa)
    pygame.draw.rect(tela, cores["branca"], painel_pausa, 3)
    desenhar_texto("PAUSADO", fonte_titulo, cores["branca"], (tamanho_tela[0]//2, 170))
    desenhar_botoes(botoes_pausa)
    desenhar_texto(aviso, fonte_pequena, cores["verde"], (tamanho_tela[0]//2, 470))


blocos = criar_blocos(qtd_blocos_linha, qtd_linhas_blocos)
apontar_bola(1)

#criar um loop infinito para o jogo________________________________________________
estado_jogo = "menu" #menu, jogando, pausado, derrota, vitoria
fim_de_jogo = False


while fim_de_jogo == False:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            fim_de_jogo = True

        if evento.type == pygame.KEYDOWN and evento.key in (pygame.K_p, pygame.K_ESCAPE):
            aviso = ""
            if estado_jogo == "jogando":
                estado_jogo = "pausado"
            elif estado_jogo == "pausado":
                estado_jogo = "jogando"

        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            aviso = ""
            if estado_jogo == "menu":
                clique = clicar_botao(botoes_menu, evento.pos)
                if clique == "Novo Jogo":
                    reiniciar_jogo()
                    estado_jogo = "jogando"
                elif clique == "Carregar Jogo":
                    if carregar_jogo():
                        estado_jogo = "jogando"
                    else:
                        aviso = "Nenhum save encontrado"
                elif clique == "Sair":
                    fim_de_jogo = True

            elif estado_jogo == "pausado":
                clique = clicar_botao(botoes_pausa, evento.pos)
                if clique == "Retomar":
                    estado_jogo = "jogando"
                elif clique == "Salvar":
                    salvar_jogo()
                    aviso = "Jogo salvo!"
                elif clique == "Reiniciar":
                    reiniciar_jogo()
                    aviso = "Jogo Reiniciado!"
                elif clique == "Sair":
                    fim_de_jogo = True

            elif estado_jogo in ("derrota", "vitoria"):
                if clicar_botao(botoes_fim, evento.pos) == "REINICIAR":
                    reiniciar_jogo()
                    estado_jogo = "jogando"

    if estado_jogo == "menu":
        desenhar_menu()

    elif estado_jogo == "jogando":
        venceu = desenhar_campo()

        movimento_jogador()
        bola_viva = movimentar_bola(bola)

        if not bola_viva:
            estado_jogo = "derrota"
        elif venceu:
            estado_jogo = "vitoria"

    elif estado_jogo == "pausado":
        desenhar_pausa()

    elif estado_jogo == "derrota":
        tela.fill(cores["preto"])
        desenhar_texto("FIM DE JOGO", fonte_titulo, cores["vermelho"], (tamanho_tela[0]//2, tamanho_tela[1]//2 - 35))
        desenhar_texto(f"Pontuação: {qtd_total_blocos - len(blocos)}", fonte_media, cores["amarelo"],
                       (tamanho_tela[0]//2, tamanho_tela[1]//2 + 40))
        desenhar_botoes(botoes_fim)

    elif estado_jogo == "vitoria":
        tela.fill(cores["verde"])
        desenhar_texto("VOCÊ VENCEU!", fonte_titulo, cores["amarelo"], (tamanho_tela[0]//2, tamanho_tela[1]//2 - 15))
        desenhar_botoes(botoes_fim)

    #tempo para rodar a atualização do jogo, a cada 1 milisegundo
    pygame.time.wait(1)
    #flip atualiza a tela do jogo
    pygame.display.flip()

pygame.quit()

#criar um loop infinito para o jogo________________________________________________
