from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

# SM64-style settings
window.title = 'Mario 64 Style Castle'
window.borderless = False
window.fullscreen = False

# Load textures (you'll need to add these image files to your project)
# For now using solid colors as placeholders
class SM64Player(Entity):
    def __init__(self):
        super().__init__(
            model='cube',
            texture='white_cube',
            color=color.red,
            scale=(1, 2, 1),
            position=(0, 5, 0)
        )
        self.speed = 5
        self.jump_height = 8
        self.velocity_y = 0
        self.gravity = 20
        self.grounded = False
        self.camera_pivot = Entity(parent=self, y=1.5)
        
    def update(self):
        # Movement
        movement = Vec3(0, 0, 0)
        
        if held_keys['w']:
            movement += self.forward
        if held_keys['s']:
            movement -= self.forward
        if held_keys['a']:
            movement -= self.right
        if held_keys['d']:
            movement += self.right
            
        if movement.length() > 0:
            movement = movement.normalized() * self.speed * time.dt
            
        self.position += movement
        
        # Jumping with gravity
        self.velocity_y -= self.gravity * time.dt
        self.y += self.velocity_y * time.dt
        
        # Ground collision
        if self.y <= 0.5:
            self.y = 0.5
            self.velocity_y = 0
            self.grounded = True
        else:
            self.grounded = False
            
    def input(self, key):
        if key == 'space' and self.grounded:
            self.velocity_y = self.jump_height

class CastleBlock(Entity):
    def __init__(self, position, scale, texture='white_cube', color=color.white):
        super().__init__(
            model='cube',
            color=color,
            texture=texture,
            position=position,
            scale=scale,
            collider='box'
        )

class Coin(Entity):
    def __init__(self, position):
        super().__init__(
            model='sphere',
            color=color.yellow,
            position=position,
            scale=0.5,
            collider='sphere'
        )
        self.rotation_speed = 100
        
    def update(self):
        self.rotation_y += self.rotation_speed * time.dt

# Create scene
def create_castle_scene():
    # Ground
    ground = Entity(
        model='plane',
        texture='white_cube',
        color=color.green,
        scale=(50, 1, 50),
        y=-0.5,
        collider='box'
    )
    
    # Main castle structure
    CastleBlock(position=(0, 5, 0), scale=(6, 10, 6), color=color.gray)  # Central tower
    CastleBlock(position=(0, 2, -8), scale=(10, 4, 4), color=color.light_gray)  # Entrance hall
    
    # Surrounding towers
    tower_positions = [(8, 3, 8), (-8, 3, 8), (8, 3, -8), (-8, 3, -8)]
    for pos in tower_positions:
        CastleBlock(position=pos, scale=(3, 6, 3), color=color.gray)
    
    # Platforms and obstacles
    CastleBlock(position=(5, 1, 0), scale=(2, 0.5, 8), color=color.blue)  # Bridge
    CastleBlock(position=(-12, 3, 0), scale=(4, 0.5, 4), color=color.orange)  # Platform
    CastleBlock(position=(12, 5, 5), scale=(4, 0.5, 4), color=color.orange)  # High platform
    
    # Coins
    coin_positions = [
        (0, 8, 0), (5, 2, 0), (-12, 4, 0), 
        (12, 6, 5), (8, 4, 8), (-8, 4, -8)
    ]
    for pos in coin_positions:
        Coin(position=pos)

# Setup
create_castle_scene()
player = SM64Player()

# SM64-style camera
camera.parent = player.camera_pivot
camera.position = (0, 0, 0)
camera.rotation = (0, 0, 0)
camera.fov = 90

# Instructions
text = Text(
    text='WASD: Move | SPACE: Jump | Mouse: Look around',
    position=(-0.8, 0.4),
    scale=1.5
)

def update():
    # Camera rotation with mouse
    player.rotation_y += mouse.velocity[0] * 100
    player.camera_pivot.rotation_x -= mouse.velocity[1] * 100
    player.camera_pivot.rotation_x = clamp(player.camera_pivot.rotation_x, -90, 90)

app.run()
