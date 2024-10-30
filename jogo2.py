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
VERMELHO = (255, 0, 0)
SOMBRA = (150, 150, 150)

fonte_titulo = pygame.font.Font(None, 60)
fonte_problema = pygame.font.Font(None, 50)
fonte_entrada = pygame.font.Font(None, 40)
fonte_instrucao = pygame.font.Font(None, 30)

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
        self.bloqueado = False
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
        if self.rect.collidepoint(pos_mouse) and not self.revelado and not self.bloqueado:
            pygame.draw.rect(self.image, DESTAQUE, self.image.get_rect(), 5)
        else:
            pygame.draw.rect(self.image, AZUL, self.image.get_rect(), 5)

    def bloquear_bloco(self):
        self.image.fill(CINZA)
        self.bloqueado = True

blocos = pygame.sprite.Group()
posicoes = [(0, 100), (400, 100), (0, 300), (400, 300)]
for pos, parte in zip(posicoes, partes_imagem):
    problema, resposta = gerar_problema()
    bloco = BlocoImagem(*pos, parte, problema, resposta)
    blocos.add(bloco)

def desenhar_texto_centralizado(texto, fonte, cor, y):
    texto_surface = fonte.render(texto, True, cor)
    tela.blit(texto_surface, (tela.get_width() // 2 - texto_surface.get_width() // 2, y))

def desenhar_caixa_entrada(superficie, texto_entrada, x, y, blocos_revelados, largura=300, altura=50):
    caixa_entrada = pygame.Rect(x, y, largura, altura)
    cor_caixa = DESTAQUE if caixa_entrada.collidepoint(pygame.mouse.get_pos()) and blocos_revelados > 0 else PRETO
    pygame.draw.rect(superficie, cor_caixa, caixa_entrada, 2)
    texto_surface = fonte_entrada.render(texto_entrada, True, PRETO)
    superficie.blit(texto_surface, (caixa_entrada.x + 10, caixa_entrada.y + 10))

def tela_instrucoes():
    tela.fill(BRANCO)
    pygame.draw.rect(tela, AZUL, (40, 70, 720, 250), 5)
    instrucoes = [
        "Bem-vindo ao nosso jogo! Novo por aqui?",
        "1. Clique em qualquer quadrado para aparecer a conta matemática.",
        "2. Resolva-a para revelar uma parte da imagem.",
        "3. Após resolver todas, adivinhe a imagem para vencer!",
        "4. Se errar 2 vezes, perde a chance de revelar aquela parte."
    ]
    for i, instrucao in enumerate(instrucoes):
        desenhar_texto_centralizado(instrucao, fonte_instrucao, PRETO, 100 + i * 40)

    x_rect = pygame.Rect(750, 20, 30, 30)
    cor_x = BRANCO if x_rect.collidepoint(pygame.mouse.get_pos()) else PRETO
    pygame.draw.rect(tela, PRETO, x_rect)
    tela.blit(fonte_instrucao.render("X", True, cor_x), (758, 20))
    pygame.display.flip()

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

def tela_derrota():
    tela.fill(BRANCO)
    texto_derrota = fonte_titulo.render("Você Perdeu!", True, VERMELHO)
    tela.blit(texto_derrota, (250, 250))
    pygame.display.flip()
    pygame.time.delay(3000)

rodando, bloco_atual, texto_adivinhar = True, None, ""
blocos_revelados, max_revelacoes, vitoria = 0, 4, False
exibindo_instrucoes = True
tentativas_adivinhacao = 0 

while rodando:
    pos_mouse = pygame.mouse.get_pos()
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

        if exibindo_instrucoes:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if pygame.Rect(750, 20, 30, 30).collidepoint(evento.pos):
                    exibindo_instrucoes = False
            continue

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
                if bloco.rect.collidepoint(evento.pos) and not bloco.bloqueado:
                    bloco_atual = bloco if not bloco.revelado else None

        if evento.type == pygame.KEYDOWN and not bloco_atual:
            if evento.key == pygame.K_BACKSPACE:
                texto_adivinhar = texto_adivinhar[:-1]
            elif evento.key == pygame.K_RETURN and blocos_revelados > 0:
                if texto_adivinhar.lower() == "biblioteca":
                    vitoria = True
                    rodando = False
                else:
                    tentativas_adivinhacao += 1  
                    texto_adivinhar = ""
                    if tentativas_adivinhacao >= 3:
                        tela_derrota()
                        rodando = False
            else:
                texto_adivinhar += evento.unicode

    if exibindo_instrucoes:
        tela_instrucoes()
        pygame.display.flip()
        continue

    if all(bloco.bloqueado for bloco in blocos):
        tela_derrota()
        rodando = False

    for bloco in blocos:
        bloco.atualizar(pos_mouse)

    tela.fill(BRANCO)
    desenhar_titulo(tela, "Adivinhe a Imagem Matemática", 150, 20)
    blocos.draw(tela)
    desenhar_caixa_entrada(tela, texto_adivinhar, 250, 520, blocos_revelados, 300, 50)

    if bloco_atual:
        bloco_atual.desenhar_problema(tela)

    pygame.display.flip()

if vitoria:
    tela_vitoria()
elif tentativas_adivinhacao >= 3:
    tela_derrota()

pygame.quit()
