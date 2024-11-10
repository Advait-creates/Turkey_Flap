import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen settings
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Turkey - Thanksgiving Edition")

# Colors
WHITE = (255, 255, 255)

# Game variables
GRAVITY = 0.25
TURKEY_FLAP = -6.5
TURKEY_SIZE = (40, 39)
PIPE_WIDTH = 87
PIPE_GAP = 200
PIPE_VELOCITY = -3

# Load images
TURKEY_IMAGE = pygame.transform.scale(pygame.image.load("assets/turkey.png"), TURKEY_SIZE)
PIPE_IMAGE = pygame.image.load("assets/pipe.png")
BG_IMAGE = pygame.image.load("assets/background.png")

# Font for displaying the score
FONT = pygame.font.Font(None, 36)

# Turkey class
class Turkey:
    def __init__(self):
        self.image = TURKEY_IMAGE
        self.rect = self.image.get_rect(center=(100, SCREEN_HEIGHT // 2))
        self.movement = 0

    def flap(self):
        self.movement = TURKEY_FLAP

    def update(self):
        # Apply gravity to turkey movement
        self.movement += GRAVITY
        self.rect.y += self.movement
        # Keep turkey within the screen
        if self.rect.top <= 0:
            self.rect.top = 0

    def draw(self, screen):
        screen.blit(self.image, self.rect)

# Pipe class
class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = random.randint(100, 400)
        self.rect_top = PIPE_IMAGE.get_rect(midbottom=(self.x, self.height - PIPE_GAP // 2))
        self.rect_bottom = PIPE_IMAGE.get_rect(midtop=(self.x, self.height + PIPE_GAP // 2))

    def update(self):
        self.rect_top.x += PIPE_VELOCITY
        self.rect_bottom.x += PIPE_VELOCITY

    def draw(self, screen):
        screen.blit(PIPE_IMAGE, self.rect_top)
        screen.blit(pygame.transform.flip(PIPE_IMAGE, False, True), self.rect_bottom)

# Game functions
def check_collision(turkey, pipes):
    for pipe in pipes:
        if turkey.rect.colliderect(pipe.rect_top) or turkey.rect.colliderect(pipe.rect_bottom):
            return True
    if turkey.rect.bottom >= SCREEN_HEIGHT:
        return True
    return False

def display_score(score):
    score_text = FONT.render(f"Score: {score}", True, WHITE)
    SCREEN.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 20))

def main():
    # Game variables
    clock = pygame.time.Clock()
    turkey = Turkey()
    pipes = [Pipe(SCREEN_WIDTH + i * 300) for i in range(2)]
    score = 0
    running = True

    while running:
        SCREEN.fill(WHITE)
        SCREEN.blit(BG_IMAGE, (0, 0))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    turkey.flap()

        # Update turkey and pipes
        turkey.update()
        for pipe in pipes:
            pipe.update()
            if pipe.rect_top.right < 0:
                pipes.remove(pipe)
                pipes.append(Pipe(SCREEN_WIDTH))
                score += 1  # Increase score for each pipe passed

        # Check for collisions
        if check_collision(turkey, pipes):
            running = False

        # Draw everything
        turkey.draw(SCREEN)
        for pipe in pipes:
            pipe.draw(SCREEN)
        display_score(score)

        pygame.display.update()
        clock.tick(60)  # 60 FPS

    # Game over message
    game_over_text = FONT.render("Game Over! Press R to Restart", True, WHITE)
    SCREEN.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2))
    pygame.display.update()

    # Wait for restart
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    main()

if __name__ == "__main__":
    main()
