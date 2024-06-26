import pygame
import random
import os
from tkinter import simpledialog

pygame.init()

relogio = pygame.time.Clock()
icone  = pygame.image.load("recursos/icone.png")
guardian = pygame.image.load("recursos/guardian.png")
fundo = pygame.image.load("recursos/fundo.png")
fundoStart = pygame.image.load("recursos/fundoStart.png")
fundoDead = pygame.image.load("recursos/morte.png")
bola = pygame.image.load("recursos/bola.png")
sword = pygame.image.load("recursos/sword.png")
tamanho = (800,600)
tela = pygame.display.set_mode( tamanho ) 
pygame.display.set_caption("projetoMoon")
pygame.display.set_icon(icone)
castSound = pygame.mixer.Sound("recursos/cast.wav")
bolaSound = pygame.mixer.Sound("recursos/bola.wav")
youdiedSound = pygame.mixer.Sound("recursos/youdied.wav")
fonte = pygame.font.SysFont("comicsans",28)
fonteStart = pygame.font.SysFont("comicsans",55)
fonteMorte = pygame.font.SysFont("arial",120)
pygame.mixer.music.load("recursos/battle.mp3")

branco = (255,255,255)
preto = (0,0,0 )
amarelo = (255,255,0)

def jogar(nome):
    pygame.mixer.Sound.play(bolaSound)
    pygame.mixer.Sound.play(castSound)
    pygame.mixer.music.play(-1)
    posicaoXPersona = 550
    posicaoYPersona = 450
    movimentoXPersona  = 0
    movimentoYPersona  = 0
    posicaoXBola = 400
    posicaoYBola = -240
    velocidadeBola = 1
    posicaoXSword = 400
    posicaoYSword = -240
    velocidadeSword = 1
    pontos = 0
    larguraPersona = 250
    alturaPersona = 127
    larguraSword  = 50
    alturaSword  = 250
    larguraBola = 40
    alturaBola = 205
    dificuldade  = 20

    #circulo amarelo 
    raio = 50
    pulse = 1
    maximo_raio = 60
    minimo_raio =40

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_RIGHT:
                movimentoXPersona = 10
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_LEFT:
                movimentoXPersona = -10
            elif evento.type == pygame.KEYUP and evento.key == pygame.K_RIGHT:
                movimentoXPersona = 0
            elif evento.type == pygame.KEYUP and evento.key == pygame.K_LEFT:
                movimentoXPersona = 0
                    
        posicaoXPersona = posicaoXPersona + movimentoXPersona            
        posicaoYPersona = posicaoYPersona + movimentoYPersona            
        
        if posicaoXPersona < 0 :
            posicaoXPersona = 10
        elif posicaoXPersona >550:
            posicaoXPersona = 540
            
        if posicaoYPersona < 0 :
            posicaoYPersona = 10
        elif posicaoYPersona > 473:
            posicaoYPersona = 463
        
            
        tela.fill(branco)
        tela.blit(fundo, (0,0) )    
        raio += pulse
        if raio >= maximo_raio or raio <=minimo_raio:
            pulse = -pulse 
        pygame.draw.circle(tela, amarelo, (750,100), raio )
        
        tela.blit( guardian, (posicaoXPersona, posicaoYPersona) )
        
        posicaoYSword = posicaoYSword + velocidadeSword
        if posicaoYSword > 600:
            posicaoYSword = -240
            pontos = pontos + 1
            velocidadeSword = velocidadeSword + 1
            posicaoXSword = random.randint(0,800)
            pygame.mixer.Sound.play(castSound)
            
        posicaoYBola = posicaoYBola + velocidadeBola
        if posicaoYBola > 600:
            posicaoYBola = -240
            pontos = pontos + 1
            velocidadeBola = velocidadeBola + 1
            posicaoXSword = random.randint(0,800)
            pygame.mixer.Sound.play(bolaSound)                   
            
            
        tela.blit( sword, (posicaoXSword, posicaoYSword) )                       
        tela.blit( bola, (posicaoXBola, posicaoYBola) )
        
        texto = fonte.render(nome+"- Pontos: "+str(pontos), True, branco)
        tela.blit(texto, (10,10))
        
        pixelsPersonaX = list(range(posicaoXPersona, posicaoXPersona+larguraPersona))
        pixelsPersonaY = list(range(posicaoYPersona, posicaoYPersona+alturaPersona))
        pixelsSwordX = list(range(posicaoXSword, posicaoXSword + larguraSword))
        pixelsSwordY = list(range(posicaoYSword, posicaoYSword + alturaSword))
        pixelsBolaX = list(range(posicaoXBola, posicaoXBola + larguraBola))
        pixelsBolaY = list(range(posicaoYBola, posicaoYBola + alturaBola))
        
        #print( len( list( set(pixelsSwordX).intersection(set(pixelsPersonaX))   ) )   )
        if  len( list( set(pixelsSwordY).intersection(set(pixelsPersonaY))) ) > dificuldade:
            if len( list( set(pixelsSwordX).intersection(set(pixelsPersonaX))   ) )  > dificuldade:
                dead(nome, pontos)
        if  len( list( set(pixelsBolaY).intersection(set(pixelsPersonaY))) ) > dificuldade:
            if len( list( set(pixelsBolaX).intersection(set(pixelsPersonaX))   ) )  > dificuldade:
                dead(nome, pontos)
        
    
        
        pygame.display.update()
        relogio.tick(60)


