import pygame
import random

pygame.init()

tela = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Adivinhe a Imagem Matemática")

BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
AZUL = (0, 0, 255)
DESTAQUE = (0, 255, 0)
CINZA = (169, 169, 169)
VERDE = (0, 255, 0)
SOMBRA = (150, 150, 150)

fonte_titulo = pygame.font.Font(None, 60)
fonte_problema = pygame.font.Font(None, 50)
fonte_entrada = pygame.font.Font(None, 40)

imagem = pygame.image.load("bibliotecaaa.png")
imagem = pygame.transform.scale(imagem, (800, 400))

partes_imagem = [
    imagem.subsurface((0, 0, 400, 200)),
    imagem.subsurface((400, 0, 400, 200)),
    imagem.subsurface((0, 200, 400, 200)),
    imagem.subsurface((400, 200, 400, 200))
]

def gerar_problema():
    a = random.randint(1, 10)
    b = random.randint(1, 10)
    resposta = random.randint(-10, 10)
    problema = f"{a}x + {b} = {a * resposta + b}"
    return problema, resposta

class BlocoImagem(pygame.sprite.Sprite):
    def __init__(self, x, y, parte, problema, resposta):
        super().__init__()
        self.image = pygame.Surface((400, 200))
        self.image.fill(BRANCO)
        pygame.draw.rect(self.image, AZUL, self.image.get_rect(), 5)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.parte = parte
        self.problema = problema
        self.resposta = resposta
        self.revelado = False
        self.texto_entrada = ""
        self.tentativas = 0
        self.max_tentativas = 2

    def revelar(self):
        self.image.blit(self.parte, (0, 0))
        self.revelado = True

    def desenhar_problema(self, superficie):
        texto_problema = fonte_problema.render(self.problema, True, PRETO)
        texto_entrada = fonte_problema.render(self.texto_entrada, True, PRETO)
        superficie.blit(self.image, self.rect.topleft)
        superficie.blit(texto_problema, (self.rect.x + self.rect.width // 2 - texto_problema.get_width() // 2, self.rect.y + self.rect.height // 2 - texto_problema.get_height() // 2))
        superficie.blit(texto_entrada, (self.rect.x + self.rect.width // 2 - texto_entrada.get_width() // 2, self.rect.y + self.rect.height // 2 + 40))

    def lidar_entrada(self, evento):
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_BACKSPACE:
                self.texto_entrada = self.texto_entrada[:-1]
            elif evento.key == pygame.K_RETURN:
                return self.texto_entrada
            else:
                self.texto_entrada += evento.unicode
        return None

    def atualizar(self, pos_mouse):
        if self.rect.collidepoint(pos_mouse) and not self.revelado:
            pygame.draw.rect(self.image, DESTAQUE, self.image.get_rect(), 5)
        else:
            pygame.draw.rect(self.image, AZUL, self.image.get_rect(), 5)

    def bloquear_bloco(self):
        self.image.fill(CINZA)

blocos = pygame.sprite.Group()
posicoes = [(0, 100), (400, 100), (0, 300), (400, 300)]
for pos, parte in zip(posicoes, partes_imagem):
    problema, resposta = gerar_problema()
    bloco = BlocoImagem(*pos, parte, problema, resposta)
    blocos.add(bloco)

def desenhar_caixa_entrada(superficie, texto_entrada, x, y, largura=300, altura=50):
    caixa_entrada = pygame.Rect(x, y, largura, altura)
    pygame.draw.rect(superficie, PRETO, caixa_entrada, 2)
    texto_surface = fonte_entrada.render(texto_entrada, True, PRETO)
    superficie.blit(texto_surface, (caixa_entrada.x + 10, caixa_entrada.y + 10))

def desenhar_titulo(superficie, texto, x, y):
    sombra_surface = fonte_titulo.render(texto, True, SOMBRA)
    texto_surface = fonte_titulo.render(texto, True, PRETO)
    superficie.blit(sombra_surface, (x + 2, y + 2))
    superficie.blit(texto_surface, (x, y))

def tela_vitoria():
    tela.fill(BRANCO)
    texto_vitoria = fonte_titulo.render("Você Ganhou!", True, VERDE)
    tela.blit(texto_vitoria, (250, 250))
    pygame.display.flip()
    pygame.time.delay(3000)

rodando = True
bloco_atual = None
blocos_revelados = 0
max_revelacoes = 4
texto_adivinhar = ""
vitoria = False

while rodando:
    pos_mouse = pygame.mouse.get_pos()
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

        if bloco_atual:
            entrada_usuario = bloco_atual.lidar_entrada(evento)
            if entrada_usuario is not None and entrada_usuario.lstrip('-').isdigit():
                if int(entrada_usuario) == bloco_atual.resposta:
                    bloco_atual.revelar()
                    blocos_revelados += 1
                    bloco_atual = None
                else:
                    bloco_atual.tentativas += 1
                    bloco_atual.texto_entrada = ""
                    if bloco_atual.tentativas >= bloco_atual.max_tentativas:
                        bloco_atual.bloquear_bloco()
                        bloco_atual = None

        elif evento.type == pygame.MOUSEBUTTONDOWN and blocos_revelados < max_revelacoes:
            for bloco in blocos:
                if bloco.rect.collidepoint(evento.pos):
                    bloco_atual = bloco if not bloco.revelado else None

        if evento.type == pygame.KEYDOWN and not bloco_atual:
            if evento.key == pygame.K_BACKSPACE:
                texto_adivinhar = texto_adivinhar[:-1]
            elif evento.key == pygame.K_RETURN and blocos_revelados > 0:
                if texto_adivinhar.lower() == "biblioteca":
                    vitoria = True
                    rodando = False
                else:
                    texto_adivinhar = ""
            else:
                texto_adivinhar += evento.unicode

    for bloco in blocos:
        bloco.atualizar(pos_mouse)

    tela.fill(BRANCO)
    desenhar_titulo(tela, "Adivinhe a Imagem Matemática", 150, 20)
    blocos.draw(tela)
    desenhar_caixa_entrada(tela, texto_adivinhar, 250, 520, 300, 50)

    if bloco_atual:
        bloco_atual.desenhar_problema(tela)

    pygame.display.flip()

if vitoria:
    tela_vitoria()

pygame.quit()
