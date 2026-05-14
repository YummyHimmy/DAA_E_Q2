import pygame
import sys
import random

class Button:
    def __init__(
        self, x, y, width, height, text,
        color=(15, 15, 25),
        hover_color=(65, 65, 75), # Dark when hover
        selected_color=(180, 60, 60) # Red when select
    ):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.selected_color = selected_color

        self.current_color = color
        self.selected = False

        self.font = pygame.font.SysFont("chiller", 24)

    def draw(self, screen):
        pygame.draw.rect(screen, self.current_color, self.rect, border_radius=10)
        pygame.draw.rect(screen, (240, 240, 240), self.rect, 2, border_radius=10)

        text_surf = self.font.render(self.text, True, (240, 240, 240))
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_hovered(self, pos):
        return self.rect.collidepoint(pos)

    def update(self, pos):
        if self.selected:
            self.current_color = self.selected_color
        elif self.is_hovered(pos):
            self.current_color = self.hover_color
        else:
            self.current_color = self.color

    def is_clicked(self, pos, event):
        return (
            self.is_hovered(pos)
            and event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
        )

class Particle:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.reset()

    def reset(self):
        self.x = random.randint(0, self.screen_width)
        self.y = random.randint(-self.screen_height, 0)

        self.radius = random.randint(2, 5)

        self.speed = random.uniform(0.5, 2.0)

        self.alpha = random.randint(60, 180)

        self.drift = random.uniform(-0.5, 0.5)

    def update(self):
        self.y += self.speed
        self.x += self.drift

        if self.y > self.screen_height:
            self.reset()
            self.y = random.randint(-100, -10)

    def draw(self, screen):
        surface = pygame.Surface(
            (self.radius * 4, self.radius * 4),
            pygame.SRCALPHA
        )

        pygame.draw.circle(
            surface,
            (80, 255, 120, self.alpha),
            (self.radius * 2, self.radius * 2),
            self.radius
        )

        screen.blit(surface, (self.x, self.y))

class HomeScreen:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.running = True
        self.selected_difficulty = "EASY"
        self.start_game = False
        
        center_x = screen_width // 2
        center_y = screen_height // 2
        
        button_width = 200
        button_height = 50
        button_spacing = 20
        
        self.easy_button = Button(
            center_x - button_width // 2,
            center_y - button_height - button_spacing,
            button_width, button_height, "EASY"
        )
        
        self.medium_button = Button(
            center_x - button_width // 2,
            center_y,
            button_width, button_height, "MEDIUM"
        )
        
        self.hard_button = Button(
            center_x - button_width // 2,
            center_y + button_height + button_spacing,
            button_width, button_height, "HARD"
        )
        
        self.start_button = Button(
            center_x - button_width // 2,
            center_y + 2 * (button_height + button_spacing),
            button_width, button_height, "START GAME", 
            color=(15, 115, 25), hover_color=(25, 125, 35)
        )

        self.particles = [
            Particle(screen_width, screen_height)
            for _ in range(80)
        ]
        
    def run(self, screen):
        while self.running and not self.start_game:
            mouse_pos = pygame.mouse.get_pos()
            
            self.easy_button.update(mouse_pos)
            self.medium_button.update(mouse_pos)
            self.hard_button.update(mouse_pos)
            self.start_button.update(mouse_pos)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                        return None

                if self.easy_button.is_clicked(mouse_pos, event):
                    self.selected_difficulty = "EASY"
                    self.easy_button.selected = True
                    self.medium_button.selected = False
                    self.hard_button.selected = False
                
                elif self.medium_button.is_clicked(mouse_pos, event):
                    self.selected_difficulty = "MEDIUM"
                    self.easy_button.selected = False
                    self.medium_button.selected = True
                    self.hard_button.selected = False
                
                elif self.hard_button.is_clicked(mouse_pos, event):
                    self.selected_difficulty = "HARD"
                    self.easy_button.selected = False
                    self.medium_button.selected = False
                    self.hard_button.selected = True

                elif self.start_button.is_clicked(mouse_pos, event) and self.selected_difficulty:
                    self.start_game = True
            
            screen.fill((15, 15, 25))

            for particle in self.particles:
                particle.update()
                particle.draw(screen)
                
            self.title_font = pygame.font.SysFont("chiller", 70, bold=True)
            title = self.title_font.render("EXORCIZE", True, (180, 60, 60))
            title_rect = title.get_rect(center=(self.screen_width // 2, 100))
            screen.blit(title, title_rect)
            
            self.easy_button.draw(screen)
            self.medium_button.draw(screen)
            self.hard_button.draw(screen)
            self.start_button.draw(screen)
            
            pygame.display.flip()
            pygame.time.Clock().tick(60)
        
        if self.start_game:
            return self.selected_difficulty
        return None
