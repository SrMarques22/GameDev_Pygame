import random

import pygame

pygame.init()

#Tamanho da Janela e inicialização:
x = 1280
y = 720

screen = pygame.display.set_mode((x,y)) # Setar o tamanho da tela definida acima
pygame.display.set_caption('GameDev Pygame') # Setar o nome do game na janela

# Background
bg = pygame.image.load('images/pixel_bg.jpg').convert_alpha() # Essa é a imagem que fica sempre fixa
bg = pygame.transform.scale(bg,(x,y)) #Vai transformar meu background no tamanho da janela que definimos

#Personagens:
alien = pygame.image.load('images/Slug.jpg').convert_alpha()
alien = pygame.transform.scale(alien,(50,50))

playerImg = pygame.image.load('images/NAVE.JPG').convert_alpha()
playerImg = pygame.transform.scale(playerImg,(50,50))
playerImg = pygame.transform.rotate(playerImg,-90) # girar a imagem na posição que prefirir

missel = pygame.image.load('images/tiro.jpg').convert_alpha()
missel = pygame.transform.scale(missel,(25,25))
#missel = pygame.transform.rotate(missel,-45) # girar a imagem na posição que prefirir

missel = pygame.image.load('images/tiro.jpg').convert_alpha()
missel = pygame.transform.scale(missel,(25,25))

heart = pygame.image.load('images/heart.png').convert_alpha()
heart = pygame.transform.scale(heart,(80,80))

#Definindo as posições dos personagens na tela
pos_alien_x = 500
pos_alien_y = 360

velocidade_y_player = 0
pos_player_x = 200
pos_player_y = 300

velocidade_x_missil = 0
pos_x_missil = 200
pos_y_missil = 300

vida = 4


triggered = False

pontos = 0

rodando = True

font = pygame.font.SysFont('/font/colossus.ttf',50)



#Criando as colições, o rect deixou os itens permitidos de colisão
player_rect = playerImg.get_rect()
alien_rect = alien.get_rect()
missil_rect = missel.get_rect()

# Função de Respaw do Alien:
def respawn():
    x = 1350 #posição do Alien vertical sempre será no canto direito da tela
    y = random.randint(1,640) # posição horizontal do Alien será aleatória dentro dos limites da tela
    return [x,y]

# Função de Respaw do missel:
def respawn_missil():
    triggered = False
    respawn_missil_x = pos_player_x
    respawn_missil_y = pos_player_y
    velocidade_x_missil = 0
    return [respawn_missil_x,respawn_missil_y,triggered,velocidade_x_missil]


#configurando a colisão do missil  nave e alien
def colisions():
    global pontos
    global vida

    if player_rect.colliderect(alien_rect) or alien_rect.x == 60:
        #pontos -= 1
        vida -= 1
        return True
    elif missil_rect.colliderect(alien_rect):
        pontos += 1
        return True
    else:
        return False

#Looping para que a tela fique rodando até a tecla pressionada(x) pra fechar a janela seja parada
while rodando:

    for event in pygame.event.get():
        if event.type == pygame.QUIT: # se o tipo do evento for "QUIT" que é o X para fechar a janela, o programa para!
            rodando = False
    screen.blit(bg,(0,0)) # Essa função informa que a janela de backgroud será carregado junto com a janela

    #Abaixo vamos criar uma forma de a imagem de fundo ficar se movendo para ficar mais bonito, só que, como a imagem tem seu tamanho fixo, ao se deslocar ela vai
    # ficar com uma parte preta, que seria o fundo real, então vamos criar um looping para que sempre seja preenchido o fundo mesmo com o deslocamneto a imagem
    # a imagem de fundo vai trabalhar como se fosse um carrocel (sai uma entra outra).

    rel_x = x % bg.get_rect().width #vai pegar o RESTO (x) do tamanho que sobrar da imagem e realocar
    screen.blit(bg,(rel_x - bg.get_rect().width,0)) #Cria o background novo de acordo com o espaço vazio
    if rel_x < 1280:
        screen.blit(bg,(rel_x,0)) # quando a imagem chegar no fim, vai carregar outra imagem

    # Controles:

    tecla = pygame.key.get_pressed()
    if tecla[pygame.K_UP] and pos_player_y > 1: # O argumento MENOR que 1 é pra ele não sair da tela
        pos_player_y -=1
        if not triggered: # se o botão de tiro não for acionado o missil que fica por baixo da imagem fica seguindo a mesma posição da nave
            pos_y_missil -=1

    if tecla[pygame.K_DOWN] and pos_player_y < 665: # O argumento MENOR que 665 é pra ele não sair da tela
        pos_player_y += 1
        if not triggered: # se o botão de tiro não for acionado o missil que fica por baixo da imagem fica seguindo a mesma posição da nave
            pos_y_missil += 1

    if tecla[pygame.K_SPACE]:
        triggered = True # quando o botão for pressionado ele vai atirar
        velocidade_x_missil = 1.5 # além de atirar o missel vai se mover

    # Fechar o programa se atingir a pontuação -1
    if vida == 0:
        rodando = False


    # Respawn:
    if pos_alien_x == 50 :
        pos_alien_x = respawn()[0]
        pos_alien_y = respawn()[1]
        # Respawn Missil:
        # se passar do tamanho da tela de 1300 ele vai aplicar o def respawn do missil
    if pos_x_missil >= 1300:
        pos_x_missil,pos_y_missil,triggered,velocidade_x_missil = respawn_missil()

    if pos_alien_x == 50 or colisions():
        pos_alien_x = respawn()[0]
        pos_alien_y = respawn()[1]
    #Velocidade de Movimento de troca de imagem
    x -= 0.5

    #Colocando os icones de coração:
    if vida == 3:
        screen.blit(heart, (150, 17))
        screen.blit(heart, (190, 17))
        screen.blit(heart, (230, 17))

    if vida == 2:
        screen.blit(heart, (150, 17))
        screen.blit(heart, (190, 17))
    if vida == 1:
        screen.blit(heart, (150, 17))


    pos_alien_x -=1 # Dar a posição do Alien para ele ir da equerda pra direita
    pos_x_missil += velocidade_x_missil

    #Criar a cor na tela
    pygame.draw.rect(screen,(255,0,0), player_rect,4)
    pygame.draw.rect(screen, (255, 0, 0), missil_rect, 4)
    pygame.draw.rect(screen, (255, 0, 0), alien_rect, 4)

    #deixar as margens do Draw acima de acordo com a posição de cada item
    #Posição do React:
    player_rect.y = pos_player_y
    player_rect.x = pos_player_x

    missil_rect.y = pos_y_missil
    missil_rect.x = pos_x_missil

    alien_rect.y = pos_alien_y
    alien_rect.x = pos_alien_x


    #Criar as imagens na tela:

    screen.blit(alien,(pos_alien_x,pos_alien_y)) # o comando BLIT, serve para mostar a imagem na tela, aqui estamos mostrando as imagens criadas nas posições descritas nos personagens
    screen.blit(missel, (pos_x_missil, pos_y_missil))  # colocamos ela acima da imagem do player para não sobrepor a imagem da NAVE
    screen.blit(playerImg,(pos_player_x,pos_player_y))


    score = font.render(f' Pontos: {int(pontos)} ', True, (0,0,0))
    vidas = font.render(f' Vidas:  ', True, (0, 0, 0))
    screen.blit(score, (1000,47)) # Posição do nome pontos
    screen.blit(vidas, (50, 47))  # Posição do nome pontos



    pygame.display.update()