def dead(nome, pontos):
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(youdiedSound)
    
    jogadas  = {}
    try:
        arquivo = open("historico.txt","r",encoding="utf-8")
        jogadas = eval(arquivo.read())
        arquivo.close()
    except:
        arquivo = open("historico.txt","w",encoding="utf-8")
        arquivo.close()
 
    jogadas[nome] = pontos   
    arquivo = open("historico.txt","w",encoding="utf-8") 
    arquivo.write(str(jogadas))
    arquivo.close()
    
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                jogar(nome)

            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if buttonStart.collidepoint(evento.pos):
                    jogar(nome)
        tela.fill(branco)
        tela.blit(fundoDead, (0,0))
        buttonStart = pygame.draw.rect(tela, preto, (35,482,750,100),0)
        textoStart = fonteStart.render("RESTART", True, branco)
        tela.blit(textoStart, (400,482))
        textoEnter = fonte.render("Press enter to continue...", True, branco)
        tela.blit(textoEnter, (60,482))
        pygame.display.update()
        relogio.tick(60)


def ranking():
    estrelas = {}
    try:
        arquivo = open("historico.txt","r",encoding="utf-8" )
        estrelas = eval(arquivo.read())
        arquivo.close()
    except:
        pass
    
    nomes = sorted(estrelas, key=estrelas.get,reverse=True)
    print(estrelas)
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if buttonStart.collidepoint(evento.pos):
                    start()

        tela.fill(preto)
        buttonStart = pygame.draw.rect(tela, preto, (35,482,750,100),0)
        textoStart = fonteStart.render("BACK TO START", True, branco)
        tela.blit(textoStart, (330,482))
        
        
        posicaoY = 50
        for key,nome in enumerate(nomes):
            if key == 13:
                break
            textoJogador = fonte.render(nome + " - "+str(estrelas[nome]), True, branco)
            tela.blit(textoJogador, (300,posicaoY))
            posicaoY = posicaoY + 30

            
        
        pygame.display.update()
        relogio.tick(60)


def start():
    nome = simpledialog.askstring("Moon","Nome Completo:")
    
    
    
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if buttonStart.collidepoint(evento.pos):
                    jogar(nome)
                elif buttonRanking.collidepoint(evento.pos):
                    ranking()

        tela.fill(branco)
        tela.blit(fundoStart, (0,0))
        buttonStart = pygame.draw.rect(tela, preto, (35,482,750,100),0)
        buttonRanking = pygame.draw.rect(tela, preto, (35,50,200,50),0,30)
        textoRanking = fonte.render("Ranking", True, branco)
        tela.blit(textoRanking, (90,50))
        textoStart = fonteStart.render("START", True, branco)
        tela.blit(textoStart, (330,482))

        
        
        pygame.display.update()
        relogio.tick(60)

start()