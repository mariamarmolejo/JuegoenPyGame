# AUTOR: MARIA MARMOLEJO
# FECHA: 03/06/2023
# PROYECTO: TEST KODLAND PYTHON "CUBO SALTARIN"

# Importo la libreriade Pygame y el modulo Random
import pygame
import random

# Inicializar Pygame
pygame.init()

# Dimensiones de la ventana
WIDTH = 800
HEIGHT = 400

# Colores en RGB
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
PINK = (255, 105, 180)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)

# Configuración de la ventana
ventana = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CuboSaltarin")

# Clase para el jugador
class Player(pygame.sprite.Sprite):
    def __init__(self, color):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (100, HEIGHT // 2)
        self.y_speed = 0

    def update(self):
        self.y_speed += 1
        self.rect.y += self.y_speed
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT

    def jump(self):
        self.y_speed = -15

# Clase para los obstáculos
class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, random.randint(50, 200)))
        self.image.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        self.rect.y = HEIGHT - self.rect.height

    def update(self):
        self.rect.x -= 5
        if self.rect.right < 0:
            self.kill()

# Función para mostrar el puntaje en la ventana
def mostrarPuntaje(puntos, nombre):
    font = pygame.font.SysFont(None, 36)
    text = font.render(nombre +": " + str(puntos), True, BLACK)
    ventana.blit(text, (10, 10))

# Función para mostrar el último puntaje más alto en la ventana
def mostrarPuntajeAlto(puntos):
    font = pygame.font.SysFont(None, 36)
    text = font.render("Puntaje más alto: " + str(puntos), True, BLACK)
    ventana.blit(text, (10, 50))

# Función para mostrar la pantalla de presentación
def mostrarIntro():
    intro = True
    name = ""
    color = None
    font = pygame.font.SysFont(None, 28)

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if WIDTH // 2 - 75 <= event.pos[0] <= WIDTH // 2 - 25 and 200 <= event.pos[1] <= 250:
                    color = GREEN
                elif WIDTH // 2 - 25 <= event.pos[0] <= WIDTH // 2 + 25 and 200 <= event.pos[1] <= 250:
                    color = PINK
                elif WIDTH // 2 + 25 <= event.pos[0] <= WIDTH // 2 + 75 and 200 <= event.pos[1] <= 250:
                    color = BLUE
                elif WIDTH // 2 + 75 <= event.pos[0] <= WIDTH // 2 + 125 and 200 <= event.pos[1] <= 250:
                    color = PURPLE
                elif WIDTH // 2 - 50 <= event.pos[0] <= WIDTH // 2 + 50 and 360 <= event.pos[1] <= 400:
                    intro = False

            if event.type == pygame.KEYDOWN and intro:
                if event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    name += event.unicode

        ventana.fill(WHITE)
        text = font.render("BIENVENIDO AL CUBO SALTARIN", True, PURPLE)
        ventana.blit(text, (WIDTH // 2 - text.get_width() // 2, 50))

        text = font.render("El juego consiste en que el cubo pueda saltar y no chocar para ganar puntos,", True, BLACK)
        ventana.blit(text, (WIDTH // 2 - text.get_width() // 2, 85))
        text = font.render("Presiona espacio para evitar los obstaculos y obtener el puntaje mas alto.", True, BLACK)
        ventana.blit(text, (WIDTH // 2 - text.get_width() // 2, 110))
        
        text = font.render("Elige el color de tu cubo:", True, BLACK)
        ventana.blit(text, (WIDTH // 2 - text.get_width() // 2, 150))

        pygame.draw.rect(ventana, GREEN, (WIDTH // 2 - 75, 200, 50, 50))
        pygame.draw.rect(ventana, PINK, (WIDTH // 2 - 25, 200, 50, 50))
        pygame.draw.rect(ventana, BLUE, (WIDTH // 2 + 25, 200, 50, 50))
        pygame.draw.rect(ventana, PURPLE, (WIDTH // 2 + 75, 200, 50, 50))

        pygame.draw.rect(ventana, BLACK, (WIDTH // 2 - 75, 200, 50, 50), 3)
        pygame.draw.rect(ventana, BLACK, (WIDTH // 2 - 25, 200, 50, 50), 3)
        pygame.draw.rect(ventana, BLACK, (WIDTH // 2 + 25, 200, 50, 50), 3)
        pygame.draw.rect(ventana, BLACK, (WIDTH // 2 + 75, 200, 50, 50), 3)

        text = font.render("JUGAR", True, BLACK)
        ventana.blit(text, (WIDTH // 2 - text.get_width() // 2, 360))

        pygame.draw.rect(ventana, BLACK, (WIDTH // 2 - 50, 350, 100, 40), 3)

        text = font.render("Escribe tu nombre:", True, BLACK)
        ventana.blit(text, (WIDTH // 2 - text.get_width() // 2, 270))

        text = font.render(name, True, BLACK)
        ventana.blit(text, (WIDTH // 2 - text.get_width() // 2, 300))

        pygame.display.update()

    return name, color

# Función principal del juego
def game(player_name, player_color):
    # Variables del juego
    score = 0
    high_score = 0
    running = True

    # Crear jugador
    player = Player(player_color)
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    # Crear grupos de obstáculos
    obstacles = pygame.sprite.Group()

    # Reloj del juego
    clock = pygame.time.Clock()

    # Bucle principal del juego
    while running:
        # Eventos del juego
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.jump()

        # Actualizar jugador
        all_sprites.update()

        # Generar obstáculos
        if random.randrange(100) < 2:
            obstacle = Obstacle()
            obstacles.add(obstacle)
            all_sprites.add(obstacle)

        # Detectar colisión con obstáculos
        if pygame.sprite.spritecollide(player, obstacles, False):
            if score > high_score:
                high_score = score
            score = 0
            obstacles.empty()

        # Dibujar en la ventana
        ventana.fill(WHITE)
        all_sprites.draw(ventana)
        mostrarPuntaje(score, player_name)
        mostrarPuntajeAlto(high_score)
        pygame.display.flip()

        # Actualizar puntaje
        score += 1

        # Controlar la velocidad del juego
        clock.tick(40)

# Función principal
def main():
    # Mostrar pantalla de presentación y obtener nombre y color del jugador
    player_name, player_color = mostrarIntro()

    # Iniciar el juego
    game(player_name, player_color)

    # Finalizar Pygame
    pygame.quit()

# Ejecutar el juego
if __name__ == "__main__":
    main()