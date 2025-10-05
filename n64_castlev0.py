#!/usr/bin/env python3
"""
N64 TECH DEMO - Princess Peach's Castle
A playable SGI/N64-style tech demo featuring:
- Player movement with Mario sprite
- Collectible stars and coins
- Interactive castle elements
- Classic N64 visual effects
"""

import turtle
import math
import random
import time

class N64TechDemo:
    def __init__(self):
        self.screen = None
        self.player = None
        self.stars = []
        self.coins = []
        self.collected_stars = 0
        self.collected_coins = 0
        self.demo_mode = False
        self.frame_count = 0
        self.player_x = 0
        self.player_y = -150
        self.player_speed = 5
        self.jump_velocity = 0
        self.is_jumping = False
        self.gravity = -0.5
        self.ground_level = -150
        self.messages = []
        self.castle_door_open = False
        
    def setup_screen(self):
        """Initialize the demo screen with N64 aesthetics."""
        self.screen = turtle.Screen()
        self.screen.title("N64 TECH DEMO - Super Mario 64 Castle v1.0 [600x400 @ 60FPS]")
        self.screen.bgcolor("#87CEEB")  # Sky blue
        self.screen.setup(width=600, height=400)
        self.screen.tracer(0)  # Turn off automatic screen updates
        
        # Register key bindings
        self.screen.onkey(lambda: self.move_player('left'), 'Left')
        self.screen.onkey(lambda: self.move_player('right'), 'Right')
        self.screen.onkey(lambda: self.move_player('up'), 'Up')
        self.screen.onkey(lambda: self.move_player('down'), 'Down')
        self.screen.onkey(self.jump, 'space')
        self.screen.onkey(self.toggle_demo_mode, 'd')
        self.screen.onkey(self.reset_demo, 'r')
        self.screen.onkey(self.interact, 'Return')
        self.screen.listen()
        
        return self.screen
    
    def create_player(self):
        """Create the player character (Mario)."""
        self.player = turtle.Turtle()
        self.player.shape("circle")
        self.player.color("red")
        self.player.penup()
        self.player.goto(self.player_x, self.player_y)
        self.player.shapesize(1.5, 1.5)
        
        # Create player hat (simplified Mario cap)
        self.player_hat = turtle.Turtle()
        self.player_hat.shape("triangle")
        self.player_hat.color("red")
        self.player_hat.penup()
        self.player_hat.shapesize(0.5, 1)
        
    def draw_castle(self):
        """Draw the castle with N64 low-poly aesthetic."""
        castle = turtle.Turtle()
        castle.hideturtle()
        castle.speed(0)
        castle.pensize(3)
        
        # Main keep (scaled for 600x400)
        self.draw_rectangle(castle, -75, -120, 150, 180, "#FFE4B5")
        self.draw_triangle_roof(castle, -90, 60, 180, "#DC143C")
        
        # Left tower (scaled)
        self.draw_rectangle(castle, -180, -120, 90, 150, "#FFE4B5")
        self.draw_triangle_roof(castle, -190, 30, 110, "#DC143C")
        
        # Right tower (scaled)
        self.draw_rectangle(castle, 90, -120, 90, 150, "#FFE4B5")
        self.draw_triangle_roof(castle, 80, 30, 110, "#DC143C")
        
        # Windows (scaled)
        self.draw_window(castle, -45, 0, 25, "#ADD8E6")
        self.draw_window(castle, 20, 0, 25, "#ADD8E6")
        
        # Castle door
        if self.castle_door_open:
            self.draw_arch(castle, -30, -120, 60, 60, "#000000")  # Open door
        else:
            self.draw_arch(castle, -30, -120, 60, 60, "#8B4513")  # Closed door
            
        # Draw ground (adjusted for 600x400)
        castle.penup()
        castle.goto(-300, -150)
        castle.pendown()
        castle.fillcolor("#90EE90")
        castle.begin_fill()
        castle.goto(300, -150)
        castle.goto(300, -200)
        castle.goto(-300, -200)
        castle.goto(-300, -150)
        castle.end_fill()
        
    def draw_rectangle(self, t, x, y, width, height, color):
        """Draw a filled rectangle."""
        t.penup()
        t.goto(x, y)
        t.pendown()
        t.fillcolor(color)
        t.begin_fill()
        for _ in range(2):
            t.forward(width)
            t.left(90)
            t.forward(height)
            t.left(90)
        t.end_fill()
        
    def draw_triangle_roof(self, t, x, y, base, color):
        """Draw a triangular roof."""
        t.penup()
        t.goto(x, y)
        t.pendown()
        t.fillcolor(color)
        t.begin_fill()
        t.setheading(0)
        height = base * 0.6
        t.forward(base)
        t.goto(x + base/2, y + height)
        t.goto(x, y)
        t.end_fill()
        
    def draw_window(self, t, x, y, size, color):
        """Draw a window."""
        self.draw_rectangle(t, x, y, size, size, color)
        # Add window cross
        t.penup()
        t.goto(x + size/2, y)
        t.pendown()
        t.goto(x + size/2, y + size)
        t.penup()
        t.goto(x, y + size/2)
        t.pendown()
        t.goto(x + size, y + size/2)
        
    def draw_arch(self, t, x, y, width, height, color):
        """Draw an archway door."""
        t.penup()
        t.goto(x, y)
        t.pendown()
        t.fillcolor(color)
        t.begin_fill()
        t.setheading(0)
        t.forward(width)
        t.left(90)
        t.forward(height * 0.6)
        t.circle(-width/2, 180)
        t.forward(height * 0.6)
        t.end_fill()
        
    def create_collectibles(self):
        """Create stars and coins to collect."""
        # Create stars (adjusted positions for 600x400)
        star_positions = [(-150, -140), (150, -140), (0, 40), (-120, 0), (120, 0)]
        for i, pos in enumerate(star_positions):
            star = turtle.Turtle()
            star.shape("triangle")
            star.color("gold")
            star.penup()
            star.goto(pos)
            star.shapesize(1.5, 1.5)
            star.id = i
            self.stars.append(star)
            
        # Create coins (adjusted range for 600x400)
        for _ in range(10):
            coin = turtle.Turtle()
            coin.shape("circle")
            coin.color("yellow")
            coin.penup()
            coin.goto(random.randint(-280, 280), random.randint(-140, 150))
            coin.shapesize(0.5, 0.5)
            self.coins.append(coin)
            
    def move_player(self, direction):
        """Move the player character."""
        if direction == 'left' and self.player_x > -280:
            self.player_x -= self.player_speed
        elif direction == 'right' and self.player_x < 280:
            self.player_x += self.player_speed
        elif direction == 'up' and self.player_y < 180:
            self.player_y += self.player_speed
        elif direction == 'down' and self.player_y > self.ground_level:
            self.player_y -= self.player_speed
            
    def jump(self):
        """Make the player jump."""
        if not self.is_jumping and self.player_y <= self.ground_level + 5:
            self.is_jumping = True
            self.jump_velocity = 15
            
    def update_physics(self):
        """Update jump physics."""
        if self.is_jumping:
            self.player_y += self.jump_velocity
            self.jump_velocity += self.gravity
            
            if self.player_y <= self.ground_level:
                self.player_y = self.ground_level
                self.is_jumping = False
                self.jump_velocity = 0
                
    def check_collisions(self):
        """Check for collisions with collectibles."""
        player_pos = (self.player_x, self.player_y)
        
        # Check star collisions
        for star in self.stars[:]:
            if self.distance(player_pos, star.position()) < 30:
                star.hideturtle()
                self.stars.remove(star)
                self.collected_stars += 1
                self.show_message(f"STAR GET! ({self.collected_stars}/5)", 1)
                
        # Check coin collisions
        for coin in self.coins[:]:
            if self.distance(player_pos, coin.position()) < 20:
                coin.hideturtle()
                self.coins.remove(coin)
                self.collected_coins += 1
                self.show_message(f"COIN! x{self.collected_coins}", 0.5)
                
        # Check if player is at castle door
        if -30 < self.player_x < 30 and self.player_y < -100:
            if self.collected_stars >= 3 and not self.castle_door_open:
                self.castle_door_open = True
                self.show_message("CASTLE UNLOCKED!", 2)
                self.draw_castle()  # Redraw with open door
                
    def distance(self, p1, p2):
        """Calculate distance between two points."""
        return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
        
    def interact(self):
        """Interact with castle elements."""
        # Check if near castle door
        if -30 < self.player_x < 30 and self.player_y < -100:
            if self.castle_door_open:
                self.show_message("ENTERING CASTLE... (Demo Complete!)", 3)
                self.demo_complete()
            else:
                self.show_message(f"Need {3 - self.collected_stars} more stars!", 1)
                
    def show_message(self, text, duration):
        """Display a message on screen."""
        msg = turtle.Turtle()
        msg.hideturtle()
        msg.penup()
        msg.goto(0, 140)
        msg.color("white")
        msg.write(text, align="center", font=("Arial", 20, "bold"))
        self.messages.append((msg, time.time() + duration))
        
    def update_messages(self):
        """Update and remove expired messages."""
        current_time = time.time()
        for msg, expire_time in self.messages[:]:
            if current_time > expire_time:
                msg.clear()
                self.messages.remove((msg, expire_time))
                
    def toggle_demo_mode(self):
        """Toggle automatic demo mode."""
        self.demo_mode = not self.demo_mode
        status = "ON" if self.demo_mode else "OFF"
        self.show_message(f"DEMO MODE: {status}", 1)
        
    def demo_movement(self):
        """Automatic movement for demo mode."""
        if self.demo_mode:
            # Sine wave movement pattern (adjusted for 600x400)
            self.player_x = 150 * math.sin(self.frame_count * 0.02)
            # Occasional jumps
            if self.frame_count % 120 == 0:
                self.jump()
                
    def reset_demo(self):
        """Reset the demo."""
        self.player_x = 0
        self.player_y = self.ground_level
        self.collected_stars = 0
        self.collected_coins = 0
        self.castle_door_open = False
        self.is_jumping = False
        self.jump_velocity = 0
        
        # Reset collectibles
        for star in self.stars:
            star.hideturtle()
        for coin in self.coins:
            coin.hideturtle()
        self.stars.clear()
        self.coins.clear()
        
        self.create_collectibles()
        self.draw_castle()
        self.show_message("DEMO RESET!", 1)
        
    def draw_hud(self):
        """Draw the heads-up display."""
        hud = turtle.Turtle()
        hud.hideturtle()
        hud.penup()
        
        # Stars counter
        hud.goto(-280, 170)
        hud.color("gold")
        hud.write(f"★ {self.collected_stars}/5", font=("Arial", 16, "bold"))
        
        # Coins counter
        hud.goto(-280, 150)
        hud.color("yellow")
        hud.write(f"● {self.collected_coins}", font=("Arial", 16, "bold"))
        
        # Controls
        hud.goto(280, 170)
        hud.color("white")
        hud.write("Controls:", align="right", font=("Arial", 12, "normal"))
        hud.goto(280, 155)
        hud.write("Arrows: Move", align="right", font=("Arial", 10, "normal"))
        hud.goto(280, 140)
        hud.write("Space: Jump", align="right", font=("Arial", 10, "normal"))
        hud.goto(280, 125)
        hud.write("Enter: Interact", align="right", font=("Arial", 10, "normal"))
        hud.goto(280, 110)
        hud.write("D: Demo Mode", align="right", font=("Arial", 10, "normal"))
        hud.goto(280, 95)
        hud.write("R: Reset", align="right", font=("Arial", 10, "normal"))
        
        # Title
        hud.goto(0, 170)
        hud.color("red")
        hud.write("N64 TECH DEMO", align="center", font=("Arial", 18, "bold"))
        
        # FPS indicator
        hud.goto(0, -185)
        hud.color("lime")
        hud.write("60 FPS", align="center", font=("Arial", 10, "bold"))
        
        return hud
        
    def demo_complete(self):
        """Show demo completion screen."""
        complete = turtle.Turtle()
        complete.hideturtle()
        complete.penup()
        complete.goto(0, 50)
        complete.color("gold")
        complete.write("DEMO COMPLETE!", align="center", font=("Arial", 24, "bold"))
        complete.goto(0, 20)
        complete.write(f"Stars: {self.collected_stars}/5", align="center", font=("Arial", 18, "normal"))
        complete.goto(0, -5)
        complete.write(f"Coins: {self.collected_coins}", align="center", font=("Arial", 18, "normal"))
        complete.goto(0, -35)
        complete.color("white")
        complete.write("Thanks for playing!", align="center", font=("Arial", 14, "normal"))
        complete.goto(0, -60)
        complete.write("SGI/N64 Tech Demo v1.0", align="center", font=("Arial", 10, "italic"))
        complete.goto(0, -80)
        complete.write("600x400 @ 60FPS", align="center", font=("Arial", 10, "italic"))
        
    def animate_collectibles(self):
        """Animate the collectibles."""
        # Rotate stars
        for star in self.stars:
            star.right(3)
            
        # Bob coins up and down
        for i, coin in enumerate(self.coins):
            y = coin.ycor()
            offset = math.sin(self.frame_count * 0.05 + i) * 2
            coin.sety(coin.position()[1] + offset - y + coin.position()[1])
            
    def run(self):
        """Main game loop optimized for 60 FPS."""
        print("=== N64 TECH DEMO - PRINCESS PEACH'S CASTLE ===")
        print("Resolution: 600x400 @ 60 FPS")
        print("Collect 3 stars to unlock the castle!")
        print("Press 'D' for demo mode, 'R' to reset")
        
        self.setup_screen()
        self.draw_castle()
        self.create_player()
        self.create_collectibles()
        
        hud = None
        frame_time = 1.0 / 60.0  # Target 60 FPS
        last_time = time.time()
        
        # Main game loop
        while True:
            try:
                current_time = time.time()
                delta_time = current_time - last_time
                
                # Only update if enough time has passed for 60 FPS
                if delta_time >= frame_time:
                    self.frame_count += 1
                    
                    # Update demo mode
                    self.demo_movement()
                    
                    # Update physics
                    self.update_physics()
                    
                    # Update player position
                    self.player.goto(self.player_x, self.player_y)
                    self.player_hat.goto(self.player_x, self.player_y + 15)
                    
                    # Animate collectibles
                    self.animate_collectibles()
                    
                    # Check collisions
                    self.check_collisions()
                    
                    # Update messages
                    self.update_messages()
                    
                    # Update HUD
                    if hud:
                        hud.clear()
                    hud = self.draw_hud()
                    
                    # Update screen
                    self.screen.update()
                    last_time = current_time
                
            except turtle.Terminator:
                break
            except Exception as e:
                print(f"Error: {e}")
                break

def main():
    """Entry point for the tech demo."""
    demo = N64TechDemo()
    demo.run()

if __name__ == "__main__":
    main()
