# program.py — Baby Bowser Fight (SMW Mario + SMB3 HUD + SMB1 Fireballs)
# Press [E] to fire fireballs (SMB1-style)

import pygame
import random
import math

pygame.init()
pygame.mixer.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 256, 240
FPS = 60
GRAVITY = 0.35
JUMP_POWER = -7.0
RUN_JUMP_POWER = -8.5
MAX_FALL_SPEED = 6.0

# Colors
BLACK = (0,0,0)
WHITE = (248,248,248)
RED = (228,92,16)
ORANGE = (252,152,56)
YELLOW = (248,216,120)
GREEN = (0,168,0)
BLUE = (0,88,248)
PURPLE = (136,20,176)
BROWN = (172,124,0)
GRAY = (184,184,184)
DARK_GRAY = (92,92,92)
SKY_BLUE = (92,148,252)

# Game states
STATE_APPROACH, STATE_INTRO, STATE_BATTLE, STATE_VICTORY = 0,1,2,3

# --- CLASSES ---

class Mario:
    """SMW-style Mario"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 12
        self.height = 16
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        self.facing_right = True
        self.running = False
        
    def update(self, keys, platforms):
        # Movement
        accel = 0.5
        max_speed = 2.5
        friction = 0.85
        
        if keys[pygame.K_LEFT]:
            self.vel_x -= accel
            self.facing_right = False
        if keys[pygame.K_RIGHT]:
            self.vel_x += accel
            self.facing_right = True
            
        self.vel_x = max(-max_speed, min(max_speed, self.vel_x))
        self.vel_x *= friction
        
        # Jump
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = RUN_JUMP_POWER if abs(self.vel_x) > 2 else JUMP_POWER
            
        # Gravity
        self.vel_y += GRAVITY
        self.vel_y = min(self.vel_y, MAX_FALL_SPEED)
        
        # Apply velocity
        self.x += self.vel_x
        self.y += self.vel_y
        
        # Platform collision
        self.on_ground = False
        for plat in platforms:
            if (self.x + self.width > plat[0] and self.x < plat[0] + plat[2] and
                self.y + self.height >= plat[1] and self.y + self.height <= plat[1] + 10 and
                self.vel_y >= 0):
                self.y = plat[1] - self.height
                self.vel_y = 0
                self.on_ground = True
                
        # Screen bounds
        self.x = max(0, min(SCREEN_WIDTH - self.width, self.x))
        
    def draw(self, screen):
        # Simple Mario sprite
        pygame.draw.rect(screen, RED, (int(self.x), int(self.y), self.width, self.height))
        pygame.draw.rect(screen, BLUE, (int(self.x) + 2, int(self.y) + 2, self.width - 4, 6))

class BabyBowser:
    """Baby Bowser boss"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 24
        self.height = 24
        self.vel_x = 0
        self.vel_y = 0
        self.hp = 6
        self.max_hp = 6
        self.pattern = 0
        self.timer = 0
        self.invuln_timer = 0
        # Intro animation
        self.intro_scale = 0.0
        self.intro_complete = False
        
    def update_intro(self):
        """SMW2-style growth animation"""
        if self.intro_scale < 1.0:
            self.intro_scale += 0.02  # Slow growth
            return False
        else:
            self.intro_complete = True
            return True
        
    def update(self, platforms, mario_fireballs):
        if not self.intro_complete:
            return
            
        self.timer += 1
        if self.invuln_timer > 0:
            self.invuln_timer -= 1
            
        # Simple movement pattern
        if self.timer % 120 < 60:
            self.vel_x = 1
        else:
            self.vel_x = -1
            
        self.x += self.vel_x
        self.x = max(0, min(SCREEN_WIDTH - self.width, self.x))
        
        # Check fireball hits
        for fb in mario_fireballs:
            if fb.alive and self.invuln_timer == 0:
                dist = math.sqrt((fb.x - (self.x + self.width/2))**2 + 
                               (fb.y - (self.y + self.height/2))**2)
                if dist < 15:
                    self.hp -= 1
                    self.invuln_timer = 30
                    fb.alive = False
                    
    def draw(self, screen, intro_mode=False):
        # During intro, draw with scaling
        if intro_mode and not self.intro_complete:
            scale = self.intro_scale
            scaled_w = int(self.width * scale)
            scaled_h = int(self.height * scale)
            center_x = int(self.x + self.width/2)
            center_y = int(self.y + self.height/2)
            
            # Draw scaled Bowser
            pygame.draw.rect(screen, GREEN, 
                           (center_x - scaled_w//2, center_y - scaled_h//2, scaled_w, scaled_h))
            if scaled_w > 8:
                pygame.draw.rect(screen, YELLOW, 
                               (center_x - scaled_w//2 + 4, center_y - scaled_h//2 + 4, 
                                scaled_w - 8, scaled_h//2))
            return
            
        # Normal drawing
        # Flash when invulnerable
        if self.invuln_timer > 0 and self.invuln_timer % 6 < 3:
            return
        # Simple Bowser sprite
        pygame.draw.rect(screen, GREEN, (int(self.x), int(self.y), self.width, self.height))
        pygame.draw.rect(screen, YELLOW, (int(self.x) + 4, int(self.y) + 4, 16, 8))
        # HP bar
        bar_width = 40
        bar_x = self.x + self.width/2 - bar_width/2
        pygame.draw.rect(screen, BLACK, (int(bar_x), int(self.y) - 8, bar_width, 4))
        hp_width = int((self.hp / self.max_hp) * bar_width)
        pygame.draw.rect(screen, RED, (int(bar_x), int(self.y) - 8, hp_width, 4))

class BackgroundBowser:
    """Large background Bowser for intro"""
    def __init__(self):
        self.visible = False
        self.opacity = 0
        
    def update(self):
        """Fade in effect"""
        if self.visible and self.opacity < 255:
            self.opacity = min(255, self.opacity + 5)
        
    def draw(self, screen):
        if self.visible and self.opacity > 0:
            # Create semi-transparent shadow Bowser
            s = pygame.Surface((70, 70))
            s.set_alpha(self.opacity // 2)
            s.fill(DARK_GRAY)
            screen.blit(s, (175, 35))
            # Eyes
            if self.opacity > 100:
                pygame.draw.circle(screen, RED, (195, 55), 6)
                pygame.draw.circle(screen, RED, (215, 55), 6)

class MagicSparkle:
    """Kamek's magic sparkles for intro"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-3, -1)
        self.life = 60
        self.color = random.choice([YELLOW, ORANGE, WHITE, PURPLE])
        
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.1  # Slight gravity
        self.life -= 1
        
    def draw(self, screen):
        if self.life > 0:
            size = max(1, int((self.life / 60) * 3))
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), size)

class SMB3_HUD:
    """Super Mario Bros 3 style HUD"""
    def __init__(self):
        self.coins = 0
        self.lives = 3
        self.time = 300
        self.frame_counter = 0
        
    def update(self):
        """Update timer - counts down once per second"""
        self.frame_counter += 1
        if self.frame_counter >= 60:  # 60 frames = 1 second at 60 FPS
            self.frame_counter = 0
            if self.time > 0:
                self.time -= 1
        
    def draw(self, screen):
        # Top black bar
        pygame.draw.rect(screen, BLACK, (0, 0, SCREEN_WIDTH, 16))
        # Simple HUD text would go here
        font = pygame.font.Font(None, 16)
        text = font.render(f"LIVES:{self.lives} TIME:{self.time}", True, WHITE)
        screen.blit(text, (8, 2))

class MarioFireball:
    """SMB1-style fireball (press E to shoot)"""
    def __init__(self, x, y, facing_right):
        self.x = x
        self.y = y
        self.radius = 4
        self.vel_x = 3.5 if facing_right else -3.5
        self.vel_y = -2
        self.gravity = 0.25  # SMB1 lighter gravity
        self.bounce_damp = 0.8
        self.alive = True

    def update(self, platforms):
        # Apply motion
        self.x += self.vel_x
        self.y += self.vel_y
        self.vel_y += self.gravity

        # Bounce off ground/platforms
        for plat in platforms:
            if (self.x > plat[0] and self.x < plat[0]+plat[2] and
                self.y + self.radius >= plat[1] and
                self.y + self.radius <= plat[1]+10 and
                self.vel_y > 0):
                self.vel_y = -abs(self.vel_y) * self.bounce_damp
                self.y = plat[1] - self.radius

        # Kill if offscreen
        if self.x < -16 or self.x > SCREEN_WIDTH+16 or self.y > SCREEN_HEIGHT+16:
            self.alive = False

    def draw(self, screen):
        frame = (pygame.time.get_ticks()//80) % 3
        colors = [RED, ORANGE, YELLOW]
        color = colors[frame]
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), max(1, self.radius-2))

def create_boom_boom_music():
    """Create simple boss music (placeholder)"""
    return None  # In a real game, would load/generate music

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH*3, SCREEN_HEIGHT*3))
    pygame.display.set_caption("Baby Bowser Fight - Press E to Fire (SMB1 Style)")
    clock = pygame.time.Clock()
    game_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

    mario = Mario(32, 100)
    baby_bowser = BabyBowser(200, 100)
    background_bowser = BackgroundBowser()
    hud = SMB3_HUD()

    boss_music = create_boom_boom_music()
    music_playing = False

    platforms = [
        (0,200,256,40),
        (32,160,48,8),
        (176,160,48,8),
        (96,120,64,8),
    ]

    enemy_fireballs = []
    mario_fireballs = []
    magic_sparkles = []
    game_state = STATE_INTRO  # Start with dramatic intro
    intro_timer = 180  # 3 seconds for intro
    intro_phase = 0  # 0=sparkles, 1=shadow appears, 2=growth
    victory_timer = 0
    approach_flash = 0
    timer_counter = 0
    fireball_cooldown = 300
    last_fireball_time = 0
    screen_shake_x = 0
    screen_shake_y = 0

    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False

        keys = pygame.key.get_pressed()

        # Fireball with E key
        if keys[pygame.K_e] and game_state == STATE_BATTLE:
            now = pygame.time.get_ticks()
            if now - last_fireball_time > fireball_cooldown:
                mario_fireballs.append(MarioFireball(mario.x + (mario.width if mario.facing_right else 0),
                                                     mario.y + mario.height//2,
                                                     mario.facing_right))
                last_fireball_time = now

        # Game state machine
        if game_state == STATE_APPROACH:
            approach_flash += 1
            if approach_flash > 180:
                game_state = STATE_INTRO
                background_bowser.visible = True
                
        elif game_state == STATE_INTRO:
            intro_timer -= 1
            
            # Phase 0: Magic sparkles appear (frames 180-120)
            if intro_timer > 120:
                intro_phase = 0
                if random.random() < 0.3:
                    magic_sparkles.append(MagicSparkle(
                        baby_bowser.x + baby_bowser.width/2 + random.uniform(-20, 20),
                        baby_bowser.y + baby_bowser.height/2 + random.uniform(-20, 20)
                    ))
            # Phase 1: Background Bowser shadow appears (frames 120-60)
            elif intro_timer > 60:
                intro_phase = 1
                background_bowser.visible = True
                background_bowser.update()
                # Add more sparkles
                if random.random() < 0.4:
                    magic_sparkles.append(MagicSparkle(
                        baby_bowser.x + baby_bowser.width/2 + random.uniform(-30, 30),
                        baby_bowser.y + baby_bowser.height/2 + random.uniform(-30, 30)
                    ))
            # Phase 2: Baby Bowser grows! (frames 60-0)
            else:
                intro_phase = 2
                is_complete = baby_bowser.update_intro()
                # Screen shake during growth
                if not is_complete:
                    screen_shake_x = random.randint(-2, 2)
                    screen_shake_y = random.randint(-2, 2)
                    # Intense sparkles
                    if random.random() < 0.5:
                        magic_sparkles.append(MagicSparkle(
                            baby_bowser.x + baby_bowser.width/2 + random.uniform(-40, 40),
                            baby_bowser.y + baby_bowser.height/2 + random.uniform(-40, 40)
                        ))
                else:
                    screen_shake_x = 0
                    screen_shake_y = 0
            
            # Update sparkles
            for sparkle in magic_sparkles:
                sparkle.update()
            magic_sparkles = [s for s in magic_sparkles if s.life > 0]
            
            if intro_timer <= 0:
                game_state = STATE_BATTLE
                background_bowser.visible = False
                magic_sparkles.clear()
                
        elif game_state == STATE_BATTLE:
            # Update timer
            hud.update()
            
            mario.update(keys, platforms)
            baby_bowser.update(platforms, mario_fireballs)
            
            # Update fireballs
            mario_fireballs = [f for f in mario_fireballs if f.alive]
            for f in mario_fireballs:
                f.update(platforms)
                
            # Check victory
            if baby_bowser.hp <= 0:
                game_state = STATE_VICTORY
                victory_timer = 180
                
            # Check time out
            if hud.time <= 0:
                # Game over condition (you could add this)
                pass
                
        elif game_state == STATE_VICTORY:
            victory_timer -= 1
            if victory_timer <= 0:
                running = False

        # Rendering (with screen shake during intro)
        game_surface.fill(SKY_BLUE)
        
        # Draw platforms
        for plat in platforms:
            pygame.draw.rect(game_surface, BROWN, plat)
            pygame.draw.rect(game_surface, ORANGE, (plat[0], plat[1], plat[2], 2))
            
        # Draw game objects
        background_bowser.draw(game_surface)
        
        # Draw magic sparkles during intro
        for sparkle in magic_sparkles:
            sparkle.draw(game_surface)
        
        # Draw Baby Bowser (with intro animation if in intro)
        if game_state == STATE_INTRO:
            baby_bowser.draw(game_surface, intro_mode=True)
        elif game_state >= STATE_BATTLE:
            baby_bowser.draw(game_surface)
            
        mario.draw(game_surface)
        
        for f in mario_fireballs:
            f.draw(game_surface)
            
        # Draw HUD
        hud.draw(game_surface)
        
        # Intro text
        if game_state == STATE_INTRO and intro_timer > 60:
            font = pygame.font.Font(None, 24)
            if intro_phase == 0:
                text = font.render("A challenger appears!", True, WHITE)
                game_surface.blit(text, (SCREEN_WIDTH//2 - 90, 30))
            elif intro_phase == 1:
                text = font.render("Baby Bowser awakens!", True, YELLOW)
                game_surface.blit(text, (SCREEN_WIDTH//2 - 95, 30))
        
        # Victory message
        if game_state == STATE_VICTORY:
            font = pygame.font.Font(None, 36)
            text = font.render("VICTORY!", True, WHITE)
            game_surface.blit(text, (SCREEN_WIDTH//2 - 60, SCREEN_HEIGHT//2))

        # Scale and display (with screen shake)
        scaled = pygame.transform.scale(game_surface, (SCREEN_WIDTH*3, SCREEN_HEIGHT*3))
        screen.fill(BLACK)
        screen.blit(scaled, (screen_shake_x, screen_shake_y))
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
