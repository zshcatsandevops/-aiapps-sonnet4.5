"""
YOSHI'S ISLAND BABY BOWSER FIGHT
Ported to SMB1 NES Engine -> M64 Pro Compatible
HUD: OFF | Pure Gameplay Experience
OG BOSS APPROACH SEQUENCE INCLUDED
"""

import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 256
SCREEN_HEIGHT = 240
FPS = 60
GRAVITY = 0.4
JUMP_POWER = -8.5

# Colors (NES Palette)
BLACK = (0, 0, 0)
WHITE = (248, 248, 248)
RED = (228, 92, 16)
ORANGE = (252, 152, 56)
YELLOW = (248, 216, 120)
GREEN = (0, 168, 0)
BLUE = (0, 88, 248)
PURPLE = (136, 20, 176)
BROWN = (172, 124, 0)
GRAY = (184, 184, 184)
DARK_GRAY = (92, 92, 92)
SKY_BLUE = (92, 148, 252)

# Game States
STATE_APPROACH = 0
STATE_INTRO = 1
STATE_BATTLE = 2
STATE_VICTORY = 3

class BackgroundBowser:
    """Giant Baby Bowser approaching from the background - OG Yoshi's Island style"""
    def __init__(self):
        self.scale = 0.1  # Start tiny in the distance
        self.target_scale = 3.0  # Grow to 3x size
        self.growth_rate = 0.008
        self.base_x = SCREEN_WIDTH // 2
        self.base_y = SCREEN_HEIGHT // 2 + 20
        self.shake_offset_x = 0
        self.shake_offset_y = 0
        self.shake_intensity = 0
        self.roar_timer = 0
        
    def update(self):
        # Grow larger (approaching effect)
        if self.scale < self.target_scale:
            self.scale += self.growth_rate
            
            # Increase shake as he gets closer
            if self.scale > 1.5:
                self.shake_intensity = (self.scale - 1.5) * 3
                
        # Screen shake effect
        if self.shake_intensity > 0:
            self.shake_offset_x = random.randint(-int(self.shake_intensity), int(self.shake_intensity))
            self.shake_offset_y = random.randint(-int(self.shake_intensity), int(self.shake_intensity))
            
        # Roar animation
        if self.scale > 2.5:
            self.roar_timer += 1
            
    def is_complete(self):
        return self.scale >= self.target_scale
        
    def draw(self, screen):
        # Calculate size based on scale
        size = int(32 * self.scale)
        x = self.base_x + self.shake_offset_x - size // 2
        y = self.base_y + self.shake_offset_y - size // 2
        
        # Shadow (gets darker as he approaches)
        shadow_alpha = min(200, int(self.scale * 60))
        shadow_size = size + 10
        pygame.draw.ellipse(screen, DARK_GRAY, 
                          (x - 5, y + size - 5, shadow_size, shadow_size // 3))
        
        # Body (green shell)
        body_rect = pygame.Rect(x, y + size // 4, size, size - size // 4)
        pygame.draw.rect(screen, GREEN, body_rect)
        
        # Shell spikes
        spike_count = max(3, int(self.scale * 3))
        for i in range(spike_count):
            spike_x = x + (size // spike_count) * i + size // (spike_count * 2)
            spike_size = size // 6
            pygame.draw.polygon(screen, ORANGE, [
                (spike_x, y + size // 4),
                (spike_x + spike_size // 2, y),
                (spike_x + spike_size, y + size // 4)
            ])
            
        # Head
        head_y = y + size // 6
        head_radius = int(size // 2.5)
        pygame.draw.circle(screen, GREEN, (x + size // 2, head_y), head_radius)
        
        # Horns
        horn_size = int(size // 8)
        pygame.draw.polygon(screen, ORANGE, [
            (x + size // 2 - head_radius + horn_size, head_y - head_radius),
            (x + size // 2 - head_radius, head_y - head_radius - horn_size),
            (x + size // 2 - head_radius, head_y - head_radius)
        ])
        pygame.draw.polygon(screen, ORANGE, [
            (x + size // 2 + head_radius - horn_size, head_y - head_radius),
            (x + size // 2 + head_radius, head_y - head_radius - horn_size),
            (x + size // 2 + head_radius, head_y - head_radius)
        ])
        
        # Eyes (menacing)
        eye_size = max(2, int(size // 12))
        eye_offset = int(head_radius // 3)
        # White of eyes
        pygame.draw.circle(screen, WHITE, 
                         (x + size // 2 - eye_offset, head_y), eye_size + 1)
        pygame.draw.circle(screen, WHITE, 
                         (x + size // 2 + eye_offset, head_y), eye_size + 1)
        # Pupils (angry)
        pygame.draw.circle(screen, RED, 
                         (x + size // 2 - eye_offset, head_y), eye_size)
        pygame.draw.circle(screen, RED, 
                         (x + size // 2 + eye_offset, head_y), eye_size)
        
        # Mouth (roaring if close enough)
        if self.scale > 2.0:
            mouth_width = int(size // 3)
            mouth_height = int(size // 6) if self.roar_timer % 20 < 10 else int(size // 8)
            mouth_rect = pygame.Rect(x + size // 2 - mouth_width // 2, 
                                    head_y + head_radius // 2,
                                    mouth_width, mouth_height)
            pygame.draw.ellipse(screen, BLACK, mouth_rect)
            
            # Teeth
            tooth_count = 4
            for i in range(tooth_count):
                tooth_x = mouth_rect.x + (mouth_width // tooth_count) * i
                pygame.draw.polygon(screen, WHITE, [
                    (tooth_x, mouth_rect.y),
                    (tooth_x + mouth_width // (tooth_count * 2), mouth_rect.y + 4),
                    (tooth_x + mouth_width // tooth_count, mouth_rect.y)
                ])
                
        # Arms (waving menacingly)
        if self.scale > 1.0:
            arm_length = int(size // 3)
            arm_width = int(size // 8)
            wave_offset = int(math.sin(self.roar_timer * 0.2) * arm_length // 3)
            
            # Left arm
            pygame.draw.rect(screen, GREEN, 
                           (x - arm_width, y + size // 2 + wave_offset, 
                            arm_width, arm_length))
            # Right arm  
            pygame.draw.rect(screen, GREEN,
                           (x + size, y + size // 2 - wave_offset,
                            arm_width, arm_length))

class Mario:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 16
        self.height = 16
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        self.speed = 2.5
        self.facing_right = True
        self.invincible_timer = 0
        self.lives = 3
        
    def update(self, keys, platforms):
        # Horizontal movement (SMB1 style)
        self.vel_x = 0
        if keys[pygame.K_LEFT]:
            self.vel_x = -self.speed
            self.facing_right = False
        if keys[pygame.K_RIGHT]:
            self.vel_x = self.speed
            self.facing_right = True
            
        # Jump (SMB1 physics)
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = JUMP_POWER
            self.on_ground = False
            
        # Apply gravity
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y = 10
            
        # Update position
        self.x += self.vel_x
        self.y += self.vel_y
        
        # Platform collision
        self.on_ground = False
        for platform in platforms:
            if (self.x + self.width > platform[0] and 
                self.x < platform[0] + platform[2] and
                self.y + self.height >= platform[1] and
                self.y + self.height <= platform[1] + 10 and
                self.vel_y >= 0):
                self.y = platform[1] - self.height
                self.vel_y = 0
                self.on_ground = True
                
        # Screen boundaries
        if self.x < 0:
            self.x = 0
        if self.x > SCREEN_WIDTH - self.width:
            self.x = SCREEN_WIDTH - self.width
            
        # Update invincibility
        if self.invincible_timer > 0:
            self.invincible_timer -= 1
            
    def draw(self, screen):
        # Flicker effect when invincible
        if self.invincible_timer > 0 and self.invincible_timer % 4 < 2:
            return
            
        # Draw Mario (simple rectangle with color)
        pygame.draw.rect(screen, RED, (self.x, self.y, self.width, self.height))
        # Cap
        pygame.draw.rect(screen, RED, (self.x + 2, self.y - 4, self.width - 4, 4))
        # Overalls
        pygame.draw.rect(screen, BLUE, (self.x + 4, self.y + 8, self.width - 8, 4))
        
    def take_damage(self):
        if self.invincible_timer <= 0:
            self.lives -= 1
            self.invincible_timer = 120  # 2 seconds at 60 FPS
            return True
        return False

class BabyBowser:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 32
        self.height = 32
        self.vel_x = 0
        self.vel_y = 0
        self.health = 12
        self.max_health = 12
        self.phase = 1  # 1, 2, or 3
        self.attack_timer = 0
        self.attack_cooldown = 120
        self.movement_pattern = 0
        self.on_ground = True
        self.facing_right = True
        self.hit_flash = 0
        
    def update(self, platforms, mario):
        self.attack_timer += 1
        
        # Phase changes
        if self.health <= 8 and self.phase == 1:
            self.phase = 2
            self.attack_cooldown = 90
        elif self.health <= 4 and self.phase == 2:
            self.phase = 3
            self.attack_cooldown = 60
            
        # Movement AI
        if self.attack_timer % 180 < 90:
            # Chase Mario
            if mario.x < self.x:
                self.vel_x = -1.5 * self.phase * 0.5
                self.facing_right = False
            else:
                self.vel_x = 1.5 * self.phase * 0.5
                self.facing_right = True
        else:
            # Jump around
            if self.on_ground and random.random() < 0.02:
                self.vel_y = -7
                
        # Gravity
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y = 10
            
        # Update position
        self.x += self.vel_x
        self.y += self.vel_y
        
        # Platform collision
        self.on_ground = False
        for platform in platforms:
            if (self.x + self.width > platform[0] and 
                self.x < platform[0] + platform[2] and
                self.y + self.height >= platform[1] and
                self.y + self.height <= platform[1] + 10 and
                self.vel_y >= 0):
                self.y = platform[1] - self.height
                self.vel_y = 0
                self.on_ground = True
                
        # Boundaries
        if self.x < 0:
            self.x = 0
            self.vel_x = -self.vel_x
        if self.x > SCREEN_WIDTH - self.width:
            self.x = SCREEN_WIDTH - self.width
            self.vel_x = -self.vel_x
            
        # Update hit flash
        if self.hit_flash > 0:
            self.hit_flash -= 1
            
        return []
        
    def shoot_fireballs(self):
        fireballs = []
        if self.attack_timer >= self.attack_cooldown:
            self.attack_timer = 0
            # Shoot fireballs in different patterns based on phase
            if self.phase == 1:
                # Single fireball toward Mario
                angle = math.atan2(0, 1 if self.facing_right else -1)
                fireballs.append(Fireball(self.x + self.width // 2, self.y + self.height // 2, angle))
            elif self.phase == 2:
                # Triple spread
                for angle_offset in [-0.3, 0, 0.3]:
                    base_angle = 0 if self.facing_right else math.pi
                    fireballs.append(Fireball(self.x + self.width // 2, self.y + self.height // 2, 
                                             base_angle + angle_offset))
            else:
                # Phase 3: Five-way spread
                for i in range(5):
                    angle = (i - 2) * 0.4
                    fireballs.append(Fireball(self.x + self.width // 2, self.y + self.height // 2, angle))
        return fireballs
        
    def take_damage(self):
        self.health -= 1
        self.hit_flash = 10
        
    def draw(self, screen):
        # Flash white when hit
        color = WHITE if self.hit_flash > 0 and self.hit_flash % 4 < 2 else GREEN
        
        # Body
        pygame.draw.rect(screen, color, (self.x, self.y + 8, self.width, self.height - 8))
        # Head
        pygame.draw.circle(screen, color, (int(self.x + self.width // 2), int(self.y + 12)), 12)
        # Shell spikes
        for i in range(3):
            spike_x = self.x + 8 + i * 8
            pygame.draw.polygon(screen, ORANGE, [
                (spike_x, self.y + 8),
                (spike_x + 4, self.y),
                (spike_x + 8, self.y + 8)
            ])
        # Eyes
        eye_offset = 4 if self.facing_right else -4
        pygame.draw.circle(screen, WHITE, (int(self.x + self.width // 2 + eye_offset), int(self.y + 10)), 3)
        pygame.draw.circle(screen, BLACK, (int(self.x + self.width // 2 + eye_offset), int(self.y + 10)), 1)

class Fireball:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = 3
        self.vel_x = math.cos(angle) * self.speed
        self.vel_y = math.sin(angle) * self.speed
        self.radius = 4
        self.lifetime = 180
        
    def update(self):
        self.x += self.vel_x
        self.y += self.vel_y
        self.lifetime -= 1
        
    def draw(self, screen):
        # Animated fireball
        colors = [ORANGE, YELLOW, RED]
        color = colors[(pygame.time.get_ticks() // 100) % 3]
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.radius)
        
    def is_alive(self):
        return (self.lifetime > 0 and 
                0 <= self.x <= SCREEN_WIDTH and 
                0 <= self.y <= SCREEN_HEIGHT)

class Egg:
    def __init__(self, x, y, vel_x, vel_y):
        self.x = x
        self.y = y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.radius = 6
        self.lifetime = 120
        
    def update(self, platforms):
        self.vel_y += GRAVITY * 0.8
        self.x += self.vel_x
        self.y += self.vel_y
        self.lifetime -= 1
        
        # Bounce off platforms
        for platform in platforms:
            if (self.x + self.radius > platform[0] and 
                self.x - self.radius < platform[0] + platform[2] and
                self.y + self.radius >= platform[1] and
                self.y - self.radius <= platform[1] + platform[3]):
                self.vel_y = -self.vel_y * 0.7
                self.vel_x *= 0.9
                self.y = platform[1] - self.radius
                
    def draw(self, screen):
        # Spotted egg
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(screen, GREEN, (int(self.x - 2), int(self.y - 2)), 2)
        pygame.draw.circle(screen, GREEN, (int(self.x + 2), int(self.y + 1)), 2)
        
    def is_alive(self):
        return self.lifetime > 0 and -50 <= self.x <= SCREEN_WIDTH + 50

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH * 3, SCREEN_HEIGHT * 3))
    pygame.display.set_caption("Baby Bowser Fight - SMB1 Engine - M64 Pro Port")
    clock = pygame.time.Clock()
    
    # Scaled surface for pixel-perfect rendering
    game_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    # Game objects
    mario = Mario(32, 100)
    baby_bowser = BabyBowser(200, 100)
    background_bowser = BackgroundBowser()
    
    # Platforms (x, y, width, height)
    platforms = [
        (0, 200, 256, 40),      # Main floor
        (32, 160, 48, 8),        # Left platform
        (176, 160, 48, 8),       # Right platform
        (96, 120, 64, 8),        # Center platform
    ]
    
    fireballs = []
    eggs = []
    game_state = STATE_APPROACH
    intro_timer = 120
    victory_timer = 0
    approach_flash = 0
    
    running = True
    while running:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_e and game_state == STATE_BATTLE:
                    # Throw egg (Yoshi's Island mechanic)
                    angle = 0.3 if mario.facing_right else math.pi - 0.3
                    egg_vel_x = 5 if mario.facing_right else -5
                    eggs.append(Egg(mario.x, mario.y, egg_vel_x, -4))
                    
        keys = pygame.key.get_pressed()
        
        # Clear screen
        game_surface.fill(SKY_BLUE if game_state == STATE_APPROACH else BLACK)
        
        if game_state == STATE_APPROACH:
            # Draw background (castle/throne room vibe)
            # Floor
            pygame.draw.rect(game_surface, BROWN, (0, 180, SCREEN_WIDTH, 60))
            # Brick pattern
            for y in range(180, 240, 8):
                for x in range(0, SCREEN_WIDTH, 16):
                    offset = 8 if (y // 8) % 2 else 0
                    pygame.draw.rect(game_surface, ORANGE, (x + offset, y, 14, 6))
            
            # Update and draw approaching Baby Bowser
            background_bowser.update()
            background_bowser.draw(game_surface)
            
            # Warning text (flashing)
            approach_flash += 1
            if approach_flash % 30 < 15 and background_bowser.scale > 0.5:
                font = pygame.font.Font(None, 12)
                text = font.render("DANGER!", True, RED)
                text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 20))
                game_surface.blit(text, text_rect)
                
            # Transition to intro when approach is complete
            if background_bowser.is_complete():
                game_state = STATE_INTRO
                # Flash effect
                for i in range(5):
                    game_surface.fill(WHITE)
                    
        elif game_state == STATE_INTRO:
            intro_timer -= 1
            if intro_timer <= 0:
                game_state = STATE_BATTLE
                
            # Draw platforms
            for platform in platforms:
                pygame.draw.rect(game_surface, BROWN, platform)
                for i in range(0, platform[2], 8):
                    pygame.draw.rect(game_surface, ORANGE, (platform[0] + i, platform[1], 8, 2))
                    
            # Draw intro text
            font = pygame.font.Font(None, 16)
            text = font.render("BABY BOWSER APPEARS!", True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            game_surface.blit(text, text_rect)
            
            # Draw Baby Bowser entering
            baby_bowser.draw(game_surface)
            
        elif game_state == STATE_BATTLE:
            # Update
            mario.update(keys, platforms)
            baby_bowser.update(platforms, mario)
            
            # Bowser shoots fireballs
            new_fireballs = baby_bowser.shoot_fireballs()
            fireballs.extend(new_fireballs)
            
            # Update fireballs
            for fireball in fireballs[:]:
                fireball.update()
                if not fireball.is_alive():
                    fireballs.remove(fireball)
                # Collision with Mario
                elif (abs(mario.x + mario.width // 2 - fireball.x) < 12 and
                      abs(mario.y + mario.height // 2 - fireball.y) < 12):
                    mario.take_damage()
                    fireballs.remove(fireball)
                    
            # Update eggs
            for egg in eggs[:]:
                egg.update(platforms)
                if not egg.is_alive():
                    eggs.remove(egg)
                # Collision with Baby Bowser
                elif (abs(baby_bowser.x + baby_bowser.width // 2 - egg.x) < 20 and
                      abs(baby_bowser.y + baby_bowser.height // 2 - egg.y) < 20):
                    baby_bowser.take_damage()
                    eggs.remove(egg)
                    if baby_bowser.health <= 0:
                        game_state = STATE_VICTORY
                        victory_timer = 180
                        
            # Draw platforms
            for platform in platforms:
                pygame.draw.rect(game_surface, BROWN, platform)
                # Platform texture
                for i in range(0, platform[2], 8):
                    pygame.draw.rect(game_surface, ORANGE, (platform[0] + i, platform[1], 8, 2))
                    
            # Draw game objects
            mario.draw(game_surface)
            baby_bowser.draw(game_surface)
            
            for fireball in fireballs:
                fireball.draw(game_surface)
                
            for egg in eggs:
                egg.draw(game_surface)
                
            # Check game over
            if mario.lives <= 0:
                font = pygame.font.Font(None, 24)
                text = font.render("GAME OVER", True, RED)
                text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                game_surface.blit(text, text_rect)
                
        elif game_state == STATE_VICTORY:
            victory_timer -= 1
            
            # Draw victory
            for platform in platforms:
                pygame.draw.rect(game_surface, BROWN, platform)
                
            mario.draw(game_surface)
            
            font = pygame.font.Font(None, 20)
            text = font.render("VICTORY!", True, YELLOW)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 60))
            game_surface.blit(text, text_rect)
            
            if victory_timer <= 0:
                running = False
                
        # Scale up to window size
        scaled_surface = pygame.transform.scale(game_surface, (SCREEN_WIDTH * 3, SCREEN_HEIGHT * 3))
        screen.blit(scaled_surface, (0, 0))
        pygame.display.flip()
        
    pygame.quit()

if __name__ == "__main__":
    main()
